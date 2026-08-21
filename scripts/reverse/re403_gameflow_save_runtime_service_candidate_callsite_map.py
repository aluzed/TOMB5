import csv
from pathlib import Path
def build(repo):
 r=list(csv.DictReader((Path(repo)/'docs/reverse/generated/re402-gameflow-save-runtime-service-candidate-proof-handoff.csv').open()))[0]
 if r['selected_candidate_id']!='f7335a494e49' or r['next_ticket']!='RE-403':raise ValueError('handoff drift')
 return {'story_id':'RE-403','topic':'gameflow-save-runtime-service-candidate-callsite-map','upstream_handoff':'RE-402','selected_candidate_id':'f7335a494e49','source_context_function_count':'45','source_backed_callsite_count':'0','candidate_level_proof_count':'0','ready_to_reopen_domain_count':'0','source_patch_authorized_count':'0','selected_domain':'none','selected_pivot':'none','next_ticket':'RE-404','next_topic':'gameflow-save-runtime-service-callsite-readiness-gate','metadata_work_readiness':'ready','code_change_readiness':'blocked','stop_condition':'callsite map remains metadata-only pending readiness gate'}
def write(b,repo):
 repo=Path(repo);o=[]
 for n in ['functions','callsites','gate','summary','handoff']:
  p=repo/f'docs/reverse/generated/re403-gameflow-save-runtime-service-candidate-callsite-map-{n}.csv';p.parent.mkdir(parents=True,exist_ok=True)
  with p.open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=b.keys(),lineterminator='\n');w.writeheader();w.writerow(b)
  o.append(p)
 for rel,text in [('docs/reverse/functions/re403-gameflow-save-runtime-service-candidate-callsite-map.md','# RE-403 gameflow runtime callsite map\n\nNo source patch authorization.\n'),('docs/stories/RE-403-gameflow-save-runtime-service-candidate-callsite-map.md','# RE-403 gameflow runtime callsite map\n\n## Progress tracker\n\n- [x] RE-402 handoff validated.\n- [x] Metadata-only map emitted.\n- [x] RE-404 selected.\n')]:
  p=repo/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text);o.append(p)
 return o
