"""Assemble owner pages and reference links around the existing saved VI help."""
from pathlib import Path
import hashlib
import html
import json
from api_inventory import inventory, slug
from vi_descriptions import description, resource
from detailed_help import load_help

GUIDE_LABELS = {'reply': 'Receive a text reply', 'multiple-actions': 'Handle multiple actions',
                'protocol': 'Open a link'}
FAMILIES = {'toolkit': ('T', 'Windows notifications for LabVIEW'),
            'builder': ('B', 'Compose content'), 'service': ('S', 'Display and lifecycle'),
            'handler': ('H', 'React to activation')}


def generate_reference(root: Path, site: Path, require_help: bool) -> list[str]:
    owners = inventory(root)
    by_id = {o.id: o for o in owners}
    authored = load_help(root, site, {
        f'reference/{o.config.get("reference_prefix", o.id)}/{slug(m.path.stem)}': m.path.relative_to(root).as_posix()
        for o in owners for m in o.members})
    links, routes, breadcrumbs = [], ['/reference'], {}
    index = ['# VI and data type reference', '',
             '[API overview](/api.md) · [Choose an example](/examples.md)', '',
             'Names, ownership, scope and saved descriptions are generated from the versioned sources. '
             'This index includes application methods, extension points and low-level helpers. '
             'Technical Public scope does not establish a release support guarantee.', '',
             'Start with the [owner pages](/api.md) to choose the appropriate layer. '
             'Entries marked **Detailed help** add a native help image, terminals and usage scenario. '
             'Other entries contain the short description only; consult LabVIEW Context Help for their connectors.', '']

    def breadcrumb(owner, member=None):
        crumbs = [('API', '/api')]
        if owner.parent:
            parent = by_id[owner.parent]
            crumbs.append((parent.label, '/api/' + parent.id))
        crumbs.append((owner.label, '/api/' + owner.id if member else None))
        if member:
            crumbs.append((member.path.stem, None))
        family = owner.config.get('visual_family', 'toolkit')
        if family not in FAMILIES:
            raise ValueError(f'Unknown visual family: {family}')
        symbol, purpose = FAMILIES[family]
        banner = (f'<div class="module-banner family-{family}"><span class="module-symbol" aria-hidden="true">{symbol}</span>'
                  f'<span><strong>{html.escape(owner.label)}</strong><small>{purpose}</small></span>'
                  f'<span class="module-kind">{owner.kind}</span></div>')
        nav = '<nav aria-label="Breadcrumb">' + ' / '.join(
            '<a href="#' + url + '">' + html.escape(label) + '</a>' if url else html.escape(label)
            for label, url in crumbs) + '</nav>'
        # Historical versions retain their own presentation assets.
        return nav + banner if (site / 'assets/identity.css').is_file() else nav

    def related(owner):
        items = []
        if owner.config.get('concept'):
            items.append(f'[Related concept or ownership contract](/{owner.config["concept"]})')
        items += [f'[{GUIDE_LABELS[g]}](/guides/{g}.md)' for g in owner.config.get('examples', [])]
        return ' · '.join(items)

    for owner in owners:
        routes.append('/api/' + owner.id)
        index += [f'## {owner.label}', '', f'[Role, dependencies and members](/api/{owner.id}.md)', '']
        rows, reference_rows = [], []
        for member in owner.members:
            name = member.path.stem
            prefix = owner.config.get('reference_prefix', owner.id)
            route = f'reference/{prefix}/{slug(name)}'
            routes.append('/' + route)
            source = member.path.relative_to(root).as_posix()
            body = description(member.path)
            needs_help = owner.kind == 'Class' and member.path.suffix == '.vi'
            if not body.strip():
                if require_help and needs_help:
                    raise ValueError(f'Missing public VI description: {source}')
                body = 'No description is recorded in this saved file. Consult the owner page for its role and limitations.'
            if require_help and needs_help:
                expected = ('https://loicwoh.github.io/ToastNotifications/#/' + route).encode('ascii')
                if resource(member.path, b'HLPW') != len(expected).to_bytes(4, 'big') + expected or resource(member.path, b'HLPU') != b'\x01\x00\x00\x00':
                    raise ValueError(f'Missing or outdated detailed help URL: {source}')
            if needs_help:
                # Preserve the existing 23-entry maintenance contract. New helper
                # reference pages do not require saving their VIs to add URLs.
                links.append(dict(source=source, route='#/' + route))
            title = name + (' (data type)' if member.path.suffix == '.ctl' else '')
            note = ''
            if member.role == 'Native reference access':
                note = ('This technically public accessor exposes implementation-level reference access. '
                        'Prefer the application workflow on the owner page; copying a handle does not transfer ownership.\n\n')
            breadcrumbs['/' + route] = breadcrumb(owner, member)
            page = f'# {owner.label}: {title}\n\n'
            page += f'Layer: {owner.category} · Kind: {member.role} · Saved scope: {member.scope}\n\n'
            page += ('' if route in authored
                     else '**Short description only** — a full usage walkthrough is not yet authored.\n\n')
            page += '## Short description\n\n' + note + body + '\n\n'
            if route in authored:
                page += authored[route] + '\n'
            page += f'[Back to {owner.label}](/api/{owner.id}.md) · [Reference index](/reference.md)\n\n'
            if related(owner):
                page += '## Related owner workflows\n\n' + related(owner) + '\n\n'
                page += 'These guides explain workflows involving this owner; they do not validate every helper listed here.\n\n'
            page += f'**Source:** `{source}`\n\n<!-- VI SHA-256: {hashlib.sha256(member.path.read_bytes()).hexdigest()} -->\n'
            destination = site / (route + '.md')
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(page, encoding='utf-8')
            row = f'| [{title}](/{route}.md) | {member.role} | {member.scope} |'
            (reference_rows if member.role == 'Native reference access' else rows).append(row)
            help_label = ' · **Detailed help**' if route in authored else ''
            index.append(f'- [{title}](/{route}.md) — {member.role}{help_label}')

        generated = f'**Kind:** {owner.kind} · **Layer:** {owner.category}\n\n'
        if owner.children:
            generated += '## Contained libraries and classes\n\n'
            generated += '\n'.join(f'- [{by_id[c].label}](/api/{c}.md) — {by_id[c].category}' for c in owner.children) + '\n\n'
        generated += '## Public members\n\nThe list follows the saved owner XML and effective item scope.\n\n'
        generated += '| Member | Role | Scope |\n|---|---|---|\n' + '\n'.join(rows) + '\n\n'
        if reference_rows:
            generated += '## Native reference accessors\n\nThese entries remain technically public; listing them does not recommend native-handle manipulation in application code.\n\n'
            generated += '| Member | Role | Scope |\n|---|---|---|\n' + '\n'.join(reference_rows) + '\n\n'
        if related(owner):
            generated += '## Concepts and examples\n\n' + related(owner) + '\n\n'
        generated += f'**Owner file:** `{owner.path.relative_to(root).as_posix()}`\n'
        destination = site / 'api' / (owner.id + '.md')
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.exists():
            content = destination.read_text(encoding='utf-8')
            if content.count('<!-- API-MEMBERS -->') != 1:
                raise ValueError(f'Expected one API-MEMBERS marker: {destination}')
            content = content.replace('<!-- API-MEMBERS -->', generated)
        else:
            # Compatibility for published refs that predate authored owner pages.
            content = f'# {owner.label}\n\nMembers discovered from the saved owner file.\n\n' + generated
        breadcrumbs['/api/' + owner.id] = breadcrumb(owner)
        destination.write_text(content, encoding='utf-8')
        index.append('')

    for guide, label in GUIDE_LABELS.items():
        path = site / 'guides' / (guide + '.md')
        if not path.exists():
            continue
        content = path.read_text(encoding='utf-8')
        breadcrumbs['/guides/' + guide] = '<nav aria-label="Breadcrumb"><a href="#/examples">Examples</a> / ' + html.escape(label) + '</nav>'
        owner_links = [f'[{o.label}](/api/{o.id}.md)' for o in owners if guide in o.config.get('examples', [])]
        footer = '\n\n## Related API owners\n\n' + ' · '.join(owner_links) if owner_links else ''
        path.write_text(content + footer + '\n\n[Back to all examples](/examples.md)\n', encoding='utf-8')
    (site / 'reference.md').write_text('\n'.join(index), encoding='utf-8')
    (site / 'api-links.json').write_text(json.dumps(links, indent=2), encoding='utf-8')
    (site / 'navigation.js').write_text('window.toastApiBreadcrumbs = ' + json.dumps(breadcrumbs) + ';\n', encoding='utf-8')
    (site / 'api-inventory.json').write_text(json.dumps([
        dict(source=o.path.relative_to(root).as_posix(), id=o.id, kind=o.kind, category=o.category,
             members=[dict(source=m.path.relative_to(root).as_posix(), scope=m.scope, role=m.role) for m in o.members])
        for o in owners], indent=2), encoding='utf-8')
    return routes
