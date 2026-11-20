# PowerPoint build specification

Use Python 3's standard library. Resolve paths from the skill directory; write
specs and decks into the user's working project, not this installed package.

```sh
python3 scripts/build_case_study.py /path/to/deck-spec.json /path/to/case-study.pptx
python3 scripts/validate_deck.py /path/to/case-study.pptx
```

## Schema

The specification contains exactly `palette`, `sources`, and `slides`.

- `palette`: eight six-digit RGB hex strings, without `#`: `primary`, `accent`,
  `accent_light`, `accent_dark`, `surface`, `ink`, `muted`, and `rule`.
  Select client-specific values and confirm contrast. White is fixed.
- `sources`: nonempty array of `{id, title, location, as_of?}` records. `location`
  may identify an approved brief or local file, or give an exact public URL.
  `as_of` is optional source/measurement dating, not a generated project date.
- `slides`: one to five objects, in intended story order. Each has `layout`,
  `fields`, nonempty `source_ids`, optional `notes`, and optional `source_line`.
- `layout`: a key from `assets/layouts.json`. Read only the chosen layouts' field
  definitions; they include defaults, optional status, and character budgets.
- `fields`: map of slot names to text. Section labels and agency credit have
  documented defaults. Supply every other required field. Omit optional units
  instead of adding filler. Line breaks are supported; styles stay editable.
- `source_ids`: identifiers from the top-level `sources` array supporting this
  slide. The builder writes them and the source references into speaker notes.
- `notes`: context, speaker guidance, metric definitions and qualifications.
- `source_line`: optional short editable footer, useful for qualitative results
  built with `approach_cards`. Use `source` instead when the result layout already
  has that field. Full URLs and long citations belong in notes.

Example of valid **single-slide syntax**, not a complete case-study story. The
copy is deliberately marked as synthetic; replace it with actual sourced content:

```json
{
  "palette": {
    "primary": "203044",
    "accent": "007DA3",
    "accent_light": "7DD1E8",
    "accent_dark": "02607B",
    "surface": "F4F7F9",
    "ink": "17202A",
    "muted": "52606D",
    "rule": "D9E0E5"
  },
  "sources": [
    {"id": "brief", "title": "Synthetic layout test", "location": "Test fixture only"}
  ],
  "slides": [
    {
      "layout": "cover",
      "fields": {
        "client": "Synthetic example — not client work",
        "headline": "A clear story.\nA consistent presentation.",
        "engagement": "Synthetic layout test only"
      },
      "source_ids": ["brief"],
      "notes": "All content on this slide is fictional test copy."
    }
  ]
}
```

A normal five-slide selection is `cover`, `overview`, `approach_cards`,
`results_three`, `closing`. Replace the approach/results variants based on actual
evidence; interior order can change. The builder can reuse a layout when a shorter
or reordered narrative benefits, but never raises the five-slide cap.

## Notes on implementation

`assets/layout-library.pptx` contains eight sanitized reusable slide designs,
with named text shapes such as `case.headline` and no original case-study facts.
It preserves native text, vector shapes, icons, Georgia/Calibri styling, and a
neutral role palette. It is not a finished eight-slide case study.

The builder selects requested pages, rewrites native text and palette values,
removes unused optional groups, renumbers slide/note relationships, and includes
only the selected slide XML parts in the final package. Native image effects
recolor the bundled icons without flattening the slide. The original example
decks are unchanged and are not required at runtime.

The checker validates the ZIP/XML package, internal relationship targets, slide
count/aspect ratio, editable text, source notes, obvious placeholders, shape
bounds, and full-slide bitmaps. It does not certify metric truth, text fitting,
contrast, correct application of fonts, or native icon rendering.

Prefer native PowerPoint or an available compatible headless renderer to export
PDF/previews, then inspect every slide. If the environment lacks a renderer,
report structural validation separately and deliver a draft for visual review.
Do not upload private client material to an external conversion service without
user authorization. No PDF companion is produced by the bundled builder itself.
