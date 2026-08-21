import csv
from pathlib import Path
def build(repo):
 r=list(csv.DictReader((Path(repo)/'docs/reverse/generated/re422-matrix-render-runtime-bridge-service-readiness-gate-handoff.csv').open()))[0]
 if r['selected_candidate_id']!='c2ed98ffa484' or r['next_ticket']!='RE-423':raise ValueError('handoff drift')
 return {'story_id':'RE-423','topic':'matrix-render-runtime-bridge-service-candidate-proof-export','upstream_handoff':'RE-422','selected_candidate_id':'c2ed98ffa484','source_symbol_context_count':'10','candidate_level_proof_count':'0','repository_symbol_direct_proof_count':'0','ready_to_reopen_domain_count':'0','source_patch_authorized_count':'0','selected_domain':'none','selected_pivot':'none','next_ticket':'RE-424','next_topic':'matrix-render-runtime-bridge-service-candidate-callsite-map','metadata_work_readiness':'ready','code_change_readiness':'blocked','stop_condition':'matrix/render symbolic context has no direct candidate proof'}
def write(b,repo):
 repo=Path(repo);o=[]
 for n in ['contexts','summary','handoff']:
  p=repo/f'docs/reverse/generated/re423-matrix-render-runtime-bridge-service-candidate-proof-{n}.csv';p.parent.mkdir(parents=True,exist_ok=True)
  with p.open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=b.keys(),lineterminator='\n');w.writeheader();w.writerow(b)
  o.append(p)
 for rel,text in [('docs/reverse/functions/re423-matrix-render-runtime-bridge-service-candidate-proof-export.md','# RE-423 matrix/render bridge proof export\n\nNo direct candidate proof is available.\n'),('docs/stories/RE-423-matrix-render-runtime-bridge-service-candidate-proof-export.md','# RE-423 matrix/render bridge proof export\n\n## Progress tracker\n\n- [x] RE-422 handoff validated.\n- [x] Context export completed.\n- [x] RE-424 selected.\n')]:
  p=repo/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text);o.append(p)
 return o
