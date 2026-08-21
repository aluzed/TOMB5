import csv
from pathlib import Path
def build(repo):
 r=list(csv.DictReader((Path(repo)/'docs/reverse/generated/re415-ghidra-second-window-candidate-narrow-export-handoff.csv').open()))[0]
 if r['selected_candidate_id']!='9d570ef9a5a7' or r['next_ticket']!='RE-416':raise ValueError('handoff drift')
 return {'story_id':'RE-416','topic':'collision-runtime-bridge-service-readiness-gate','upstream_handoff':'RE-415','selected_candidate_id':'9d570ef9a5a7','selected_subcluster':'collision-runtime-bridge-service','source_symbol_context_count':'8','candidate_level_proof_count':'0','ready_to_reopen_domain_count':'0','source_patch_authorized_count':'0','selected_domain':'none','selected_pivot':'none','next_ticket':'RE-417','next_topic':'collision-runtime-bridge-service-candidate-proof-export','metadata_work_readiness':'ready','code_change_readiness':'blocked','stop_condition':'collision/runtime bridge lacks candidate-level proof'}
def write(b,repo):
 repo=Path(repo);o=[]
 for n in ['gate','summary','handoff']:
  p=repo/f'docs/reverse/generated/re416-collision-runtime-bridge-service-readiness-gate-{n}.csv';p.parent.mkdir(parents=True,exist_ok=True)
  with p.open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=b.keys(),lineterminator='\n');w.writeheader();w.writerow(b)
  o.append(p)
 for rel,text in [('docs/reverse/functions/re416-collision-runtime-bridge-service-readiness-gate.md','# RE-416 collision/runtime bridge readiness gate\n\nNo candidate-level proof; source changes remain blocked.\n'),('docs/stories/RE-416-collision-runtime-bridge-service-readiness-gate.md','# RE-416 collision/runtime bridge readiness gate\n\n## Progress tracker\n\n- [x] RE-415 handoff validated.\n- [x] Candidate gated fail-closed.\n- [x] RE-417 selected.\n')]:
  p=repo/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text);o.append(p)
 return o
