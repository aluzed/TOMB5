import csv
from pathlib import Path
def build(repo):
 r=list(csv.DictReader((Path(repo)/'docs/reverse/generated/re421-ghidra-second-window-rank-27-narrow-export-handoff.csv').open()))[0]
 if r['selected_candidate_id']!='c2ed98ffa484' or r['next_ticket']!='RE-422':raise ValueError('handoff drift')
 return {'story_id':'RE-422','topic':'matrix-render-runtime-bridge-service-readiness-gate','upstream_handoff':'RE-421','selected_candidate_id':'c2ed98ffa484','selected_subcluster':'matrix-render-runtime-bridge-service','source_symbol_context_count':'10','candidate_level_proof_count':'0','ready_to_reopen_domain_count':'0','source_patch_authorized_count':'0','selected_domain':'none','selected_pivot':'none','next_ticket':'RE-423','next_topic':'matrix-render-runtime-bridge-service-candidate-proof-export','metadata_work_readiness':'ready','code_change_readiness':'blocked','stop_condition':'matrix/render callee bridge remains prioritization signal without candidate proof'}
def write(b,repo):
 repo=Path(repo);o=[]
 for n in ['gate','summary','handoff']:
  p=repo/f'docs/reverse/generated/re422-matrix-render-runtime-bridge-service-readiness-gate-{n}.csv';p.parent.mkdir(parents=True,exist_ok=True)
  with p.open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=b.keys(),lineterminator='\n');w.writeheader();w.writerow(b)
  o.append(p)
 for rel,text in [('docs/reverse/functions/re422-matrix-render-runtime-bridge-service-readiness-gate.md','# RE-422 matrix/render bridge readiness gate\n\nCandidate proof absent; source changes blocked.\n'),('docs/stories/RE-422-matrix-render-runtime-bridge-service-readiness-gate.md','# RE-422 matrix/render bridge readiness gate\n\n## Progress tracker\n\n- [x] RE-421 handoff validated.\n- [x] Candidate blocked.\n- [x] RE-423 selected.\n')]:
  p=repo/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text);o.append(p)
 return o
