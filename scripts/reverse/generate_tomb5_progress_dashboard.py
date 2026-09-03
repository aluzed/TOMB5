import csv, html, re
from pathlib import Path

TERMINAL_HANDOFF_FLOOR = 420
TERMINAL_REQUIRED_FIELDS = ('story_id', 'topic', 'next_ticket', 'next_topic')

def _read_handoff(path):
 with path.open(encoding='utf-8', newline='') as handle:
  reader=csv.DictReader(handle)
  rows=list(reader)
 if not reader.fieldnames or len(rows)!=1 or any(None in row or None in row.values() for row in rows):
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
   missing=next((field for field in TERMINAL_REQUIRED_FIELDS if not row.get(field)),None)
   if missing: raise ValueError(f'incomplete terminal handoff {missing}: {p.name}')
  if n >= TERMINAL_HANDOFF_FLOOR and n in terminal_ticket_paths:
   raise ValueError(f'ambiguous terminal handoff ticket: RE-{n}')
  if n >= TERMINAL_HANDOFF_FLOOR: terminal_ticket_paths[n]=p
  rows.append((n,row))
 if not rows: raise ValueError('no valid handoff')
 rows.sort(key=lambda item: item[0]); recent=[(n,r) for n,r in rows if n>=TERMINAL_HANDOFF_FLOOR]; n,last=rows[-1]
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
 text=f'''<!doctype html><html lang="fr"><meta charset="utf-8"><title>TOMB5 suivi</title><style>body{{font:15px monospace;background:#101514;color:#edf4ee;margin:auto;max-width:1200px;padding:32px}}table{{border-collapse:collapse;width:100%}}td,th{{padding:10px;border-bottom:1px solid #30433e;text-align:left}}.n{{font-size:32px;color:#b7f36a}}</style><h1>TOMB5 / Reconstruction tracker</h1><p class="n">{model['next_ticket']}</p><p>Prochain objectif à valider : {html.escape(model['next_topic'])}</p><p>Statut terminal : {html.escape(model['stop_condition'])}</p><h2>{html.escape(model['history_heading'])}</h2><table><tr><th>Ticket</th><th>Étape</th><th>Suivant</th><th>Readiness</th></tr>{body}</table></html>'''
 out=Path(repo)/'docs/reverse/tomb5-progress-dashboard.html';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(text,encoding='utf-8');return out
