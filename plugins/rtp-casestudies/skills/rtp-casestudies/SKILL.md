---
name: rtp-casestudies
description: Create editable 9Rooftops client case-study PowerPoint files with consistent typography, client-colored layouts, and evidence-backed storytelling. Use for case-study decks, RFP case-study inserts, and pitch leave-behinds.
---

# 9Rooftops Case Studies

Create an editable `.pptx` of at most five slides from the supplied case brief and
supporting files. Default to a new-business leave-behind that can also support a
live pitch. Use the established Georgia/Calibri design system and client brand
colors. The packaged layouts are native editable shapes, not slide screenshots.

## Start with the case, not the example's facts

Read [the brief and evidence guide](references/brief-and-evidence.md) and the
user's supplied material. Ask only about consequential missing information:
results and their measurement periods, audience-specific relevance, dates,
client identity/colors, and actual contributors or partners. Do not make the
user refill fields already present in their files.

Limited web lookup is allowed for official client branding and general context.
Use the supplied brief/files as the authority for work performed and results;
public context is not proof of private project outcomes. Ask about missing or
conflicting metrics. Identify historic measurements and post-engagement outcomes
without silently changing their dates. Record the source behind each claim.

The supplied input format is [the case brief](assets/case-brief.md). Accept loose
notes, Word/PDF documents, an existing deck, or a completed brief; normalize them
rather than requiring a particular input file type.

## Keep the family resemblance

Read [the design and story rules](references/design-and-story.md). Default story:

1. Cover: client, campaign, and a grounded outcome-led headline.
2. At a Glance: client, challenge, approach, engagement dates, scope.
3. Approach: what 9Rooftops did, shown as capability cards or two phases.
4. Results: sourced KPIs, recognition, or confirmed qualitative outcomes.
5. Closing: our unfair advantage, explicit relevance, team, website/dates;
   attributed quotations belong here if supplied.

Controlled variants and occasional story reordering are permitted when the case
benefits. Preserve the typography, spacing, palette roles, and five-slide maximum.
Do not force numeric KPI cards when only qualitative outcomes are supported.
Do not add screenshots. Small icons and native diagrams are acceptable. Keep
quotes exact and attributed; an agency-authored takeaway is not a testimonial.
Use an Agency Professional tone: specific, confident, concise, and defensible.

The examples are design/content references, not a bank of reusable claims.
[The review](references/example-review.md) explains the shared conventions,
layout differences, and evidence pitfalls across all four source decks. The
seven-slide UPS example does not override the five-slide cap.

## Build the PowerPoint

Use the bundled native layout library and builder by default. Read
[the build specification](references/build-spec.md) and inspect
`assets/layouts.json` for the selected layouts' field names and drafting budgets.
The eight-slide `assets/layout-library.pptx` is a layout bank, never a deliverable.
A finished deck selects at most five layouts; order is the spec's slide order.

```sh
python3 scripts/build_case_study.py /absolute/path/deck-spec.json /absolute/path/client-case-study.pptx
python3 scripts/validate_deck.py /absolute/path/client-case-study.pptx
```

Resolve script paths relative to this skill directory. Output into the user's
project or requested destination, not the installed skill. The builder uses only
Python 3's standard library, refuses to overwrite an existing output, and puts
source references in speaker notes. No accounts or cloud uploads are needed.

Use the actual client's palette. The layout bank's neutral colors are not a
fallback client identity. If the palette is unknown and cannot be found in an
official source, ask rather than borrowing another client's colors. Credit
9Rooftops in text as the examples do; add agency/client logos only when requested
or supplied for that use. Do not inherit unrelated projects' branding choices.

Copy budgets protect the layouts. Edit prose, choose another controlled variant,
or reduce the number of ideas before shrinking type. For live-pitch use, reduce
content and increase reading sizes; the leave-behind layouts' small body text is
not a universal projected-presentation standard. If a necessary adaptation exceeds
the builder's slots, edit a copy of the native layout with available presentation
tools while preserving the design rules and output constraints.

## Verify and deliver

- Validate package relationships, slide count, editable text, notes, and geometry
  with the bundled checker. Its success is structural, not proof of visual quality.
- Inspect every slide in a native PowerPoint or compatible PDF render when the
  environment supports it. Check wrapping, clipped text, overlap, font fallback,
  icon recoloring, contrast, reading size, and source footers. If native rendering
  is unavailable, disclose that limit and label the deck a draft for visual review.
- Reconcile all dates, figures, units, comparisons, quotes, and names with their
  sources. Relevance and unfair advantage must be specific to this case.
- Confirm no other client's facts, placeholder copy, invented results, or hidden
  unused slides remain. Do not deliver the eight-slide layout bank as a case study.

Deliver the actual editable `.pptx` with a concise account of its story/variants
and any remaining source or verification limitations. PDF/preview copies are
optional companions, not substitutes. Creating a deck does not authorize sending
it to clients or publishing it externally.
