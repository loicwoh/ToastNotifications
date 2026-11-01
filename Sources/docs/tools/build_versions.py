"""Build each remote branch/tag that contains docs, without executing its scripts."""
from pathlib import Path
import argparse
import hashlib
import html
import io
import json
import subprocess
import sys
import tarfile
import tempfile


def git(*args: str) -> bytes:
    return subprocess.check_output(['git', *args])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    refs = git('for-each-ref', '--format=%(refname)', 'refs/remotes/origin', 'refs/tags').decode().splitlines()
    versions = []
    builder = Path(__file__).with_name('docs_preview.py')
    with tempfile.TemporaryDirectory() as temp:
        for ref in refs:
            if ref.endswith('/HEAD'):
                continue
            if not git('ls-tree', '--name-only', ref, 'Sources/docs/site/index.html').strip():
                continue
            label = ref.removeprefix('refs/remotes/origin/').removeprefix('refs/tags/')
            is_tag = ref.startswith('refs/tags/')
            id_ = ('tag-' if is_tag else 'branch-') + hashlib.sha256(ref.encode()).hexdigest()[:16]
            source = Path(temp) / id_
            source.mkdir()
            # Read archive bytes as data. Reject links and path traversal; never run
            # scripts/workflows from another branch or tag.
            archive = git('archive', ref, 'Sources')
            with tarfile.open(fileobj=io.BytesIO(archive)) as bundle:
                for member in bundle:
                    if not member.isfile():
                        continue
                    target = (source / member.name).resolve()
                    if not target.is_relative_to(source):
                        raise ValueError('Unsafe archive path')
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(bundle.extractfile(member).read())
            destination = output / 'versions' / id_
            subprocess.run([sys.executable, str(builder), 'build', '--source-root', str(source), '--output', str(destination)], check=True)
            versions.append(dict(id=id_, label=('Release ' if is_tag else '') + label,
                                 ref=ref, commit=git('rev-parse', ref).decode().strip()))
    if not versions:
        raise SystemExit('No branch contains Sources/docs/site/index.html')
    versions.sort(key=lambda v: (0 if v['label'] == 'main' else 1 if v['label'] == 'develop' else 2, v['label']))
    for current in versions:
        manifest = dict(current=current['id'], versions=[dict(v, path='../' + v['id'] + '/?build=' + v['commit'][:12]) for v in versions])
        (output / 'versions' / current['id'] / 'versions.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    # The stable root keeps VI detailed-help links independent of branch slugs.
    # Before main contains docs, show an explicit version landing page.
    stable = next((v for v in versions if v['label'] == 'main'), None)
    if stable is None:
        stable = next((v for v in versions if v['label'] == 'develop'), versions[0])
    if stable:
        target = 'versions/' + stable['id'] + '/?build=' + stable['commit'][:12]
        page = '<!doctype html><title>ToastAPI documentation</title><script>location.replace(' + json.dumps(target) + '+location.hash)</script>'
    else:
        links = ''.join('<li><a href="versions/' + v['id'] + '/">' + html.escape(v['label']) + '</a></li>' for v in versions)
        page = '<!doctype html><html lang="en"><meta charset="utf-8"><title>ToastAPI documentation versions</title><h1>ToastAPI documentation</h1><p>Stable documentation has not been released on main yet. Choose a development version:</p><ul>' + links + '</ul></html>'
    (output / 'index.html').write_text(page, encoding='utf-8')
    (output / '.nojekyll').touch()
    print(f'Built {len(versions)} documentation versions.')


if __name__ == '__main__':
    main()
