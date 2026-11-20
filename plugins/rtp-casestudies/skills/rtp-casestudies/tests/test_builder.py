"""Behavior checks for native PowerPoint generation; run with python3 -B."""
from pathlib import Path
import importlib.util
import json
import tempfile
import unittest
from zipfile import ZipFile
import xml.etree.ElementTree as ET

BASE = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name, BASE / 'scripts' / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


builder, validator = load('build_case_study'), load('validate_deck')
LIB = json.loads((BASE / 'assets/layouts.json').read_text())


def fixture(layouts):
    return {
        'palette': dict(LIB['palette']),
        'sources': [{'id': 'test', 'title': 'Synthetic layout fixture', 'location': 'Unit test; not client work'}],
        'slides': [{
            'layout': layout,
            'fields': {key: 'TEST' if key.endswith('_value') or key == 'hero_value' else 'Synthetic test copy'
                       for key, rule in LIB['layouts'][layout]['fields'].items()
                       if rule['default'] is None and not rule['optional']},
            'source_ids': ['test'],
            'notes': 'Fictional copy used only to exercise the layout. No client claim.'
        } for layout in layouts]
    }


class BuilderTests(unittest.TestCase):
    def test_every_layout_is_a_valid_editable_presentation(self):
        with tempfile.TemporaryDirectory() as tmp:
            for layout in LIB['layouts']:
                with self.subTest(layout=layout):
                    target = Path(tmp) / (layout + '.pptx')
                    builder.build(fixture([layout]), target)
                    result = validator.validate(target)
                    self.assertTrue(result['ok'], result)
                    self.assertEqual(result['slides'], 1)

    def test_five_slide_story_reorders_and_keeps_notes_and_fields(self):
        spec = fixture(['cover', 'overview', 'results_hero', 'approach_phases', 'closing'])
        spec['slides'][0]['fields']['headline'] = 'Synthetic first line\nSecond line & <literal text>'
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / 'story.pptx'
            builder.build(spec, target)
            self.assertTrue(validator.validate(target)['ok'])
            with ZipFile(target) as z:
                third = '\n'.join(t.text or '' for t in ET.fromstring(z.read('ppt/slides/slide3.xml')).findall('.//a:t', builder.NS))
                self.assertIn('THE RESULTS', third)
                cover = '\n'.join(t.text or '' for t in ET.fromstring(z.read('ppt/slides/slide1.xml')).findall('.//a:t', builder.NS))
                self.assertIn('Second line & <literal text>', cover)
                notes = z.read('ppt/notesSlides/notesSlide3.xml').decode()
                self.assertIn('Synthetic layout fixture', notes)
                self.assertNotIn('ppt/slides/slide6.xml', z.namelist())

    def test_optional_units_disappear_without_filler(self):
        with tempfile.TemporaryDirectory() as tmp:
            for layout in ['approach_cards', 'approach_phases', 'results_hero', 'closing']:
                target = Path(tmp) / (layout + '.pptx')
                builder.build(fixture([layout]), target)
                with ZipFile(target) as z:
                    slide = ET.fromstring(z.read('ppt/slides/slide1.xml'))
                    names = [n.get('name') for n in slide.findall('.//p:cNvPr', builder.NS)]
                    for group in LIB['layouts'][layout].get('groups', []):
                        for key in group['fields']:
                            self.assertNotIn('case.' + key, names)

    def test_palette_and_icon_effects_follow_client_colors(self):
        spec = fixture(['overview'])
        spec['palette']['accent'] = 'AB2345'
        spec['palette']['primary'] = '342516'
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / 'palette.pptx'
            builder.build(spec, target)
            with ZipFile(target) as z:
                slide = ET.fromstring(z.read('ppt/slides/slide1.xml'))
                self.assertIn('342516', [c.get('val') for c in slide.findall('.//a:srgbClr', builder.NS)])
                effects = slide.findall('.//a:duotone/a:srgbClr', builder.NS)
                self.assertTrue(effects)
                self.assertTrue(all(c.get('val') == 'AB2345' for c in effects))

    def test_no_original_client_copy_or_unused_placeholders_leaks(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / 'clean.pptx'
            builder.build(fixture(['cover', 'overview', 'approach_cards', 'results_three', 'closing']), target)
            with ZipFile(target) as z:
                text = '\n'.join(z.read(n).decode() for n in z.namelist() if n.endswith('.xml'))
                for forbidden in ['Carle', 'SCPRT', 'Eternal Water', 'carle.com', '{{', '+725%', '+65%']:
                    self.assertNotIn(forbidden, text)

    def test_invalid_specs_and_overwriting_are_rejected(self):
        cases = []
        p = fixture(['cover'] * 6); cases.append(p)
        p = fixture(['cover']); p['slides'][0]['source_ids'] = ['missing']; cases.append(p)
        p = fixture(['cover']); p['slides'][0]['fields']['headline'] = 'x' * 81; cases.append(p)
        p = fixture(['cover']); p['slides'][0]['fields']['headline'] = '{{CLIENT_NAME}}'; cases.append(p)
        p = fixture(['approach_cards']); p['slides'][0]['fields']['card_2_title'] = 'Incomplete card'; cases.append(p)
        with tempfile.TemporaryDirectory() as tmp:
            for i, spec in enumerate(cases):
                with self.subTest(case=i), self.assertRaises(ValueError):
                    builder.build(spec, Path(tmp) / f'invalid-{i}.pptx')
            target = Path(tmp) / 'existing.pptx'; target.write_bytes(b'original')
            with self.assertRaises(ValueError):
                builder.build(fixture(['cover']), target)
            self.assertEqual(target.read_bytes(), b'original')

    def test_qualitative_outcomes_can_have_editable_source_footer(self):
        spec = fixture(['approach_cards'])
        spec['slides'][0]['fields']['section'] = 'THE RESULTS'
        spec['slides'][0]['source_line'] = 'Source: synthetic test only.'
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / 'qualitative.pptx'
            builder.build(spec, target)
            self.assertTrue(validator.validate(target)['ok'])
            with ZipFile(target) as z:
                self.assertIn('case.source_line', z.read('ppt/slides/slide1.xml').decode())


if __name__ == '__main__':
    unittest.main()
