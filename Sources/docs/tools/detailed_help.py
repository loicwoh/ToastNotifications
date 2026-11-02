"""Join reviewed, authored help to generated summaries without editing either source."""
from pathlib import Path
import hashlib
import json
import re
import shutil

ERROR_BEHAVIORS = {
    'skip': 'Skipped on incoming error.',
    'always': 'Executes even on incoming error.',
}


def load_help(root: Path, site: Path, members: dict[str, str]) -> dict[str, str]:
    """Validate all authored records; return route -> publishable enrichment."""
    directory = root / 'Sources/docs/reference'
    result = {}
    if not directory.exists():
        return result  # Historical refs, before detailed help was introduced.
    markdown = {p.with_suffix('') for p in directory.rglob('*.md')}
    records = {p.with_suffix('') for p in directory.rglob('*.json')}
    if markdown != records:
        raise ValueError('Each detailed help page needs matching .md and .json files')
    for stem in sorted(records):
        route = 'reference/' + stem.relative_to(directory).as_posix()
        record = json.loads(stem.with_suffix('.json').read_text(encoding='utf-8'))
        if record.get('schema_version') != 1:
            raise ValueError(f'Unsupported detailed help schema: {route}')
        if route not in members or record.get('source') != members[route]:
            raise ValueError(f'Orphaned or mismatched detailed help: {route}')
        reviewed = record['reviewed_files']
        if record['source'] not in reviewed or not reviewed:
            raise ValueError(f'Missing reviewed VI fingerprint: {route}')
        for name, expected in reviewed.items():
            path = (root / name).resolve()
            if not path.is_relative_to((root / 'Sources').resolve()) or not path.is_file():
                raise ValueError(f'Invalid reviewed source: {name}')
            if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
                raise ValueError(f'Stale detailed help: {route}; review {name} before updating its fingerprint')
        visual = (directory / record['visual']).resolve()
        if visual.parent != stem.parent.resolve() or visual.suffix not in {'.png', '.svg'} or not visual.is_file():
            raise ValueError(f'Missing or invalid detailed help visual: {route}')
        if record.get('visual_sha256') and hashlib.sha256(visual.read_bytes()).hexdigest() != record['visual_sha256']:
            raise ValueError(f'Changed detailed help visual: {route}; review capture provenance')
        behavior = record.get('error_behavior')
        if behavior not in ERROR_BEHAVIORS:
            raise ValueError(f'Choose skip or always error_behavior: {route}')
        content = stem.with_suffix('.md').read_text(encoding='utf-8')
        if re.search(r'^# ', content, re.MULTILINE):
            raise ValueError(f'Detailed help enrichment must start at H2: {route}')
        visual_route = 'reference/' + visual.relative_to(directory.resolve()).as_posix()
        visual_link = visual.relative_to(stem.parent.resolve()).as_posix()
        if f']({visual_link})' not in content:
            raise ValueError(f'Detailed help must link its reviewed visual: {route}')
        destination = site / visual_route
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(visual, destination)
        # Technical review evidence remains in the versioned JSON, out of reader-facing help.
        result[route] = f'**Error behavior: {ERROR_BEHAVIORS[behavior]}**\n\n' + content.rstrip() + '\n'
    return result
