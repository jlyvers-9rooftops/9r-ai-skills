#!/usr/bin/env python3
"""Check the PPTX package, slide count, editable text, sources, and shape bounds."""
from pathlib import Path
from zipfile import ZipFile
import argparse
import json
import posixpath
import re
import xml.etree.ElementTree as ET

NS = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
      'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}


def validate(path, library=False):
    errors, warnings = [], []
    with ZipFile(path) as archive:
        names = set(archive.namelist())
        bad = archive.testzip()
        if bad:
            errors.append(f'Bad ZIP member: {bad}')
        trees = {}
        for name in names:
            if name.endswith(('.xml', '.rels')):
                try:
                    trees[name] = ET.fromstring(archive.read(name))
                except ET.ParseError as exc:
                    errors.append(f'{name}: invalid XML: {exc}')
        for name, tree in trees.items():
            if not name.endswith('.rels'):
                continue
            base = '' if name == '_rels/.rels' else posixpath.dirname(posixpath.dirname(name))
            ids = [r.get('Id') for r in tree]
            if len(ids) != len(set(ids)):
                errors.append(f'{name}: duplicate relationship IDs')
            for rel in tree:
                if rel.get('TargetMode') == 'External':
                    continue
                target = rel.get('Target', '')
                resolved = target.lstrip('/') if target.startswith('/') else posixpath.normpath(posixpath.join(base, target))
                if resolved not in names:
                    errors.append(f'{name}: missing relationship target {resolved}')
        pres = trees.get('ppt/presentation.xml')
        if pres is None:
            return {'ok': False, 'errors': errors + ['Missing presentation.xml'], 'warnings': warnings}
        ids = pres.findall('p:sldIdLst/p:sldId', NS)
        slides = sorted(n for n in names if re.fullmatch(r'ppt/slides/slide\d+.xml', n))
        if len(ids) != len(slides):
            errors.append('Slide list and package slide count differ')
        maximum = 8 if library else 5
        if not 1 <= len(ids) <= maximum:
            errors.append(f'Expected 1–{maximum} slides; found {len(ids)}')
        size = pres.find('p:sldSz', NS)
        width, height = int(size.get('cx')), int(size.get('cy'))
        if abs(width / height - 16 / 9) > .001:
            errors.append('Slide size must be 16:9')
        fonts, slide_text = set(), []
        for name in slides:
            tree = trees.get(name)
            if tree is None:
                continue
            text = '\n'.join(t.text or '' for t in tree.findall('.//a:t', NS))
            slide_text.append(text)
            if not text.strip():
                errors.append(f'{name}: no editable slide text')
            if not library and re.search(r'\{\{.+?\}\}|\bLorem ipsum\b|\[(?:CLIENT_NAME|CAMPAIGN_NAME|TODO|TBD)', text, re.I):
                errors.append(f'{name}: unresolved placeholder or filler')
            for font in tree.findall('.//a:latin', NS):
                fonts.add(font.get('typeface'))
            for shape in list(tree.findall('.//p:spTree/p:sp', NS)) + list(tree.findall('.//p:spTree/p:pic', NS)):
                xfrm = shape.find('p:spPr/a:xfrm', NS)
                if xfrm is None:
                    continue
                off, ext = xfrm.find('a:off', NS), xfrm.find('a:ext', NS)
                if off is None or ext is None:
                    continue
                x, y, w, h = int(off.get('x')), int(off.get('y')), int(ext.get('cx')), int(ext.get('cy'))
                if x < -9144 or y < -9144 or x + w > width + 9144 or y + h > height + 9144:
                    errors.append(f'{name}: shape outside slide bounds')
                if shape.tag.endswith('}pic') and w > width * .8 and h > height * .8:
                    errors.append(f'{name}: full-slide bitmap; editable layouts are required')
        if not {'Georgia', 'Calibri'}.issubset(fonts):
            warnings.append('Expected Georgia headlines and Calibri body text were not both found')
        if not library:
            notes = [trees[n] for n in names if re.fullmatch(r'ppt/notesSlides/notesSlide\d+.xml', n) and n in trees]
            if len(notes) != len(slides) or any('Sources:' not in '\n'.join(t.text or '' for t in note.findall('.//a:t', NS)) for note in notes):
                errors.append('Each slide must include source references in speaker notes')
        warnings.append('Structural checks do not prove text fit, source accuracy, icon rendering, or font availability. Inspect a native PowerPoint/PDF render before calling the deck final.')
    return {'ok': not errors, 'file': str(path), 'slides': len(slides), 'fonts': sorted(fonts), 'errors': errors, 'warnings': warnings}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('deck', type=Path)
    parser.add_argument('--library', action='store_true', help='Validate the eight-layout asset, not a final deck')
    args = parser.parse_args()
    try:
        result = validate(args.deck, args.library)
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(1, f'Cannot validate deck: {exc}\n')
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result['ok'] else 1)


if __name__ == '__main__':
    main()
