import csv
from pathlib import Path
def build(repo):
 r=list(csv.DictReader((Path(repo)/'docs/reverse/generated/re424-matrix-render-runtime-bridge-service-candidate-callsite-map-handoff.csv').open()))[0]
 if r['selected_candidate_id']!='c2ed98ffa484' or r['next_ticket']!='RE-425':raise ValueError('handoff drift')
 return {'story_id':'RE-425','topic':'matrix-render-runtime-bridge-service-callsite-readiness-gate','upstream_handoff':'RE-424','selected_candidate_id':'c2ed98ffa484','source_backed_callsite_count':'0','candidate_level_proof_count':'0','ready_to_reopen_domain_count':'0','source_patch_authorized_count':'0','selected_domain':'none','selected_pivot':'none','next_ticket':'RE-426','next_topic':'ghidra-second-window-next-candidate-selection','metadata_work_readiness':'ready','code_change_readiness':'blocked','stop_condition':'rank-27 candidate closed fail-closed; select rank 28'}
def write(b,repo):
 repo=Path(repo);o=[]
 for n in ['gate','summary','handoff']:
  p=repo/f'docs/reverse/generated/re425-matrix-render-runtime-bridge-service-callsite-readiness-gate-{n}.csv';p.parent.mkdir(parents=True,exist_ok=True)
  with p.open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=b.keys(),lineterminator='\n');w.writeheader();w.writerow(b)
  o.append(p)
 for rel,text in [('docs/reverse/functions/re425-matrix-render-runtime-bridge-service-callsite-readiness-gate.md','# RE-425 matrix/render bridge callsite readiness gate\n\nRank-27 candidate closed without proof.\n'),('docs/stories/RE-425-matrix-render-runtime-bridge-service-callsite-readiness-gate.md','# RE-425 matrix/render bridge callsite readiness gate\n\n## Progress tracker\n\n- [x] RE-424 handoff validated.\n- [x] Candidate closed fail-closed.\n- [x] RE-426 selected.\n')]:
  p=repo/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text);o.append(p)
 return o
