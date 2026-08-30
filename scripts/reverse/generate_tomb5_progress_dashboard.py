import csv, html, re
from pathlib import Path

def build(repo):
 rows=[]
 for p in (Path(repo)/'docs/reverse/generated').glob('*handoff.csv'):
  try:
   r=next(csv.DictReader(p.open(encoding='utf-8')));m=re.fullmatch(r'RE-(\d+)',r.get('story_id',''))
   if m: rows.append((int(m.group(1)),r))
  except (OSError, StopIteration): pass
 rows.sort(); recent=[(n,r) for n,r in rows if n>=420]; n,last=rows[-1]
 return {
  'latest_ticket':f'RE-{n}',
  'next_ticket':last.get('next_ticket','TBD'),
  'next_topic':last.get('next_topic',''),
  'stop_condition':last.get('stop_condition',''),
  'recent_ticket_count':len(recent),
  'rows':recent,
 }

def write(model,repo):
 body=''.join(f'<tr><td>RE-{n}</td><td>{html.escape(r.get("topic",""))}</td><td>{html.escape(r.get("next_ticket",""))}</td><td>blocked</td></tr>' for n,r in model['rows'])
 text=f'''<!doctype html><html lang="fr"><meta charset="utf-8"><title>TOMB5 suivi</title><style>body{{font:15px monospace;background:#101514;color:#edf4ee;margin:auto;max-width:1200px;padding:32px}}table{{border-collapse:collapse;width:100%}}td,th{{padding:10px;border-bottom:1px solid #30433e;text-align:left}}.n{{font-size:32px;color:#b7f36a}}</style><h1>TOMB5 / Reconstruction tracker</h1><p class="n">{model['next_ticket']}</p><p>Prochain objectif à valider : {html.escape(model['next_topic'])}</p><p>Statut terminal : {html.escape(model['stop_condition'])}</p><h2>Historique &amp; reste à faire</h2><table><tr><th>Ticket</th><th>Étape</th><th>Suivant</th><th>Readiness</th></tr>{body}</table></html>'''
 out=Path(repo)/'docs/reverse/tomb5-progress-dashboard.html';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(text,encoding='utf-8');return out
