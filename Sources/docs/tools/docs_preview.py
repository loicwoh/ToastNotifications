"""Stage canonical documentation and preview it under the GitHub project subpath."""
from __future__ import annotations

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import re
import shutil
import hashlib
import json
import sys
from urllib.parse import unquote, urlsplit
sys.path.insert(0, str(Path(__file__).resolve().parent))
from reference_docs import generate_reference

ROOT = Path(__file__).resolve().parents[3]
STAGE = ROOT / '_review' / 'docsify-preview'
SITE = STAGE / 'ToastNotifications'
REQUIRE_HELP_LINKS = False
GUIDES = {
    'xml': ROOT / 'Sources/docs/example-guides/Toast From XML.md',
    'reply': ROOT / 'Sources/docs/example-guides/Reply Input.md',
    'multiple-actions': ROOT / 'Sources/docs/example-guides/Multiple Actions.md',
    'protocol': ROOT / 'Sources/docs/example-guides/Protocol Activation.md',
}


def reference() -> list[str]:
    return generate_reference(ROOT, SITE, REQUIRE_HELP_LINKS)


def stage_legal(root: Path, site: Path) -> None:
    """Publish this version's own licence texts; never invent them for old refs."""
    if not (site / 'licenses.md').is_file():
        return
    required = [root / 'LICENSE', root / 'THIRD-PARTY-NOTICES.md',
                root / 'Sources/third-party-licenses']
    if not all(path.exists() for path in required):
        raise ValueError('Licenses page requires the versioned project licence and third-party texts')
    legal = site / 'legal'
    legal.mkdir()
    shutil.copyfile(required[0], legal / 'toastapi-license.txt')
    shutil.copyfile(required[1], legal / 'third-party-notices.txt')
    shutil.copytree(required[2], legal / 'third-party')


def build() -> None:
    # A clean staging tree prevents deleted methods/pages surviving a rebuild.
    source = (ROOT / 'Sources').resolve()
    target = SITE.resolve()
    if target == ROOT.resolve() or target.is_relative_to(source) or source.is_relative_to(target):
        raise ValueError('Output must not overlap the source tree')
    if SITE.exists():
        shutil.rmtree(target)
    SITE.mkdir(parents=True, exist_ok=True)
    shutil.copytree(ROOT / 'Sources/docs/site', SITE, dirs_exist_ok=True)
    shutil.copytree(ROOT / 'Sources/docs/vendor', SITE / 'vendor', dirs_exist_ok=True)
    stage_legal(ROOT, SITE)
    (SITE / 'guides').mkdir(exist_ok=True)
    for name, source in GUIDES.items():
        # Older published refs predate the XML example. Their navigation must
        # remain buildable by the current catalogue builder.
        if name == 'xml' and not source.is_file():
            continue
        (SITE / 'guides' / f'{name}.md').write_text(source.read_text(encoding='utf-8-sig'), encoding='utf-8')
    routes = reference()
    (SITE / 'reference-routes.js').write_text('window.toastApiReferenceRoutes = ' + json.dumps(routes) + ';\n', encoding='utf-8')
    # Pages/browser caches must not reuse a runtime/configuration from a previous
    # publication while the version manifest points at a new commit.
    revision = hashlib.sha256(b''.join(p.read_bytes() for p in sorted(SITE.rglob('*')) if p.is_file())).hexdigest()[:12]
    with (SITE / 'reference-routes.js').open('a', encoding='utf-8') as config:
        config.write('window.toastApiBuildRevision = ' + json.dumps(revision) + ';\n')
    entry = SITE / 'index.html'
    html = entry.read_text(encoding='utf-8')
    html = re.sub(r'((?:src|href)=["\'])([^"\']+\.(?:js|css))(["\'])', lambda m: m[1] + m[2] + '?v=' + revision + m[3], html)
    entry.write_text(html, encoding='utf-8')
    print(f'Staged site: {SITE}')


def check() -> None:
    failures: list[str] = []
    for page in SITE.rglob('*.md'):
        text = page.read_text(encoding='utf-8-sig')
        links = re.findall(r'!?\[[^\]]*\]\(([^)\s]+)(?:\s+[^)]*)?\)', text)
        links += re.findall(r'href=["\'](#[^"\']*)["\']', text)
        for link in links:
            if link.startswith('#/'):
                link = '/' + link[2:]
            elif link.startswith('#'):
                continue
            if urlsplit(link).scheme or link.startswith('//'):
                continue
            path = unquote(urlsplit(link).path)
            if path == '/':
                target = SITE / 'README.md'
            elif not path:
                continue
            else:
                target = (SITE / path.lstrip('/')) if path.startswith('/') else page.parent / path
                if not target.suffix:
                    target = target.with_suffix('.md')
            if not target.is_file():
                failures.append(f'{page.relative_to(SITE)}: {link}')
    index = (SITE / 'index.html').read_text(encoding='utf-8')
    for asset in re.findall(r'(?:src|href)=["\']([^"\']+)["\']', index):
        if not asset.startswith('#') and not urlsplit(asset).scheme and not (SITE / urlsplit(asset).path).is_file():
            failures.append(f'index.html: {asset}')
    if failures:
        raise SystemExit('Broken local links/assets:\n' + '\n'.join(failures))
    print('Local Markdown routes and entry assets: OK')


def main() -> None:
    global ROOT, STAGE, SITE, GUIDES, REQUIRE_HELP_LINKS
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['build', 'check', 'serve'])
    parser.add_argument('--port', type=int, default=8765)
    parser.add_argument('--source-root', type=Path, default=ROOT)
    parser.add_argument('--output', type=Path, default=SITE)
    parser.add_argument('--require-help-links', action='store_true')
    args = parser.parse_args()
    ROOT = args.source_root.resolve()
    REQUIRE_HELP_LINKS = args.require_help_links
    SITE = args.output.resolve()
    STAGE = SITE.parent
    GUIDES = {name: ROOT / 'Sources/docs/example-guides' / path.name for name, path in GUIDES.items()}
    if args.command in ('build', 'serve'):
        build()
    check()
    if args.command == 'serve':
        handler = partial(SimpleHTTPRequestHandler, directory=str(STAGE))
        server = ThreadingHTTPServer(('127.0.0.1', args.port), handler)
        print(f'Preview: http://127.0.0.1:{args.port}/ToastNotifications/', flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            server.server_close()


if __name__ == '__main__':
    main()
