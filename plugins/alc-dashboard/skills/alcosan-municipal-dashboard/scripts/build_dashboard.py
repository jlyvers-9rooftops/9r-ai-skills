#!/usr/bin/env python3
"""Generate the portable ALCOSAN executive dashboard using only Python's standard library."""
import argparse
from collections import Counter
import csv
from datetime import datetime
from html import escape
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
NOTES = ['GROW Notes', 'New Industrial/Commercial Business Notes',
         'Regionalization Transfer Agreements Notes',
         'Questions or Comments for or about ALCOSAN Notes', 'Meeting Notes',
         'Rates/Clean Water Assistance Fund Notes', 'Community Events Notes']
MUNICIPALITY = 'Municipality, Township or Borough'
PATTERNS = {
    'ALCOSAN': r'\b(?:ALCOSAN|ALCOAN)\b',
    'GROW': r'\bGROW\b',
    'Regionalization': r'\b(?:regionalization|regionalize|regionalizing)\b',
    'Rates / CWAF': r'\b(?:rates?|CWAF)\b',
}
SELECTIONS = {'GROW': 'GROW', 'Community events': 'Community Events',
              'Regionalization': 'Regionalization Transfer Agreements',
              'ALCOSAN questions/comments': 'Questions or Comments for or about ALCOSAN',
              'Rates / CWAF': 'Rates/Clean Water Assistance Fund',
              'New industrial/commercial business': 'New Industrial/Commercial Business'}
COLORS = {'Neutral': '#f59e0b', 'Positive': '#00a651', 'Negative': '#dc2626', 'Unrated': '#64748b'}
CLOUD_COLORS = {**COLORS, 'Neutral': '#0066cc'}
STOPWORDS = set('''the and for was with project council motion about meeting approved this that
has discussed not from their report related will engineer manager but are work regarding which
been discussion one new public going there out during our were did per said have only all into
also would could should they them then than its had can may any some more most much such these
those what when where who why how you your him her his she been being were does each other
borough township municipal municipality alcosan alcoan grow regionalization regionalize regionalizing
rate rates cwaf'''.split())


def text(row):
    return ' '.join(row[f] for f in NOTES)


def sentiment(row):
    value = row['Meeting Observation'].strip().title()
    return value if value in ('Positive', 'Neutral', 'Negative') else 'Unrated'


def date_value(row):
    value = row['Start Date/Time']
    for fmt in ('%m/%d/%Y %I:%M %p', '%m/%d/%Y %H:%M', '%m/%d/%Y', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d'):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            pass
    return None


def internal(row):
    # Do not search owner/email columns: municipal rows share a 9Rooftops CRM owner.
    return bool(re.search(r'\b9\s*rooftops\b', row[MUNICIPALITY], re.I))


def dominant(rows, pattern):
    votes = Counter(sentiment(r) for r in rows if re.search(pattern, text(r), re.I)
                    and sentiment(r) != 'Unrated')
    winners = [s for s, n in votes.items() if n == max(votes.values(), default=0)]
    return winners[0] if len(winners) == 1 else 'Neutral'


def donut(counts, total, label, colors=None, sentiment_chart=False, extra=None):
    colors = colors or ['#0066cc', '#00a651', '#f59e0b', '#64748b', '#dc2626']
    arcs, legend, offset = [], [], 0.0
    for i, (name, n) in enumerate(counts.items()):
        percentage = 100 * n / total if total else 0
        if sentiment_chart:
            attrs = f'class="donut-arc donut-{name.lower()}"'
            legend_attrs = f'class="legend-item {name.lower()}"'
        else:
            attrs = 'class="donut-arc"'
            legend_attrs = f'class="legend-item" style="color: {colors[i % len(colors)]};"'
        stroke = '' if sentiment_chart else f'stroke: {colors[i % len(colors)]}; '
        arcs.append(f'<circle {attrs} cx="60" cy="60" r="44" pathLength="100" style="{stroke}stroke-dasharray: {percentage:.1f} 100; stroke-dashoffset: -{offset:.1f};"></circle>')
        offset += percentage
        legend.append(f'<li {legend_attrs}><span class="dot" aria-hidden="true"></span><span>{escape(name)}</span><span class="legend-value">{n}</span></li>')
    if extra:
        legend.append(f'<li class="legend-item unrated"><span class="dot" aria-hidden="true"></span><span>Unrated source records</span><span class="legend-value">{extra}</span></li>')
    desc = ', '.join(f'{k} {v}' for k, v in counts.items()) + f' out of {total} {label}.'
    return f'''<div class="sentiment-layout"><div class="donut" role="img" aria-label="{escape(desc, quote=True)}"><svg viewBox="0 0 120 120" aria-hidden="true"><circle class="donut-track" cx="60" cy="60" r="44" pathLength="100"></circle>{''.join(arcs)}</svg><div class="donut-label"><strong>{total}</strong><span>{label}</span></div></div><ul class="legend" aria-label="Distribution totals">{''.join(legend)}</ul></div>'''


def bars(counts):
    peak = max(counts.values(), default=0)
    return ''.join(f'<li class="topic-row"><span class="topic-name">{escape(k)}</span><span class="bar-track" aria-hidden="true"><span class="bar-fill" style="width: {round(100*v/peak) if peak else 0}%;"></span></span><span class="topic-count">{v}</span></li>' for k, v in counts.items())


def metric(kicker, value, label, subtext, cls=''):
    return f'<article class="metric-card{cls}"><div class="metric-kicker">{kicker}</div><span class="metric-value">{value}</span><div class="metric-label">{label}</div><p class="metric-subtext">{subtext}</p></article>'


def focus(marker, heading, detail):
    return f'<li class="focus-item"><span class="focus-marker" aria-hidden="true">{marker}</span><div><h3>{escape(heading)}</h3><p>{escape(detail)}</p></div></li>'


def build(csv_path, events_path=None, pdf_href=None):
    output = Path('web') / f'ALC-MeetingMonitorDashboard-{datetime.now():%Y%m%d}' / 'index.html'
    with csv_path.open(encoding='utf-8-sig', newline='') as handle:
        reader = csv.DictReader(handle)
        names = {n.strip().casefold(): n for n in (reader.fieldnames or [])}
        required = NOTES + [MUNICIPALITY, 'Meeting Observation', 'Start Date/Time',
                           'Meeting Number', 'Meeting Type', 'Meeting Format'] + list(SELECTIONS.values())
        missing = sorted({f for f in required if f.casefold() not in names})
        if missing:
            raise ValueError('Missing required CSV columns: ' + ', '.join(missing))
        rows = [{f: (r.get(names[f.casefold()]) or '').strip() for f in set(required)} for r in reader]
    if not rows:
        raise ValueError('CSV contains no records')
    total = len(rows)
    sentiments = Counter(sentiment(r) for r in rows)
    rated = total - sentiments['Unrated']
    primary = max(('Neutral', 'Positive', 'Negative'), key=lambda s: sentiments[s]) if rated else 'Unrated'
    percent = round(100 * sentiments[primary] / rated) if rated else 0
    mentions = {k: sum(len(re.findall(p, text(r), re.I)) for r in rows) for k, p in PATTERNS.items()}
    containing = {k: sum(bool(re.search(p, text(r), re.I)) for r in rows) for k, p in PATTERNS.items()}
    selections = {k: sum(r[f].casefold() == 'yes' for r in rows) for k, f in SELECTIONS.items()}
    selections = dict(sorted(selections.items(), key=lambda kv: -kv[1]))
    dates = [d for r in rows if (d := date_value(r))]
    period = f'{min(dates):%b %Y}–{max(dates):%b %Y}' if dates else 'Dates not recorded'
    municipalities = [r for r in rows if not internal(r)]
    municipalities.sort(key=lambda r: date_value(r) or datetime.min, reverse=True)
    meeting_rows = []
    for r in municipalities:
        d = date_value(r)
        date = f'{d:%b} {d.day}, {d.year}' if d else 'Not recorded'
        topics = ''.join(f'<span class="topic-tag">{escape(k)}</span>' for k, p in PATTERNS.items() if re.search(p, text(r), re.I))
        topics = topics or '<span class="topic-tag empty">No flagged topics</span>'
        s = sentiment(r)
        meeting_rows.append(f'<tr><td class="date-cell">{date}</td><td>{escape(r[MUNICIPALITY])}</td><td><span class="badge {s.lower()}"><span class="dot" aria-hidden="true"></span>{s}</span></td><td><span class="topic-tags">{topics}</span></td></tr>')
    # Reviewed event extraction is used only for the exact source record + note.
    overrides = json.loads(events_path.read_text()) if events_path else []
    event_rows, excluded_events = [], 0
    for r in rows:
        raw = r['Community Events Notes']
        if not raw:
            continue
        if internal(r):
            excluded_events += 1
            continue
        match = next((e for e in overrides if all(e[k] == r[f] for k, f in [
            ('meeting_number', 'Meeting Number'), ('meeting_start', 'Start Date/Time'),
            ('municipality', MUNICIPALITY), ('source_note', 'Community Events Notes')])), None)
        if match:
            date_html, event, detail = match['date_html'], match['event'], match['details']
            order = overrides.index(match)
        else:
            date_html, event, detail = 'Not recorded', 'Community event', 'Review the source note for event date and follow-up.'
            order = len(overrides)
        tr = f'<tr><td class="date-cell">{date_html}</td><td>{escape(r[MUNICIPALITY])}</td><td class="event-name">{escape(event)}</td><td class="event-detail">{escape(detail)}<details class="raw-note"><summary>View source note</summary><p>{escape(raw)}</p></details></td></tr>'
        event_rows.append((order, tr))
    event_rows.sort(key=lambda pair: pair[0])
    # Use CSV field order for stable first-occurrence tie-breaking, matching the reference.
    note_order = [n for n in names if any(n == f.casefold() for f in NOTES)]
    actual_notes = {f.casefold(): f for f in NOTES}
    tokens = Counter(w.lower() for r in rows for n in note_order
                     for w in re.findall(r"\b[A-Za-z][A-Za-z'-]*\b", r[actual_notes[n]])
                     if len(w) >= 3 and w.lower() not in STOPWORDS)
    cloud = [(k, v, dominant(rows, PATTERNS[k])) for k, v in mentions.items() if v]
    cloud += [(w.upper() if w == 'lsse' else w.capitalize(), n, dominant(rows, r'\b'+re.escape(w)+r'\b')) for w, n in tokens.most_common(max(0, 40-len(cloud)))]
    peak = max((n for _, n, _ in cloud), default=1)
    cloud_html = '\n'.join(f'<span style="font-size: {15+25*(n/peak)**0.5:.1f}px; color: {CLOUD_COLORS[s]};" aria-label="{escape(k, quote=True)}: {n} mentions">{escape(k)}</span>' for k, n, s in cloud)
    cloud_sentiments = Counter(s for _, _, s in cloud)
    cloud_legend = ''.join(f'<li class="legend-item {s.lower()}"><span class="dot" aria-hidden="true"></span><span>{s}-dominant terms</span><span class="legend-value">{cloud_sentiments[s]}</span></li>' for s in ('Positive','Neutral','Negative'))
    low = min(mentions, key=mentions.get)
    high = max(mentions, key=mentions.get)
    count_values = lambda field: dict(Counter(r[field] or 'Not recorded' for r in rows))
    formats = count_values('Meeting Format')
    formats = {k: formats[k] for k in ('Virtual', 'In Person', 'Not recorded') if k in formats} | {k:v for k,v in formats.items() if k not in ('Virtual', 'In Person', 'Not recorded')}
    community = Counter(r['Community Events'].title() or 'Not recorded' for r in rows)
    community = {k: community[k] for k in ('Yes', 'No', 'Not recorded')} | {k:v for k,v in community.items() if k not in ('Yes', 'No', 'Not recorded')}
    metrics = [metric('Rated meetings', rated, 'with sentiment captured', f'{sentiments["Unrated"]} source records remain unrated.'),
               metric('Primary sentiment', sentiments[primary], f'{primary.lower()} meetings' if rated else 'unrated records', f'{percent}% of rated meetings.' if rated else 'No explicit sentiment captured.'),
               metric('Risk signal', sentiments['Negative'], 'negative meetings', 'Review the negative records in the table below.', ' is-risk'),
               metric('Data quality', sentiments['Unrated'], 'unrated records', 'Shown as “Unrated,” never as blank values.', ' is-quality')]
    pdf = ''
    if pdf_href:
        if not (output.parent / pdf_href).is_file():
            raise ValueError('PDF link target must exist beside the dashboard')
        pdf = f'<a class="download-link" href="{escape(pdf_href, quote=True)}" download><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M11 4h2v8.17l2.59-2.58L17 11l-5 5-5-5 1.41-1.41L11 12.17V4ZM5 18h14v2H5v-2Z"/></svg><span>Download PDF</span></a>'
    slots = dict(PERIOD=escape(period), SOURCE_NAME=escape(csv_path.name),
                 SOURCE_SUMMARY=f'{total} records | {escape(period)} | {rated} rated meetings', PDF_LINK=pdf,
                 METRICS=''.join(metrics), SENTIMENT=donut({s:sentiments[s] for s in ('Neutral','Positive','Negative')},rated,'rated',sentiment_chart=True,extra=sentiments['Unrated']),
                 MENTIONS=bars(mentions), MEETING_TYPE=donut(count_values('Meeting Type'),total,'records'),
                 MEETING_FORMAT=donut(formats,total,'records'),
                 COMMUNITY_EVENTS=donut(community,total,'records',['#00a651','#0066cc','#64748b']),
                 EVENT_ROWS=''.join(tr for _,tr in event_rows),
                 EVENT_REGISTER_NOTE=f'{len(event_rows)} municipal notes shown. {excluded_events} obvious 9Rooftops test records are excluded from this register.',
                 SELECTIONS=bars(selections), MEETING_ROWS=''.join(meeting_rows), CLOUD=cloud_html, CLOUD_LEGEND=cloud_legend,
                 FOCUS=focus('1',f'{sentiments["Negative"]} negative meetings require review.',f'Negative sentiment appears in {sentiments["Negative"]} of {rated} rated meetings ({round(100*sentiments["Negative"]/rated) if rated else 0}%).')
                 +focus('2',f'{low} is the lowest-volume tracked topic.',f'{mentions[low]} mentions appear across {containing[low]} source records.')
                 +focus('3','Unrated records need cleanup before distribution.',f'{sentiments["Unrated"]} blank or unrecognized sentiment records are counted separately as Unrated.'),
                 READOUT=focus('A',f'{primary} is the leading rated sentiment.' if rated else 'No meetings have explicit sentiment.',f'{sentiments[primary]} of {rated} rated meetings are {primary.lower()}, representing {percent}% of rated records.' if rated else f'All {total} records are unrated.')
                 +focus('B',f'Positive sentiment is present in {sentiments["Positive"]} records.',f'GROW appears {mentions["GROW"]} times across {containing["GROW"]} source records.')
                 +focus('C',f'{high} is the dominant tracked term.',f'It appears {mentions[high]} times across the combined designated notes fields.'))
    template = (ROOT/'assets/dashboard.html').read_text()
    rendered = re.sub(r'\{\{([A-Z_]+)\}\}', lambda m: slots[m[1]], template)
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(rendered)
    audit = dict(source=csv_path.name, period=period, records=total, rated=rated,
                 sentiments={s:sentiments[s] for s in ('Positive','Neutral','Negative','Unrated')},
                 mentions=mentions, records_containing=containing, selections=selections,
                 meeting_type=count_values('Meeting Type'), meeting_format=formats, community_events=community,
                 visible_meetings=len(meeting_rows), visible_events=len(event_rows), excluded_internal=total-len(municipalities),
                 unparsed_dates=sum(date_value(r) is None for r in rows),
                 unreviewed_event_notes=sum(not any(all(e[k]==r[f] for k,f in [('meeting_number','Meeting Number'),('meeting_start','Start Date/Time'),('municipality',MUNICIPALITY),('source_note','Community Events Notes')]) for e in overrides) for r in municipalities if r['Community Events Notes']),
                 cloud=[dict(term=k,count=n,sentiment=s) for k,n,s in cloud])
    output.with_suffix('.audit.json').write_text(json.dumps(audit,indent=2,ensure_ascii=False)+'\n')
    print(f'Dashboard: {output}')
    print(json.dumps({k:v for k,v in audit.items() if k!='cloud'},indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('csv', type=Path)
    parser.add_argument('--events',type=Path,help='Reviewed event extraction JSON; unmatched notes retain original text')
    parser.add_argument('--pdf-href',help='Relative path to an existing PDF')
    args = parser.parse_args()
    build(args.csv,events_path=args.events,pdf_href=args.pdf_href)
