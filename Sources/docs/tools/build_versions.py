"""Build main/develop, open-PR branches and published releases as versioned data."""
from pathlib import Path
import argparse
import hashlib
import html
import io
import json
import os
import re
import subprocess
import sys
import tarfile
import tempfile
from urllib.request import Request, urlopen


def git(*args: str) -> bytes:
    return subprocess.check_output(['git', *args])


def select_refs(refs, repository, pulls, releases):
    """A retained remote branch is not evidence that its work is still open."""
    allowed = {'refs/remotes/origin/main', 'refs/remotes/origin/develop'}
    for pull in pulls:
        head = pull.get('head') or {}
        owner = head.get('repo') or {}
        if (pull.get('state') == 'open' and
                owner.get('full_name', '').lower() == repository.lower() and head.get('ref')):
            allowed.add('refs/remotes/origin/' + head['ref'])
    for release in releases:
        if not release.get('draft', True) and release.get('published_at') and release.get('tag_name'):
            allowed.add('refs/tags/' + release['tag_name'])
    return [ref for ref in refs if ref in allowed]


def api_pages(repository, endpoint, fetch_page):
    result = []
    page = 1
    while True:
        items = fetch_page(f'/repos/{repository}/{endpoint}'
                           f'{"&" if "?" in endpoint else "?"}per_page=100&page={page}')
        if not isinstance(items, list):
            raise ValueError('GitHub catalogue endpoint did not return a list')
        result.extend(items)
        if len(items) < 100:
            return result
        page += 1


def github_state(repository):
    token = os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')

    def fetch_page(path):
        headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'ToastNotifications-docs'}
        if token:
            headers['Authorization'] = 'Bearer ' + token
        with urlopen(Request('https://api.github.com' + path, headers=headers), timeout=30) as response:
            return json.load(response)

    return dict(pulls=api_pages(repository, 'pulls?state=open', fetch_page),
                releases=api_pages(repository, 'releases', fetch_page))


def event_state(state, event):
    """Use the triggering state even if the list endpoint briefly lags it."""
    pull = event.get('pull_request')
    if pull:
        state = dict(state, pulls=[p for p in state['pulls'] if p['number'] != pull['number']])
        if pull.get('state') == 'open':
            state['pulls'].append(pull)
    release = event.get('release')
    if release:
        state = dict(state, releases=[r for r in state['releases']
                                     if r.get('id') != release.get('id')])
        if (event.get('action') not in {'deleted', 'unpublished'} and
                not release.get('draft', True) and release.get('published_at')):
            state['releases'].append(release)
    return state


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--repository', default=os.environ.get('GITHUB_REPOSITORY', 'loicwoh/ToastNotifications'))
    parser.add_argument('--github-state', type=Path,
                        help='Offline JSON with pulls/releases arrays instead of querying GitHub')
    args = parser.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', args.repository):
        parser.error('repository must be owner/name')
    state = (json.loads(args.github_state.read_text(encoding='utf-8-sig'))
             if args.github_state else github_state(args.repository))
    if os.environ.get('GITHUB_EVENT_PATH'):
        state = event_state(state, json.loads(Path(os.environ['GITHUB_EVENT_PATH']).read_text(encoding='utf-8')))
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    refs = git('for-each-ref', '--format=%(refname)', 'refs/remotes/origin', 'refs/tags').decode().splitlines()
    refs = select_refs(refs, args.repository, state['pulls'], state['releases'])
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
            legal_files = git('ls-tree', '--name-only', ref, 'LICENSE',
                              'THIRD-PARTY-NOTICES.md').decode().splitlines()
            archive = git('archive', ref, 'Sources', *legal_files)
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
        raise SystemExit('No eligible documentation version contains Sources/docs/site/index.html')
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
        page = '<!doctype html><title>Toast Notifications documentation</title><script>location.replace(' + json.dumps(target) + '+location.hash)</script>'
    else:
        links = ''.join('<li><a href="versions/' + v['id'] + '/">' + html.escape(v['label']) + '</a></li>' for v in versions)
        page = '<!doctype html><html lang="en"><meta charset="utf-8"><title>Toast Notifications documentation versions</title><h1>Toast Notifications documentation</h1><p>Stable documentation has not been released on main yet. Choose a development version:</p><ul>' + links + '</ul></html>'
    (output / 'index.html').write_text(page, encoding='utf-8')
    (output / '.nojekyll').touch()
    print(f'Built {len(versions)} documentation versions.')


if __name__ == '__main__':
    main()
