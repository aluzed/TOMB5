import csv
from pathlib import Path

def build(repo):
 r=list(csv.DictReader((Path(repo)/'docs/reverse/generated/re400-ghidra-gameflow-save-runtime-cluster-narrow-export-handoff.csv').open()))[0]
 if r['selected_candidate_id']!='f7335a494e49' or r['next_ticket']!='RE-401':raise ValueError('handoff drift')
 return {'story_id':'RE-401','topic':'gameflow-save-runtime-service-readiness-gate','upstream_handoff':'RE-400','selected_candidate_id':'f7335a494e49','candidate_level_proof_count':'0','ready_to_reopen_domain_count':'0','source_patch_authorized_count':'0','selected_domain':'none','selected_pivot':'none','next_ticket':'RE-402','next_topic':'gameflow-save-runtime-service-candidate-proof-export','metadata_work_readiness':'ready','code_change_readiness':'blocked','stop_condition':'candidate lacks candidate-level proof'}
def write(b,repo):
 repo=Path(repo);p=repo/'docs/reverse/generated/re401-gameflow-save-runtime-service-readiness-gate-handoff.csv';p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=b.keys(),lineterminator='\n');w.writeheader();w.writerow(b)
 for rel,text in [('docs/reverse/functions/re401-gameflow-save-runtime-service-readiness-gate.md','# RE-401 gameflow save runtime readiness gate\n\nCandidate-level proof is absent; code remains blocked.\n'),('docs/stories/RE-401-gameflow-save-runtime-service-readiness-gate.md','# RE-401 gameflow save runtime readiness gate\n\n## Progress tracker\n\n- [x] RE-400 handoff validated.\n- [x] Proof denied fail-closed.\n- [x] RE-402 selected.\n')]:
  q=repo/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(text)
 return p
