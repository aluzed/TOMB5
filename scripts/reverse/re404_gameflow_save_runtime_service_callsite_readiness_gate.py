import csv
from pathlib import Path
def build(repo):
 r=list(csv.DictReader((Path(repo)/'docs/reverse/generated/re403-gameflow-save-runtime-service-candidate-callsite-map-handoff.csv').open()))[0]
 if r['selected_candidate_id']!='f7335a494e49' or r['next_ticket']!='RE-404':raise ValueError('handoff drift')
 return {'story_id':'RE-404','topic':'gameflow-save-runtime-service-callsite-readiness-gate','upstream_handoff':'RE-403','selected_candidate_id':'f7335a494e49','candidate_level_proof_count':'0','ready_to_reopen_domain_count':'0','source_patch_authorized_count':'0','selected_domain':'none','selected_pivot':'none','next_ticket':'RE-405','next_topic':'gameflow-save-runtime-service-next-candidate-proof-export','metadata_work_readiness':'ready','code_change_readiness':'blocked','stop_condition':'first gameflow runtime candidate closed without proof; inspect deferred candidate'}
def write(b,repo):
 repo=Path(repo);o=[]
 for n in ['gate','summary','handoff']:
  p=repo/f'docs/reverse/generated/re404-gameflow-save-runtime-service-callsite-readiness-gate-{n}.csv';p.parent.mkdir(parents=True,exist_ok=True)
  with p.open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=b.keys(),lineterminator='\n');w.writeheader();w.writerow(b)
  o.append(p)
 for rel,text in [('docs/reverse/functions/re404-gameflow-save-runtime-service-callsite-readiness-gate.md','# RE-404 gameflow runtime readiness gate\n\nNo candidate-level proof; select deferred candidate.\n'),('docs/stories/RE-404-gameflow-save-runtime-service-callsite-readiness-gate.md','# RE-404 gameflow runtime readiness gate\n\n## Progress tracker\n\n- [x] RE-403 handoff validated.\n- [x] Candidate blocked.\n- [x] RE-405 selected.\n')]:
  p=repo/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text);o.append(p)
 return o
