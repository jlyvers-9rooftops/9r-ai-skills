#!/usr/bin/env python3
"""Check local marketplace paths and package structure without dependencies."""
import json
from pathlib import Path
import re
import sys


def validate(root):
    catalog = json.loads((root / '.agents/plugins/marketplace.json').read_text())
    assert re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', catalog['name']), 'Invalid marketplace name'
    assert catalog['plugins'], 'Marketplace has no plugins'
    names = set()
    for entry in catalog['plugins']:
        name = entry['name']
        assert name not in names, f'Duplicate plugin: {name}'
        names.add(name)
        assert entry['policy']['installation'] in {'AVAILABLE', 'INSTALLED_BY_DEFAULT', 'NOT_AVAILABLE'}
        assert entry['policy']['authentication'] in {'ON_INSTALL', 'ON_USE'}
        assert entry['category'], f'Missing category: {name}'
        source = entry['source']
        assert source['source'] == 'local', 'This validator supports local sources only'
        assert source['path'].startswith('./'), f'Path must start with ./: {name}'
        plugin = (root / source['path']).resolve()
        assert plugin.is_relative_to(root), f'Path escapes repository: {name}'
        assert plugin.is_dir(), f'Plugin not found: {name}'
        for path in plugin.rglob('*'):
            assert not path.is_symlink(), f'Unsupported package symlink: {path}'
            assert path.is_file() or path.is_dir(), f'Unsupported package entry: {path}'
            assert path.name not in {'node_modules', '.venv', '__pycache__'}, f'Runtime files in package: {path}'
        manifest = json.loads((plugin / 'plugin.json').read_text())
        assert manifest['name'] == name, f'Plugin name mismatch: {name}'
        assert re.fullmatch(r'\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?', manifest['version']), f'Invalid version: {name}'
        assert manifest['description'].strip(), f'Missing description: {name}'
        skills = list((plugin / 'skills').glob('*/SKILL.md'))
        assert skills, f'No skills packaged: {name}'
        for skill in skills:
            text = skill.read_text()
            assert text.startswith('---\n'), f'Missing frontmatter: {skill}'
            parts = text.split('---', 2)
            assert len(parts) == 3 and parts[2].strip(), f'Missing skill body: {skill}'
            frontmatter = parts[1]
            match = re.search(r'^name:\s*([a-z0-9-]+)\s*$', frontmatter, re.M)
            assert match and match[1] == skill.parent.name, f'Skill name/folder mismatch: {skill}'
            assert re.search(r'^description:\s*\S', frontmatter, re.M), f'Missing description: {skill}'
        print(f'OK {name} {manifest["version"]}: {len(skills)} skill(s)')
    print(f'Marketplace {catalog["name"]}: {len(names)} plugin(s) validated')
    print('Structural checks only; run skills in the target client before release.')


if __name__ == '__main__':
    try:
        validate(Path(__file__).resolve().parents[1])
    except (AssertionError, KeyError, OSError, ValueError) as exc:
        print(f'Validation failed: {exc}', file=sys.stderr)
        sys.exit(1)
