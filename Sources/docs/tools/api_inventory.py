"""Read LabVIEW owner XML for documentation; never load or write VIs."""
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import unquote, urlsplit
import json
import re


SCOPES = {1: 'Public', 2: 'Private', 3: 'Protected', 4: 'Community'}


def slug(value: str) -> str:
    return re.sub(r'[^a-z0-9]+', '-', value.lower()).strip('-')


def item_path(root: Path, owner: Path, url: str) -> Path:
    """LabVIEW member URLs may be relative to the container or its directory.

    Resolve actual files, not Item.Name: flat class members commonly use ../VI.vi,
    while private-data controls use Control.ctl. Refuse missing/ambiguous links.
    """
    if urlsplit(url).scheme or not url:
        raise ValueError(f'Unsupported owner URL in {owner}: {url}')
    candidates = {(base / unquote(url)).resolve() for base in (owner, owner.parent)}
    matches = [p for p in candidates if p.is_file() and p.is_relative_to(root / 'Sources')]
    if len(matches) != 1:
        raise ValueError(f'Missing or ambiguous owner URL in {owner}: {url}')
    return matches[0]


@dataclass
class Member:
    path: Path
    scope: str
    property: bool
    role: str


@dataclass
class Owner:
    path: Path
    id: str
    label: str
    kind: str
    category: str
    parent: str | None
    config: dict
    members: list[Member] = field(default_factory=list)
    children: list[str] = field(default_factory=list)


def inventory(root: Path) -> list[Owner]:
    import xml.etree.ElementTree as ET
    root = root.resolve()
    mapping = root / 'Sources/docs/api-map.json'
    # Older published refs predate this map. Keep their original VI routes and
    # generate minimal owner pages instead of requiring new authored files there.
    config = json.loads(mapping.read_text(encoding='utf-8')) if mapping.exists() else {}
    owner_config = config.get('owners', {})
    entry = root / config.get('root', 'Sources/ToastNotification/ToastNotification.lvlib')
    if not entry.resolve().is_relative_to(root / 'Sources') or entry.suffix != '.lvlib':
        raise ValueError('The documentation root must be a library inside Sources')
    owners: dict[Path, Owner] = {}
    routes: set[str] = set()

    def visit(path: Path, parent: str | None = None) -> Owner:
        if path in owners:
            return owners[path]
        relative = path.relative_to(root).as_posix()
        if mapping.exists() and relative not in owner_config:
            raise ValueError(f'Classify the new documentation owner in api-map.json: {relative}')
        options = owner_config.get(relative, {})
        id_ = options.get('id', slug(path.stem))
        prefix = options.get('reference_prefix', id_)
        if not all(re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', s) for s in (id_, prefix)):
            raise ValueError(f'Invalid documentation route ID: {relative}')
        route = 'api/' + id_
        if route in routes:
            raise ValueError(f'Duplicate documentation route: {route}')
        routes.add(route)
        owner = Owner(path, id_, path.stem, 'Class' if path.suffix == '.lvclass' else 'Library',
                      options.get('category', 'Unclassified'), parent, options)
        owners[path] = owner

        def walk(element, inherited=1, property_member=False):
            for item in element.findall('Item'):
                scope = int(item.findtext("Property[@Name='NI.ClassItem.MethodScope']")
                            or item.findtext("Property[@Name='NI.LibItem.Scope']") or inherited)
                if scope not in SCOPES:
                    raise ValueError(f'Unknown scope {scope}: {relative}/{item.get("Name")}')
                kind = item.get('Type')
                is_property = property_member or kind == 'Property Definition'
                if kind in ('Library', 'LVClass'):
                    if scope != 1:
                        continue
                    child = visit(item_path(root, path, item.get('URL', '')), id_)
                    owner.children.append(child.id)
                elif kind == 'VI' and scope == 1:
                    member_path = item_path(root, path, item.get('URL', ''))
                    if member_path.suffix.lower() not in ('.vi', '.ctl'):
                        continue
                    prefix = options.get('reference_prefix', id_)
                    member_route = f'reference/{prefix}/{slug(member_path.stem)}'
                    if member_route in routes:
                        raise ValueError(f'Duplicate documentation route: {member_route}')
                    routes.add(member_route)
                    if member_path.suffix.lower() == '.ctl':
                        role = 'Data type'
                    elif member_path.name in options.get('native_accessors', []):
                        role = 'Native reference access'
                    elif is_property:
                        role = 'Property accessor'
                    else:
                        role = 'Method' if owner.kind == 'Class' else 'Helper VI'
                    owner.members.append(Member(member_path, SCOPES[scope], is_property, role))
                walk(item, scope, is_property)

        walk(ET.parse(path).getroot())
        return owner

    visit(entry.resolve())
    missing = set(owner_config) - {p.relative_to(root).as_posix() for p in owners}
    if missing:
        raise ValueError(f'Documentation owners absent from the root library: {sorted(missing)}')
    return list(owners.values())
