#!/usr/bin/env python3
"""Check Codex, Grok, and Claude marketplace catalogs without dependencies."""
import json
from pathlib import Path
import re
import sys


NAME = re.compile(r'[a-z0-9]+(?:-[a-z0-9]+)*')
VERSION = re.compile(r'\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?')


def load_json(path):
    try:
        return json.loads(path.read_text())
    except FileNotFoundError as exc:
        raise AssertionError(f'Missing {path}') from exc


def skill_description(skill):
    text = skill.read_text()
    assert text.startswith('---\n'), f'Missing frontmatter: {skill}'
    parts = text.split('---', 2)
    assert len(parts) == 3 and parts[2].strip(), f'Missing skill body: {skill}'
    frontmatter = parts[1]
    match = re.search(r'^name:\s*([a-z0-9-]+)\s*$', frontmatter, re.M)
    assert match and match[1] == skill.parent.name, f'Skill name/folder mismatch: {skill}'
    description = re.search(r'^description:\s*(.+)$', frontmatter, re.M)
    assert description, f'Missing description: {skill}'
    return match[1], description[1].strip()


def plugin_skills(plugin):
    skills = sorted((plugin / 'skills').glob('*/SKILL.md'))
    assert skills, f'No skills packaged: {plugin.name}'
    return {name: description for name, description in (skill_description(skill) for skill in skills)}


def local_path(entry, client):
    source = entry['source']
    if client == 'claude':
        assert isinstance(source, str), f'{entry["name"]}: Claude source must be a relative path string'
        return source
    assert isinstance(source, dict), f'{entry["name"]}: {client} source must be an object'
    if client == 'grok':
        assert source.get('type') == 'local', f'{entry["name"]}: Grok source type must be local'
    else:
        assert source.get('source') == 'local', f'{entry["name"]}: Codex source must be local'
    return source['path']


def catalog_entries(catalog, client):
    assert catalog['plugins'], f'{client} marketplace has no plugins'
    entries = {}
    for entry in catalog['plugins']:
        name = entry['name']
        assert NAME.fullmatch(name), f'Invalid plugin name: {name}'
        assert name not in entries, f'Duplicate {client} plugin: {name}'
        path = local_path(entry, client)
        assert path.startswith('./'), f'Path must start with ./: {name}'
        assert '..' not in Path(path).parts, f'Path must stay inside the repository: {name}'
        entries[name] = path
    return entries


def validate(root):
    codex = load_json(root / '.agents/plugins/marketplace.json')
    grok = load_json(root / '.grok-plugin/marketplace.json')
    claude = load_json(root / '.claude-plugin/marketplace.json')
    index = load_json(root / '.grok-plugin/plugin-index.json')

    for catalog in (codex, grok, claude):
        assert NAME.fullmatch(catalog['name']), 'Invalid marketplace name'
        assert catalog['name'] == '9r-ai-skills', 'Marketplace name must stay 9r-ai-skills'
    assert grok['owner']['name'].strip() and claude['owner']['name'].strip(), 'Missing marketplace owner'
    assert index.get('version') == 1, 'plugin-index.json version must be 1'

    codex_entries = catalog_entries(codex, 'codex')
    grok_entries = catalog_entries(grok, 'grok')
    claude_entries = catalog_entries(claude, 'claude')
    assert codex_entries == grok_entries == claude_entries, 'Marketplace catalogs list different plugins'

    for entry in codex['plugins']:
        assert entry['policy']['installation'] in {'AVAILABLE', 'INSTALLED_BY_DEFAULT', 'NOT_AVAILABLE'}
        assert entry['policy']['authentication'] in {'ON_INSTALL', 'ON_USE'}
        assert entry['category'], f'Missing Codex category: {entry["name"]}'

    packaged = {}
    plugin_root = root / 'plugins'
    assert plugin_root.is_dir(), 'Missing plugins directory'
    for plugin in sorted(path for path in plugin_root.iterdir() if path.is_dir()):
        for path in plugin.rglob('*'):
            assert not path.is_symlink(), f'Unsupported package symlink: {path}'
            assert path.is_file() or path.is_dir(), f'Unsupported package entry: {path}'
            assert path.name not in {'node_modules', '.venv', '__pycache__'}, f'Runtime files in package: {path}'
        manifest = load_json(plugin / 'plugin.json')
        claude_manifest = load_json(plugin / '.claude-plugin/plugin.json')
        name = plugin.name
        assert manifest['name'] == name, f'Plugin name mismatch: {name}'
        assert claude_manifest['name'] == name, f'Claude manifest name mismatch: {name}'
        assert VERSION.fullmatch(manifest['version']), f'Invalid version: {name}'
        assert claude_manifest['version'] == manifest['version'], f'Version mismatch: {name}'
        assert manifest['description'].strip(), f'Missing description: {name}'
        assert claude_manifest['description'] == manifest['description'], f'Description mismatch: {name}'
        packaged[name] = plugin_skills(plugin)

    loose_skills = []
    for path in root.rglob('SKILL.md'):
        if '.git' in path.relative_to(root).parts:
            continue
        parts = path.relative_to(root).parts
        if not (len(parts) == 5 and parts[0] == 'plugins' and parts[2] == 'skills'):
            loose_skills.append(str(path.relative_to(root)))
    assert not loose_skills, f'Skills must live in plugins/<plugin>/skills/<skill>/SKILL.md: {loose_skills}'
    assert set(packaged) == set(codex_entries), 'A plugin directory is missing from the marketplaces'

    indexed = index['plugins']
    assert set(indexed) == set(packaged), 'plugin-index.json does not match the packaged plugins'
    for name, skills in packaged.items():
        path = (root / codex_entries[name]).resolve()
        assert path == (root / 'plugins' / name).resolve(), f'Catalog path mismatch: {name}'
        assert path.is_relative_to(root), f'Path escapes repository: {name}'
        listed = {
            item['name']: item['description']
            for item in indexed[name]['components']['skills']
        }
        assert listed == skills, f'Skill catalog mismatch: {name}'
        print(f'OK {name} {load_json(path / "plugin.json")["version"]}: {len(skills)} skill(s)')

    print(f'Marketplace {codex["name"]}: {len(packaged)} plugin(s) in Codex, Grok, and Claude')
    print('Structural checks only; run skills in the target client before release.')


if __name__ == '__main__':
    try:
        validate(Path(__file__).resolve().parents[1])
    except (AssertionError, KeyError, OSError, ValueError) as exc:
        print(f'Validation failed: {exc}', file=sys.stderr)
        sys.exit(1)
