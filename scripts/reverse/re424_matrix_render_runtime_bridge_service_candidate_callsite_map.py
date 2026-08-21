import csv
from pathlib import Path
def build(repo):
 r=list(csv.DictReader((Path(repo)/'docs/reverse/generated/re423-matrix-render-runtime-bridge-service-candidate-proof-handoff.csv').open()))[0]
 if r['selected_candidate_id']!='c2ed98ffa484' or r['next_ticket']!='RE-424':raise ValueError('handoff drift')
 return {'story_id':'RE-424','topic':'matrix-render-runtime-bridge-service-candidate-callsite-map','upstream_handoff':'RE-423','selected_candidate_id':'c2ed98ffa484','source_context_function_count':'10','source_backed_callsite_count':'0','candidate_level_proof_count':'0','ready_to_reopen_domain_count':'0','source_patch_authorized_count':'0','selected_domain':'none','selected_pivot':'none','next_ticket':'RE-425','next_topic':'matrix-render-runtime-bridge-service-callsite-readiness-gate','metadata_work_readiness':'ready','code_change_readiness':'blocked','stop_condition':'no safe source-backed candidate callsite in metadata-only map'}
def write(b,repo):
 repo=Path(repo);o=[]
 for n in ['callsites','summary','handoff']:
  p=repo/f'docs/reverse/generated/re424-matrix-render-runtime-bridge-service-candidate-callsite-map-{n}.csv';p.parent.mkdir(parents=True,exist_ok=True)
  with p.open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=b.keys(),lineterminator='\n');w.writeheader();w.writerow(b)
  o.append(p)
 for rel,text in [('docs/reverse/functions/re424-matrix-render-runtime-bridge-service-candidate-callsite-map.md','# RE-424 matrix/render bridge callsite map\n\nNo candidate-level callsites are claimed.\n'),('docs/stories/RE-424-matrix-render-runtime-bridge-service-candidate-callsite-map.md','# RE-424 matrix/render bridge callsite map\n\n## Progress tracker\n\n- [x] RE-423 handoff validated.\n- [x] Metadata-only map emitted.\n- [x] RE-425 selected.\n')]:
  p=repo/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text);o.append(p)
 return o
