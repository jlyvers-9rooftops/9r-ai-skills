# Data processing rules

## Source text and counting

Analyze these seven fields, retaining repeated text across fields as repeated mentions:

- GROW Notes
- New Industrial/Commercial Business Notes
- Regionalization Transfer Agreements Notes
- Questions or Comments for or about ALCOSAN Notes
- Meeting Notes
- Rates/Clean Water Assistance Fund Notes
- Community Events Notes

Match case-insensitively with word boundaries:

| Label | Regex |
|---|---|
| ALCOSAN | `\b(?:ALCOSAN|ALCOAN)\b` |
| GROW | `\bGROW\b` |
| Regionalization | `\b(?:regionalization|regionalize|regionalizing)\b` |
| Rates / CWAF | `\b(?:rates?|CWAF)\b` |

A mention is an occurrence, not a record. Also calculate the number of records containing each topic for narrative summaries and table tags. Do not use checkbox booleans for keyword mentions or explicit Yes selections.

Read selections from the text-valued GROW, Community Events, Regionalization Transfer Agreements, Questions or Comments for or about ALCOSAN, Rates/Clean Water Assistance Fund, and New Industrial/Commercial Business fields. Count trimmed case-insensitive `Yes`, and retain blank values in distribution charts as Not recorded.

All source records contribute to summaries, distributions, mentions, selections, and the cloud, including internal test records. Exclude municipalities matching `\b9\s*rooftops\b` only from the municipal meetings table and event register. Do not search Task Owner or CRM email to detect internal records: municipal records also have 9Rooftops owner addresses. Preserve duplicate source rows; the approved report counts them separately.

Sentiment comes from Meeting Observation, with blank or unrecognized values Unrated. Rated percentages use Positive + Neutral + Negative as the denominator. The unrated legend uses a separate count. All other profile chart percentages use all source records. Keep missing/invalid meeting dates visible as Not recorded and expose their count in the audit.

## Cloud

Use the four normalized topic totals first, followed by the 36 most frequent non-target tokens after the generator's fixed stopword list. Tokenize with `\b[A-Za-z][A-Za-z'-]*\b`, keep tokens of length at least three, and preserve CSV record and note-column order for frequency ties. Calculate the vocabulary from the current CSV; never reuse a prior word list or its counts.

Color by a majority vote of rated records containing each term, one vote per record; ties or no rated votes are Neutral. Unrated records still contribute to frequency. Font size is `15 + 25 * sqrt(count / highest_cloud_count)` pixels, rounded to one decimal. The legend counts displayed terms by dominant sentiment, not meetings or mentions.

## Meeting dates and report period

Parse `Start Date/Time` values from the current export. The earliest and latest valid meeting timestamps define the report period displayed in the title, header, and source summary. Format both endpoints as month and year. Keep cross-year ranges intact. If every date is invalid or missing, display “Dates not recorded” and retain all rows. The audit exposes the unparsed-date count.

The output directory uses the current local run date; the report period uses CSV meeting dates. Filename date fragments and community event dates do not define the report period.

## Events

No event records ship with the skill. Extract event summaries from the current export's Community Events Notes. Preserve missing years, uncertain dates, and source year inconsistencies visibly; do not infer event dates from meeting dates or silently correct a stated year. Do not invent an ALCOSAN action or confirmed participation from a question.

For reviewed summaries, supply `--events FILE` with a JSON array. Each object has these fields:

| Field | Value |
|---|---|
| `meeting_number` | Exact Meeting Number from the CSV |
| `meeting_start` | Exact Start Date/Time string from the CSV |
| `municipality` | Exact Municipality, Township or Borough value |
| `source_note` | Full Community Events Notes text, trimmed |
| `date_html` | Escaped display date and optional semantic HTML; Not recorded if absent |
| `event` | Event name supported by the note |
| `details` | Factual summary and explicit uncertainty supported by the note |

Keep this export-specific JSON beside the dashboard. The generator accepts a reviewed entry only when all four source identity fields match. Without an entry, it displays the original note with a review prompt. Inspect and resolve the audit's unreviewed-event count before delivering a finished report. Event registers include notes from the export regardless of today's date.

## Validation

Recalculate totals from the referenced CSV on each run. Check that rated + unrated equals source records, sentiment categories sum to source records, and profile distributions retain missing values. Verify mention occurrences separately from records containing each topic and explicit Yes selections. Check that visible municipal table and event rows exclude only internal rows under the rule above. Compare cloud counts and colors against the current notes and Meeting Observation labels.

Check the CSV-derived period in the HTML title, header, source summary, and newly generated PDF. When rerunning into the same dated folder, replace the report with calculations from the new source and regenerate the PDF. Previous report totals and example counts are never acceptance criteria for a different export.
