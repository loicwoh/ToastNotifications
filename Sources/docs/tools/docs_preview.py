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
import xml.etree.ElementTree as ET
import sys
from urllib.parse import unquote, urlsplit
sys.path.insert(0, str(Path(__file__).resolve().parent))
from vi_descriptions import description, resource

ROOT = Path(__file__).resolve().parents[3]
STAGE = ROOT / '_review' / 'docsify-preview'
SITE = STAGE / 'ToastNotifications'
REQUIRE_HELP_LINKS = False
GUIDES = {
    'reply': ROOT / 'Sources/Examples/Reply Input.md',
    'multiple-actions': ROOT / 'Sources/Examples/Multiple Actions.md',
    'protocol': ROOT / 'Sources/Examples/Protocol Activation.md',
}


def slug(value: str) -> str:
    return re.sub(r'[^a-z0-9]+', '-', value.lower()).strip('-')


def reference() -> list[str]:
    routes = []
    links = []
    index = ['# VI reference', '', 'Generated from saved VI descriptions and class membership at build time.',
             'Edit context help in LabVIEW and save the VI to update these pages.', '',
             'Connector terminal details remain available in LabVIEW Context Help.', '']
    owners = ['Sources/ToastBuilder/ToastBuilder.lvclass',
              'Sources/ToastService/ToastService.lvclass',
              'Sources/ActivationHandler/ActivationHandler.lvclass',
              'Sources/PlugIns/UserEventActivationHandler/UserEventActivationHandler.lvclass']
    for relative in owners:
        owner = ROOT / relative
        tree = ET.parse(owner)
        index += [f'## {owner.stem}', '']
        for item in tree.iter('Item'):
            if item.get('Type') != 'VI' or not item.get('Name', '').endswith('.vi'):
                continue
            scope = item.find("Property[@Name='NI.ClassItem.MethodScope']")
            if scope is None or scope.text != '1':
                continue
            path = owner.parent / item.get('Name')
            name = path.stem
            route = f'reference/{slug(owner.stem)}/{slug(name)}'
            destination = SITE / (route + '.md')
            destination.parent.mkdir(parents=True, exist_ok=True)
            source = path.relative_to(ROOT).as_posix()
            body = description(path)
            if not body.strip():
                if REQUIRE_HELP_LINKS:
                    raise ValueError(f'Missing public VI description: {source}')
                print(f'Warning: missing public VI description: {source}')
                body = 'Context help has not been documented for this VI yet.'
            if REQUIRE_HELP_LINKS:
                expected = ('https://loicwoh.github.io/ToastNotifications/#/' + route).encode('ascii')
                raw = resource(path, b'HLPW')
                if raw != len(expected).to_bytes(4, 'big') + expected or resource(path, b'HLPU') != b'\x01\x00\x00\x00':
                    raise ValueError(f'Missing or outdated detailed help URL: {source}. Run Sync-DetailedHelp.ps1 after a normal build.')
            destination.write_text(f'# {owner.stem}: {name}\n\n{body}\n\n'
                                   f'**Source:** `{source}`\n\n'
                                   f'<!-- VI SHA-256: {hashlib.sha256(path.read_bytes()).hexdigest()} -->\n', encoding='utf-8')
            index.append(f'- [{name}](/{route}.md)')
            routes.append('/' + route)
            links.append(dict(source=source, route='#/' + route))
        index.append('')
    (SITE / 'reference.md').write_text('\n'.join(index), encoding='utf-8')
    (SITE / 'api-links.json').write_text(json.dumps(links, indent=2), encoding='utf-8')
    return ['/reference', *routes]


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
    (SITE / 'guides').mkdir(exist_ok=True)
    for name, source in GUIDES.items():
        (SITE / 'guides' / f'{name}.md').write_text(source.read_text(encoding='utf-8-sig'), encoding='utf-8')
    routes = reference()
    (SITE / 'reference-routes.js').write_text('window.toastApiReferenceRoutes = ' + json.dumps(routes) + ';\n', encoding='utf-8')
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
        if not asset.startswith('#') and not urlsplit(asset).scheme and not (SITE / asset).is_file():
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
    GUIDES = {name: ROOT / 'Sources/Examples' / path.name for name, path in GUIDES.items()}
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
