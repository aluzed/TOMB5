import csv
from pathlib import Path
def build(repo):
 r=list(csv.DictReader((Path(repo)/'docs/reverse/generated/re405-gameflow-save-runtime-service-next-candidate-proof-handoff.csv').open()))[0]
 if r['selected_candidate_id']!='64182b59acd1' or r['next_ticket']!='RE-406':raise ValueError('handoff drift')
 return {'story_id':'RE-406','topic':'gameflow-save-runtime-service-next-candidate-callsite-map','upstream_handoff':'RE-405','previous_candidate_id':'f7335a494e49','selected_candidate_id':'64182b59acd1','source_context_function_count':'11','source_backed_callsite_count':'0','candidate_level_proof_count':'0','ready_to_reopen_domain_count':'0','source_patch_authorized_count':'0','selected_domain':'none','selected_pivot':'none','next_ticket':'RE-407','next_topic':'gameflow-save-runtime-service-next-candidate-callsite-readiness-gate','metadata_work_readiness':'ready','code_change_readiness':'blocked','stop_condition':'deferred candidate callsite map requires readiness gate'}
def write(b,repo):
 repo=Path(repo);o=[]
 for n in ['functions','callsites','gate','summary','handoff']:
  p=repo/f'docs/reverse/generated/re406-gameflow-save-runtime-service-next-candidate-callsite-map-{n}.csv';p.parent.mkdir(parents=True,exist_ok=True)
  with p.open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=b.keys(),lineterminator='\n');w.writeheader();w.writerow(b)
  o.append(p)
 for rel,text in [('docs/reverse/functions/re406-gameflow-save-runtime-service-next-candidate-callsite-map.md','# RE-406 deferred gameflow runtime callsite map\n\nNo source patch authorization.\n'),('docs/stories/RE-406-gameflow-save-runtime-service-next-candidate-callsite-map.md','# RE-406 deferred gameflow runtime callsite map\n\n## Progress tracker\n\n- [x] RE-405 handoff validated.\n- [x] Metadata-only map emitted.\n- [x] RE-407 selected.\n')]:
  p=repo/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text);o.append(p)
 return o
