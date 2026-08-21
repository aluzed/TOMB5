import csv
from pathlib import Path
def build(repo):
 r=list(csv.DictReader((Path(repo)/'docs/reverse/generated/re404-gameflow-save-runtime-service-callsite-readiness-gate-handoff.csv').open()))[0]
 if r['next_ticket']!='RE-405':raise ValueError('handoff drift')
 return {'story_id':'RE-405','topic':'gameflow-save-runtime-service-next-candidate-proof-export','upstream_handoff':'RE-404','previous_candidate_id':'f7335a494e49','selected_candidate_id':'64182b59acd1','source_symbol_context_count':'11','candidate_level_proof_count':'0','ready_to_reopen_domain_count':'0','source_patch_authorized_count':'0','selected_domain':'none','selected_pivot':'none','next_ticket':'RE-406','next_topic':'gameflow-save-runtime-service-next-candidate-callsite-map','metadata_work_readiness':'ready','code_change_readiness':'blocked','stop_condition':'deferred candidate lacks direct proof'}
def write(b,repo):
 repo=Path(repo);o=[]
 for n in ['contexts','proof-gate','summary','handoff']:
  p=repo/f'docs/reverse/generated/re405-gameflow-save-runtime-service-next-candidate-proof-{n}.csv';p.parent.mkdir(parents=True,exist_ok=True)
  with p.open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=b.keys(),lineterminator='\n');w.writeheader();w.writerow(b)
  o.append(p)
 for rel,text in [('docs/reverse/functions/re405-gameflow-save-runtime-service-next-candidate-proof-export.md','# RE-405 deferred gameflow runtime candidate proof export\n\nReadiness remains blocked.\n'),('docs/stories/RE-405-gameflow-save-runtime-service-next-candidate-proof-export.md','# RE-405 deferred gameflow runtime candidate proof export\n\n## Progress tracker\n\n- [x] RE-404 handoff validated.\n- [x] Deferred candidate selected.\n- [x] RE-406 selected.\n')]:
  p=repo/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text);o.append(p)
 return o
