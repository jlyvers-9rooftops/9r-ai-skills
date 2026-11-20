# Design and story contract

## Confirmed system

- 16:9 widescreen: 13.333 × 7.5 inches.
- Georgia display headings; Calibri body, labels, dates, and source text.
- Client-specific colors within stable roles: primary dark, accent, accent light,
  accent dark, soft surface, ink, secondary text, and rule. Prefer an official
  client brand guide; otherwise inspect the official site and record the source.
- About 0.6-inch interior margins; 0.9-inch cover content origin and a 0.35-inch
  left accent strip. Preserve the supplied layout bank's geometry.
- Dark cover, bright interior pages, structured color accents, native editable
  text/cards, restrained icons, and an unfair-advantage/team closing.
- At most five finished slides. All examples except UPS use five; UPS's seven
  slides are a content reference, not permission for a longer deliverable.
- Agency Professional writing: a grounded point of view, clear stakes, specific
  actions, qualified outcomes. Avoid generic promotion and unsupported comparisons.
- No screenshots. Do not rasterize a whole slide to fake a PowerPoint deliverable.

The user approved a shared framework with controlled variants and flexibility in
story order when needed. Keep an intentional opening and closing. Reorder the
interior story when the evidence warrants it, without creating a new visual
system for each case. Shorter decks may combine story beats while retaining the
brief's essential meaning; do not pad to five with weak evidence.

## Layout choice

| Layout | Best use | Capacity |
|---|---|---|
| `cover` | Client, headline, engagement, agency credit | One narrative opening |
| `overview` | Client / challenge / approach context | Three explanatory columns |
| `approach_cards` | Parallel capabilities or qualitative outcomes | Up to six title/body units |
| `approach_phases` | A pivot or sequential strategy | Two phases, up to four points each |
| `results_three` | Three comparable principal metrics | Three metric values/labels; up to two supporting outcomes |
| `results_two` | Two principal metrics with explanation | Two metric values/labels/details; up to two supporting outcomes |
| `results_hero` | One strongest metric | One hero value/label/detail; up to four secondary metrics |
| `closing` | Unfair advantage, relevance/quote, team, website | Main point, supporting text, up to six contributors/disciplines |

The builder removes unused optional units and their backgrounds/icons. Never
invent extra capabilities or metrics to fill a grid. Optional multi-field units
must be supplied completely or omitted together. If sparse content needs better
balance, adjust native shapes in a copy rather than adding filler.

For purely qualitative results, use `approach_cards` with `section` set to
`THE RESULTS`, outcome-focused wording, and a short `source_line`. Do not force
non-numeric words into large KPI slots or imply a measurement that does not exist.

## Copy and typography

Native examples use cover headlines around 44–54 pt, interior headings 26–36 pt,
card titles 16–20 pt, body commonly 11.5–14 pt, labels/sources around 10–12 pt, and
large result values. Maintain those roles and the Georgia/Calibri pairing for the
default close-read leave-behind. The cover supports deliberate line breaks.

Character budgets in `assets/layouts.json` are conservative drafting constraints,
not line-wrap measurement. The builder rejects excess copy instead of silently
shrinking fonts. Native render inspection remains necessary. Put long supporting
facts and provenance into notes rather than tiny type.

For a live pitch, use substantially less copy and increase body reading sizes
(typically 16–18 pt or larger). A 10–12 pt leave-behind card is not adequate merely
because the source examples use it. Prefer fewer meaningful units, keep charts
simple, and adapt the native shapes as needed. The builder is a stable starting
point, not a requirement to retain unreadable text.

## Color and attribution

Use the client palette, not the previous case's palette or the Gantt planner's
9Rooftops UI colors. Choose dark/light variants so cover text, small metadata,
metrics, and rules remain readable. Small text needs at least 4.5:1 contrast;
large text needs at least 3:1. Do not assume an official accent is usable for all
text roles on white. Native icon duotone effects track the chosen accent; check
that the target presentation viewer renders them correctly.

The examples use text attribution to 9Rooftops. Logo placement is optional when
requested or assets are supplied for that purpose. Do not automatically insert a
logo from an unrelated project.

## Closing and evidence

The closing should explain why the agency's particular contribution mattered and
why the case is relevant. Use supplied personnel, disciplines, or partners; don't
invent named people or claim there were no vendors. An actual quote, if supplied,
belongs on this slide with clear attribution. It may replace supporting copy,
but should not displace the case's own differentiator or required relevance.

On results slides, keep the metric label, unit, period and short source readable.
Full source IDs, references, and qualifications are stored in speaker notes.
