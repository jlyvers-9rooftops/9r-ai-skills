#!/usr/bin/env python3
"""Fill the packaged native layouts. Python standard library; no third-party runtime."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from copy import deepcopy
import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET

BASE = Path(__file__).resolve().parents[1]
NS = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
      'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
for prefix, uri in NS.items():
    ET.register_namespace(prefix, uri)
EMU = 914400


def set_text(shape, text):
    body = shape.find('p:txBody', NS)
    original = body.find('a:p', NS)
    for paragraph in body.findall('a:p', NS):
        body.remove(paragraph)
    for line in text.split('\n'):
        paragraph = deepcopy(original)
        for child in list(paragraph):
            if child.tag not in [f'{{{NS["a"]}}}pPr', f'{{{NS["a"]}}}endParaRPr']:
                paragraph.remove(child)
        run = deepcopy(original.find('a:r', NS))
        if run is None:
            run = ET.Element(f'{{{NS["a"]}}}r')
            ET.SubElement(run, f'{{{NS["a"]}}}t')
        run.find('a:t', NS).text = line
        paragraph.insert(1 if paragraph.find('a:pPr', NS) is not None else 0, run)
        body.append(paragraph)


def footer(tree, text, muted):
    """Add a small editable source line when a non-results layout is repurposed."""
    sp = ET.SubElement(tree.find('p:cSld/p:spTree', NS), f'{{{NS["p"]}}}sp')
    nv = ET.SubElement(sp, f'{{{NS["p"]}}}nvSpPr')
    ET.SubElement(nv, f'{{{NS["p"]}}}cNvPr', {'id': '9001', 'name': 'case.source_line'})
    ET.SubElement(nv, f'{{{NS["p"]}}}cNvSpPr', {'txBox': '1'})
    ET.SubElement(nv, f'{{{NS["p"]}}}nvPr')
    props = ET.SubElement(sp, f'{{{NS["p"]}}}spPr')
    xfrm = ET.SubElement(props, f'{{{NS["a"]}}}xfrm')
    ET.SubElement(xfrm, f'{{{NS["a"]}}}off', {'x': str(round(.6 * EMU)), 'y': str(round(7.12 * EMU))})
    ET.SubElement(xfrm, f'{{{NS["a"]}}}ext', {'cx': str(12 * EMU), 'cy': str(round(.25 * EMU))})
    ET.SubElement(props, f'{{{NS["a"]}}}noFill')
    body = ET.SubElement(sp, f'{{{NS["p"]}}}txBody')
    ET.SubElement(body, f'{{{NS["a"]}}}bodyPr', {'lIns': '0', 'rIns': '0', 'tIns': '0', 'bIns': '0'})
    ET.SubElement(body, f'{{{NS["a"]}}}lstStyle')
    para = ET.SubElement(body, f'{{{NS["a"]}}}p')
    run = ET.SubElement(para, f'{{{NS["a"]}}}r')
    rp = ET.SubElement(run, f'{{{NS["a"]}}}rPr', {'sz': '1000'})
    fill = ET.SubElement(rp, f'{{{NS["a"]}}}solidFill')
    ET.SubElement(fill, f'{{{NS["a"]}}}srgbClr', {'val': muted})
    ET.SubElement(rp, f'{{{NS["a"]}}}latin', {'typeface': 'Calibri'})
    ET.SubElement(run, f'{{{NS["a"]}}}t').text = text


def build(spec, output):
    library = json.loads((BASE / 'assets/layouts.json').read_text())
    if not isinstance(spec, dict) or set(spec) - {'palette', 'sources', 'slides'}:
        raise ValueError('Use a spec object with palette, sources, and slides only.')
    slides = spec.get('slides')
    if not isinstance(slides, list) or not 1 <= len(slides) <= 5:
        raise ValueError('A finished case study must contain one to five slides.')
    palette = spec.get('palette', {})
    if set(palette) != set(library['palette']):
        raise ValueError('Supply all eight palette roles listed in assets/layouts.json.')
    if any(not isinstance(c, str) or not re.fullmatch(r'[0-9A-Fa-f]{6}', c) for c in palette.values()):
        raise ValueError('Palette values must be six-digit hex strings without #.')
    palette = {key: value.upper() for key, value in palette.items()}
    sources = spec.get('sources')
    if not isinstance(sources, list) or not sources:
        raise ValueError('Supply at least one source, such as the user-provided brief.')
    source_map = {}
    for source in sources:
        if not isinstance(source, dict) or not all(isinstance(source.get(k), str) and source[k].strip() for k in ['id', 'title', 'location']):
            raise ValueError('Every source needs nonempty id, title, and location strings.')
        if source['id'] in source_map:
            raise ValueError('Source IDs must be unique.')
        source_map[source['id']] = source
    with ZipFile(BASE / 'assets/layout-library.pptx') as archive:
        originals = {name: archive.read(name) for name in archive.namelist()}
    parts = {name: value for name, value in originals.items()
             if not name.startswith(('ppt/slides/', 'ppt/notesSlides/'))}
    pres = ET.fromstring(parts['ppt/presentation.xml'])
    ids = pres.find('p:sldIdLst', NS)
    ids.clear()
    rels = ET.fromstring(parts['ppt/_rels/presentation.xml.rels'])
    for relationship in list(rels):
        if relationship.get('Type', '').endswith('/slide'):
            rels.remove(relationship)
    content_types = ET.fromstring(parts['[Content_Types].xml'])
    for entry in list(content_types):
        if entry.get('PartName', '').startswith(('/ppt/slides/', '/ppt/notesSlides/')):
            content_types.remove(entry)
    role_map = {value: palette[key] for key, value in library['palette'].items()}
    used_layouts = set()
    for number, slide in enumerate(slides, 1):
        if not isinstance(slide, dict) or set(slide) - {'layout', 'fields', 'source_ids', 'notes', 'source_line'}:
            raise ValueError(f'Slide {number}: unexpected slide properties.')
        layout = slide.get('layout')
        if layout not in library['layouts']:
            raise ValueError(f'Slide {number}: unknown layout {layout!r}.')
        contract = library['layouts'][layout]
        fields = slide.get('fields')
        if not isinstance(fields, dict) or set(fields) - set(contract['fields']):
            raise ValueError(f'Slide {number}: unexpected or missing fields object.')
        source_ids = slide.get('source_ids')
        if not isinstance(source_ids, list) or not source_ids or any(not isinstance(k, str) or k not in source_map for k in source_ids):
            raise ValueError(f'Slide {number}: source_ids must identify provided sources.')
        if not isinstance(slide.get('notes', ''), str) or not isinstance(slide.get('source_line', ''), str):
            raise ValueError(f'Slide {number}: notes and source_line must be text.')
        values = {}
        for key, rules in contract['fields'].items():
            value = fields.get(key, rules['default'] if rules['default'] is not None else '' if rules['optional'] else None)
            if not isinstance(value, str) or (not value.strip() and not rules['optional']):
                raise ValueError(f'Slide {number}: provide {key}.')
            if re.search(r'\{\{.+?\}\}|\[(?:CLIENT|CAMPAIGN|PROJECT|TODO|TBD)', value, re.I):
                raise ValueError(f'Slide {number}: unresolved placeholder in {key}.')
            if len(value) > rules['budget']:
                raise ValueError(f'Slide {number}: {key} exceeds its {rules["budget"]}-character drafting budget. Edit the copy or choose another layout.')
            values[key] = value
        original_number = contract['slide']
        tree = ET.fromstring(originals[f'ppt/slides/slide{original_number}.xml'])
        for shape in tree.findall('.//p:spTree/p:sp', NS):
            name = shape.find('p:nvSpPr/p:cNvPr', NS).get('name', '')
            if name.startswith('case.'):
                set_text(shape, values[name[5:]])
        for group in contract.get('groups', []):
            present = [bool(values[key].strip()) for key in group['fields']]
            if any(present) and not all(present):
                raise ValueError(f'Slide {number}: fill every field in {group["fields"]} or leave that unit empty.')
            if any(present):
                continue
            gx, gy, gw, gh = group['bounds']
            shape_tree = tree.find('p:cSld/p:spTree', NS)
            for node in list(shape_tree):
                xf = node.find('p:spPr/a:xfrm', NS)
                if xf is None:
                    continue
                off, ext = xf.find('a:off', NS), xf.find('a:ext', NS)
                if off is None or ext is None:
                    continue
                x, y, w, h = int(off.get('x')), int(off.get('y')), int(ext.get('cx')), int(ext.get('cy'))
                if x >= gx - 100 and y >= gy - 100 and x + w <= gx + gw + 100 and y + h <= gy + gh + 100:
                    shape_tree.remove(node)
        for color in tree.findall('.//a:srgbClr', NS):
            if color.get('val') in role_map:
                color.set('val', role_map[color.get('val')])
        if slide.get('source_line'):
            if len(slide['source_line']) > 160:
                raise ValueError('Source footer exceeds 160 characters; put full references in notes.')
            footer(tree, slide['source_line'], palette['muted'])
        slide_name = f'ppt/slides/slide{number}.xml'
        parts[slide_name] = ET.tostring(tree, encoding='utf-8', xml_declaration=True)
        slide_rels = ET.fromstring(originals[f'ppt/slides/_rels/slide{original_number}.xml.rels'])
        for relation in slide_rels:
            if relation.get('Type', '').endswith('/notesSlide'):
                relation.set('Target', f'../notesSlides/notesSlide{number}.xml')
        parts[f'ppt/slides/_rels/slide{number}.xml.rels'] = ET.tostring(slide_rels, encoding='utf-8', xml_declaration=True)
        notes = ET.fromstring(originals[f'ppt/notesSlides/notesSlide{original_number}.xml'])
        note_body = next(s for s in notes.findall('.//p:sp', NS)
                         if s.find('p:nvSpPr/p:nvPr/p:ph', NS) is not None
                         and s.find('p:nvSpPr/p:nvPr/p:ph', NS).get('type') == 'body')
        lines = [slide.get('notes', '').strip(), '', 'Sources:']
        for source_id in source_ids:
            source = source_map[source_id]
            lines.append(f'[{source_id}] {source["title"]} — {source["location"]}' + (f' (as of {source["as_of"]})' if source.get('as_of') else ''))
        set_text(note_body, '\n'.join(lines))
        parts[f'ppt/notesSlides/notesSlide{number}.xml'] = ET.tostring(notes, encoding='utf-8', xml_declaration=True)
        note_rels = ET.fromstring(originals[f'ppt/notesSlides/_rels/notesSlide{original_number}.xml.rels'])
        for relation in note_rels:
            if relation.get('Type', '').endswith('/slide'):
                relation.set('Target', f'../slides/slide{number}.xml')
        parts[f'ppt/notesSlides/_rels/notesSlide{number}.xml.rels'] = ET.tostring(note_rels, encoding='utf-8', xml_declaration=True)
        rid = f'rIdCase{number}'
        ET.SubElement(ids, f'{{{NS["p"]}}}sldId', {'id': str(255 + number), f'{{{NS["r"]}}}id': rid})
        ET.SubElement(rels, '{http://schemas.openxmlformats.org/package/2006/relationships}Relationship',
                      {'Id': rid, 'Type': NS['r'] + '/slide', 'Target': f'slides/slide{number}.xml'})
        for kind, folder in [('slide', 'slides'), ('notesSlide', 'notesSlides')]:
            ET.SubElement(content_types, '{http://schemas.openxmlformats.org/package/2006/content-types}Override',
                          {'PartName': f'/ppt/{folder}/{kind}{number}.xml', 'ContentType': f'application/vnd.openxmlformats-officedocument.presentationml.{kind}+xml'})
        used_layouts.add(layout)
    parts['ppt/presentation.xml'] = ET.tostring(pres, encoding='utf-8', xml_declaration=True)
    parts['ppt/_rels/presentation.xml.rels'] = ET.tostring(rels, encoding='utf-8', xml_declaration=True)
    parts['[Content_Types].xml'] = ET.tostring(content_types, encoding='utf-8', xml_declaration=True)
    # The library may contain unused icon PNGs, but no unselected slides or client copy.
    output = Path(output)
    if output.exists():
        raise ValueError(f'Output already exists: {output}. Choose a new filename.')
    output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(output, 'x', ZIP_DEFLATED) as archive:
        for name, value in parts.items():
            archive.writestr(name, value)
    return {'output': str(output), 'slides': len(slides), 'layouts': sorted(used_layouts)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('spec', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps(build(json.loads(args.spec.read_text()), args.output), indent=2))
    except (ValueError, OSError, KeyError, TypeError, ET.ParseError) as exc:
        parser.exit(1, f'Cannot build case study: {exc}\n')


if __name__ == '__main__':
    main()
