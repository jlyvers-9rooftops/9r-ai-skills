---
name: alcosan-municipal-dashboard
description: Generate ALCOSAN executive dashboards from Municipal Meeting Monitor CSV reports, including sentiment, keyword mentions, tracked topic selections, meeting profiles, community events, and a keyword cloud. Use for ALCOSAN municipal meeting dashboards and updates to those reports.
---

# ALCOSAN Municipal Meeting Dashboard

Use the bundled [HTML template](assets/dashboard.html) and [generator](scripts/build_dashboard.py) to generate an executive dashboard from the CSV referenced in the current request, preserving the approved dashboard design. The template includes the complete CSS and embedded logo; it works without a network connection. Keep the skill folder together when transferring computers. A portable copy can be maintained in the project's `skills/alcosan-municipal-dashboard/` directory.

## Generate

Run from the user's project, resolving the script relative to this skill's directory:

```bash
python3 /path/to/alcosan-municipal-dashboard/scripts/build_dashboard.py \
  /path/to/MunicipalMeetingMonitorForm_Report.csv
```

Always write all deliverables under `web/ALC-MeetingMonitorDashboard-CURRENTDATE/` relative to the project root. Replace `CURRENTDATE` with the current local calendar date in `YYYYMMDD` format at generation time, not the CSV reporting period. Run the generator from the project root; it creates this folder automatically and writes `index.html` and `index.audit.json`. There is no output-path override. Save the PDF as `dashboard.pdf`, and any reviewed event JSON, previews, or validation files in this same dated folder. Same-day updates reuse this folder; a different generation date creates a new folder. Keep reusable generation code in `scripts/`; temporary experiments belong in `/tmp`.

Read [data processing rules](references/data-rules.md) when validating a run, changing processing, or interpreting source inconsistencies. Missing required columns stop generation instead of silently changing counts. Column matching ignores case and surrounding whitespace. Blank notes become empty strings; missing or unrecognized sentiment becomes Unrated.

## Fresh data and header period

Read the referenced CSV afresh on every run. Recalculate all counts, charts, cloud terms, meeting rows, event notes, and executive summaries from that export. Do not reuse previous dashboard data, totals, dates, event summaries, or PDFs.

Derive the header report period from the earliest and latest valid values in the CSV's `Start Date/Time` column. Use month and year for each endpoint, including both years when the export spans years. Use the same period in the HTML title, header, source summary, and generated PDF. If no valid meeting dates exist, show “Dates not recorded”; retain invalid-date rows and report their number in the audit. Never substitute the CSV filename, event dates, today's date, or a previously generated period for the meeting-date range.

The current local date determines only the output folder name. The CSV meeting dates determine the report period.

## Approved appearance and section order

Preserve the bundled template's design unless the user asks for changes:

- Solid navy `#003087` header, embedded round ALCOSAN logo, program name, report period.
- System sans-serif fonts; light gray `#f9fafb` background; 1280px maximum content width; white cards; 16px panel radius; existing spacing and shadows.
- Hero: “Municipal sentiment and topic signals,” executive introduction, source summary, and Download PDF when a PDF exists.
- Four summary cards: rated meetings, leading rated sentiment, negative meetings, unrated records.
- Overall sentiment SVG doughnut and keyword mention bars.
- Meeting type and meeting format SVG doughnuts.
- Community Events distribution and community event register with expandable source notes.
- Tracked topic selections, separate from keyword mention counts.
- Leadership focus and executive readout based on the current data.
- All municipal meetings, newest first, with date, municipality, sentiment, and detected topics.
- Forty-term static keyword cloud and sentiment legend, followed by data-provenance footer.

Use inline CSS/SVG and text spans as in the template. Tailwind, Chart.js, wordcloud2, Google Fonts, a gradient header, keyword-count summary cards, or a 10–15-row table would change the approved design. Preserve the mobile card-table layout, accessible labels, reduced-motion handling, and landscape Letter print styles.

Sentiment charts use positive green `#00a651`, neutral amber `#f59e0b`, negative red `#dc2626`, and unrated slate `#64748b`. The cloud uses neutral blue `#0066cc` instead of amber.

## Events and PDFs

Event notes come from the current CSV. The generator has no bundled event data. Inspect the notes and save reviewed structured entries in `events.json` in the current output folder, using the schema in `references/data-rules.md`. Pass that file with `--events FILE` for a finished report. Entries apply only when meeting number, start time, municipality, and full source note match; unmatched notes retain their source text and a review prompt. Do not guess dates or actions. Retain uncertain dates, missing years, and source year inconsistencies visibly. The register is a report-period snapshot, not a live list filtered by today's date.

For a PDF deliverable, print the generated HTML with a browser using its embedded print styles, landscape Letter, backgrounds enabled, and browser headers/footers disabled. Save it as `dashboard.pdf` in the current dated output folder. Run the generator again with `--pdf-href dashboard.pdf` to add the download button; the target must exist. Regenerate the PDF from this run’s HTML before adding the link, including when updating the same output folder.

## Verify and deliver

Confirm all deliverables are in the current dated output folder and `index.html` exists, inspect the audit counts, and check desktop, mobile, and print output when changing layout or the template. Verify the header range against the earliest and latest valid meeting dates in the referenced CSV, and verify totals against that same export. Check event source notes and unknown dates, all meeting rows, cloud counts/colors/sizes, and download target. If the data differs, explain the discrepancy rather than changing totals to fit an expected number.

Return a link to the generated dashboard and a concise summary of mentions and sentiment. For skill updates, also identify the portable skill copy and whether the installed copy was updated.
