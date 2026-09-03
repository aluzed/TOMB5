import csv, html, re, unicodedata
from pathlib import Path

TERMINAL_HANDOFF_FLOOR = 420
TERMINAL_PREDECESSOR_REQUIRED_FLOOR = 725
TERMINAL_PREDECESSOR_EXISTENCE_REQUIRED_FLOOR = 726
TERMINAL_PREDECESSOR_DIRECTION_REQUIRED_FLOOR = 727
TERMINAL_PREDECESSOR_STOP_CONDITION_REQUIRED_FLOOR = 728
TERMINAL_REQUIRED_FIELDS = ('story_id', 'topic', 'next_ticket', 'next_topic', 'stop_condition')
TERMINAL_STOP_PLACEHOLDERS = frozenset({'-', '?', 'n/a', 'na', 'none', 'tbd', 'unknown'})
TERMINAL_TOPIC_PLACEHOLDERS = frozenset({'-', '?', 'n/a', 'na', 'none', 'tbd', 'unknown'})

def _has_unsafe_terminal_format_characters(value):
 return any(unicodedata.category(character) in {'Cc', 'Cf', 'Zl', 'Zp'} for character in value)

def _read_handoff(path):
 with path.open(encoding='utf-8', newline='') as handle:
  reader=csv.DictReader(handle)
  rows=list(reader)
 if (not reader.fieldnames or len(reader.fieldnames) != len(set(reader.fieldnames))
     or len(rows)!=1 or any(None in row or None in row.values() for row in rows)):
  raise ValueError(f'invalid handoff: {path.name}')
 match=re.fullmatch(r're(\d+)-.+-handoff\.csv',path.name)
 if not match: raise ValueError(f'invalid handoff filename: {path.name}')
 row=rows[0];story_id=row.get('story_id')
 if story_id and story_id != f'RE-{match.group(1)}': raise ValueError(f'invalid handoff story_id: {path.name}')
 return int(match.group(1)),row

def build(repo):
 rows=[]
 terminal_ticket_paths={}
 for p in (Path(repo)/'docs/reverse/generated').glob('*handoff.csv'):
  try:
   n,row=_read_handoff(p)
  except (OSError, UnicodeDecodeError, csv.Error) as error: raise ValueError(f'unreadable handoff: {p.name}') from error
  if n >= TERMINAL_HANDOFF_FLOOR and row.get('story_id') != f'RE-{n}':
   raise ValueError(f'invalid handoff story_id: {p.name}')
  if n >= TERMINAL_HANDOFF_FLOOR:
   required_fields = TERMINAL_REQUIRED_FIELDS + (('predecessor',) if n >= TERMINAL_PREDECESSOR_REQUIRED_FLOOR else ())
   missing=next((field for field in required_fields if not row.get(field, '').strip()),None)
   if missing: raise ValueError(f'incomplete terminal handoff {missing}: {p.name}')
   if 'predecessor' in row:
    if row['predecessor'] != f'RE-{n - 1}':
     raise ValueError(f'incoherent terminal handoff predecessor: {p.name}')
   if row['topic'].strip().casefold() in TERMINAL_TOPIC_PLACEHOLDERS:
    raise ValueError(f'unmeaningful terminal handoff topic: {p.name}')
   if row['stop_condition'].strip().casefold() in TERMINAL_STOP_PLACEHOLDERS:
    raise ValueError(f'unmeaningful terminal handoff stop_condition: {p.name}')
   control_field=next((field for field in TERMINAL_REQUIRED_FIELDS
                       if _has_unsafe_terminal_format_characters(row[field])),None)
   if control_field:
    raise ValueError(f'unsafe terminal handoff {control_field}: {p.name}')
   next_ticket=row['next_ticket'];next_topic=row['next_topic']
   if next_ticket != 'TBD' and not re.fullmatch(r'RE-[1-9]\d*',next_ticket):
    raise ValueError(f'invalid terminal handoff next_ticket: {p.name}')
   if (next_ticket == 'TBD') != (next_topic == 'none'):
    raise ValueError(f'incoherent terminal handoff direction: {p.name}')
   if next_ticket != 'TBD' and int(next_ticket[3:]) != n + 1:
    raise ValueError(f'non-successor terminal handoff next_ticket: {p.name}')
  if n >= TERMINAL_HANDOFF_FLOOR and n in terminal_ticket_paths:
   raise ValueError(f'ambiguous terminal handoff ticket: RE-{n}')
  if n >= TERMINAL_HANDOFF_FLOOR: terminal_ticket_paths[n]=p
  rows.append((n,row))
 if not rows: raise ValueError('no valid handoff')
 for n,row in rows:
  if n >= TERMINAL_PREDECESSOR_EXISTENCE_REQUIRED_FLOOR and n - 1 not in terminal_ticket_paths:
   raise ValueError(f'missing terminal handoff predecessor: RE-{n - 1}')
  if (n >= TERMINAL_PREDECESSOR_DIRECTION_REQUIRED_FLOOR
      and terminal_ticket_paths[n - 1]):
   predecessor_row=next(candidate for ticket,candidate in rows if ticket == n - 1)
   if predecessor_row.get('next_ticket') != f'RE-{n}':
    raise ValueError(f'incoherent terminal handoff predecessor direction: RE-{n - 1}')
   if (n >= TERMINAL_PREDECESSOR_STOP_CONDITION_REQUIRED_FLOOR
       and predecessor_row.get('stop_condition') != row.get('stop_condition')):
    raise ValueError(f'incoherent terminal handoff predecessor stop_condition: RE-{n - 1}')
 rows.sort(key=lambda item: item[0]); recent=[(n,r) for n,r in rows if n>=TERMINAL_HANDOFF_FLOOR]; n,last=rows[-1]
 if n >= TERMINAL_HANDOFF_FLOOR and last['next_ticket'] != 'TBD' and int(last['next_ticket'][3:]) not in terminal_ticket_paths:
  raise ValueError(f'dangling latest terminal handoff successor: RE-{n}')
 return {
  'latest_ticket':f'RE-{n}',
  'next_ticket':last.get('next_ticket','TBD'),
  'next_topic':last.get('next_topic',''),
  'stop_condition':last.get('stop_condition',''),
  'history_heading': ('Historique clôturé — aucun backlog actif'
                      if (last.get('next_ticket', 'TBD') == 'TBD'
                          and last.get('next_topic', '') == 'none'
                          and last.get('stop_condition', ''))
                      else ('État terminal incomplet — validation requise'
                            if last.get('next_ticket', 'TBD') == 'TBD'
                            else 'Historique & reste à faire')),
  'recent_ticket_count':len(recent),
  'rows':recent,
 }

def write(model,repo):
 body=''.join(f'<tr><td>RE-{n}</td><td>{html.escape(r.get("topic",""))}</td><td>{html.escape(r.get("next_ticket",""))}</td><td>blocked</td></tr>' for n,r in model['rows'])
 text=f'''<!doctype html><html lang="fr"><meta charset="utf-8"><title>TOMB5 suivi</title><style>body{{font:15px monospace;background:#101514;color:#edf4ee;margin:auto;max-width:1200px;padding:32px}}table{{border-collapse:collapse;width:100%}}td,th{{padding:10px;border-bottom:1px solid #30433e;text-align:left}}.n{{font-size:32px;color:#b7f36a}}</style><h1>TOMB5 / Reconstruction tracker</h1><p class="n">{html.escape(model['next_ticket'])}</p><p>Prochain objectif à valider : {html.escape(model['next_topic'])}</p><p>Statut terminal : {html.escape(model['stop_condition'])}</p><h2>{html.escape(model['history_heading'])}</h2><table><tr><th>Ticket</th><th>Étape</th><th>Suivant</th><th>Readiness</th></tr>{body}</table></html>'''
 out=Path(repo)/'docs/reverse/tomb5-progress-dashboard.html';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(text,encoding='utf-8');return out
