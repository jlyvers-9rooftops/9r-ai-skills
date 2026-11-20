# Reference deck review

Review date: 2026-11-19. Source: the four supplied PowerPoint files in
`plugins/rtp-casestudies/examples/` and `plugins/rtp-casestudies/template.md`.
The source files remain unchanged.

This review inspects all slide text, explicit typography, shape positions,
colors, embedded-image dimensions, and slide counts directly from OOXML.
These are observed example conventions, not independently verified client brand
standards or substantiation of the examples' business claims. Native PowerPoint
rendering was unavailable in the review environment; layout observations derive
from the editable source geometry rather than a native application render.

## Confirmed requirements

From the supplied Markdown template:

- Use client brand colors.
- Maximum five slides.
- Agency Professional tone.
- No screenshots in the finished deck.
- If an actual quotation is used, place it in the closing.
- Capture client/campaign, website, project start/end, project description,
  approach, relevance, unfair advantage, results, and participating personnel,
  including subconsultants where supplied.

From the user interview:

- Decks serve both leave-behind and live-pitch uses; leave-behind is the default.

## Shared visual vocabulary

All four files use a 13.333 × 7.5 inch, 16:9 canvas. Text and most design elements
are native editable PowerPoint shapes. Embedded PNGs are primarily small icons;
they are not full-slide screenshots. The active content uses Georgia for display
headlines and many card titles, and Calibri for body copy, labels, and footers.
Arial also occurs in package/theme data; it is not the main authored text system.

Typical geometry in the three five-slide examples:

- Cover: dark client-colored background, a 0.35-inch accent strip on the left,
  and content beginning around x = 0.9 inches.
- Interior pages: approximately 0.6-inch horizontal margins, client-colored
  headings, white or pale tinted panels, restrained rules and accents.
- Closing: a prominent unfair-advantage statement at left and a narrower team
  section at right, with website/engagement information along the bottom.

Typical observed sizes, which vary with actual copy:

- Cover headline: 44–54 pt Georgia; client line: 22 pt Calibri.
- Interior headline: 26–36 pt Georgia.
- Card title: 16–20 pt Georgia; body: commonly 11.5–14 pt Calibri.
- Hero KPI: 56–72 pt; secondary metrics vary by layout.
- Labels, dates, team lists, and source footers: commonly 9.5–13 pt.

The smallest example text suits a close-read leave-behind better than a projected
presentation. Font substitution may change wrapping: this review machine resolves
Calibri to Carlito and Georgia to Liberation Serif. The font names in the actual
PPTX should remain explicit; do not claim a substitute is the supplied brand font.

## Inventory and narrative patterns

### Carle Health — 5 slides

1. Cover: client and a healthcare navigation outcome headline.
2. At a Glance: three columns — client, challenge, approach; engagement and
   deliverables below.
3. Approach: six capability cards in a three-column, two-row grid.
4. Results: three primary metrics with two supporting outcomes and a source line.
5. Unfair Advantage: strategic takeaway, team disciplines, website, and dates.

Observed client palette: dark teal `0E3D3A`, teal `1F8A7C`, light teal `5BB8AA`,
light surface `F2F6F4`, text `1F302E`, secondary text `5F6E6C`, rule `DCE0DD`.

### Discover South Carolina — 5 slides

Uses the same five-slide sequence and substantially the same coordinates as Carle.
The results slide uses two broad headline metrics plus two supporting outcomes,
rather than forcing Carle's three-metric layout. The closing accommodates six
team disciplines and several websites.

Observed client palette: deep blue `0F3D4D`, orange `E8623C`, darker orange
`C24A26`, cream `FAF4EA`, text `1F2D34`, secondary text `5B6770`, rule `DDD9D0`.

### Eternal Water SEO — 5 slides

1. Cover: a longer four-line outcome headline, reduced to 44 pt.
2. At a Glance: client, problem, approach; engagement and disciplines.
3. Pivot: two sequential phases instead of a six-card capability grid.
4. Results: one hero metric with four smaller supporting metrics and a source line.
5. Unfair Advantage: strategic takeaway, two disciplines, broader-engagement note.

Observed client palette: deep navy `0E2840`, blue `2BA3D6`, light blue `7DCBEA`,
darker blue `1E7FAB`, pale surface `F0F6FA`, text `1B2D3F`, secondary text
`5A6878`, rule `DCE3EA`.

### The UPS Store Franchise — 7 slides

1. Cover and three engagement/delivery facts.
2. Starting Point: four inherited-platform problems.
3. What We Built: six capability cards and a supporting-deliverables line.
4. Unfair Advantage: three differentiated capabilities with supporting evidence.
5. Team: five discipline columns.
6. When It Mattered Most: two production incidents and responses.
7. Outcomes & Ongoing Value: three headline facts and four supporting deliverables.

Observed client palette: brown `351C15`, yellow `FFB81C`, pale warm surfaces
`FAF6F1` / `E8DFD3`, text `1F1A17`, secondary text `6B5E54`, warm rules `C9B89A`.

This deck exceeds the supplied five-slide limit. Its rescue narrative, detailed
team breakdown, and incident proof are useful content references; its slide count
is not a precedent for exceeding the limit. A five-slide adaptation would fold
incidents into the approach or results, and team details into the closing.

## Evidence and editorial issues to guard against

- **Engagement versus measurement dates:** Eternal Water describes work ending
  December 2025 but reports an April 2026 endpoint. Its text identifies some
  results as post-engagement. Preserve that distinction and confirm ambiguous
  timing; do not silently move a result inside the engagement period.
- **Mixed percentage bases:** Eternal Water's “93% → 67%” is labeled as a branded
  to non-branded traffic flip, not a like-for-like series. Keep the denominators
  and traffic categories explicit. Do not convert it into percentage-point change
  without confirming comparable measures.
- **Rounded calculations:** The supplied 1.2K → 9.9K traffic values support +725%;
  1.7K → 2.9K keywords support approximately +71%. Preserve the stated precision
  and confirm raw figures before making a stronger numerical claim.
- **Time-sensitive benchmarks:** The Discover deck contains a #1 state-tourism
  benchmark and 100/100 PageSpeed claim. Future use needs the measurement date,
  tested scope, method, and actual supporting evidence. These are historical
  example claims, not current independent verifications.
- **Absolute accessibility claims:** Carle uses “100%” and WCAG 2.1 AA language.
  Such statements need an identified audit scope and supporting source; they
  should not be generalized from design intent or a single automated test.
- **Performance versus delivery facts:** The UPS deck's environments, upgrades,
  content counts, and response statements are not interchangeable with revenue,
  lead growth, conversion, or uptime measurements. Do not invent business lift.
- **Differentiation claims:** Comparative phrases about what other agencies can
  or cannot do require support. Prefer concrete capabilities demonstrated in
  the supplied project over unsourced market superiority.
- **Relevance is not a named slide in these examples:** The input template still
  requires it. Make relevance explicit in the narrative or closing, based on the
  intended audience or opportunity. Do not invent a prospective client's needs.
- **Personnel detail:** Examples mostly name disciplines, whereas the input asks
  for personnel and subconsultants. Report actual supplied names and partners;
  do not turn a discipline into a fictitious person or assume no subcontractors.
- **Sources:** Results pages contain short source labels, but the files' speaker
  notes do not provide a substantive evidence trail. Future decks should retain
  provided metric sources, dates, and qualifications in notes or a source record.
- **Quotation versus takeaway:** No actual attributed testimonial was found.
  A visually emphasized agency-written takeaway is not a client quotation.

## Confirmed alignment decisions

- Both leave-behind and live-pitch use; leave-behind is the default.
- A shared framework and Georgia/Calibri typography, with controlled layout
  variants and flexibility in story order when the case benefits.
- Supplied briefs/files are primary; limited web lookup may establish official
  client branding and general context. Ask about missing or conflicting results.
