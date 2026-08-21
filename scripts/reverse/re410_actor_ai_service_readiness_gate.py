import csv
from pathlib import Path
def build(repo):
 r=list(csv.DictReader((Path(repo)/'docs/reverse/generated/re409-ghidra-actor-ai-cluster-narrow-export-handoff.csv').open()))[0]
 if r['selected_candidate_id']!='bcfb623df366' or r['next_ticket']!='RE-410':raise ValueError('handoff drift')
 return {'story_id':'RE-410','topic':'actor-ai-service-readiness-gate','upstream_handoff':'RE-409','selected_candidate_id':'bcfb623df366','candidate_level_proof_count':'0','ready_to_reopen_domain_count':'0','source_patch_authorized_count':'0','selected_domain':'none','selected_pivot':'none','next_ticket':'RE-411','next_topic':'actor-ai-service-candidate-proof-export','metadata_work_readiness':'ready','code_change_readiness':'blocked','stop_condition':'actor AI candidate lacks candidate-level proof'}
def write(b,repo):
 repo=Path(repo);o=[]
 for n in ['gate','summary','handoff']:
  p=repo/f'docs/reverse/generated/re410-actor-ai-service-readiness-gate-{n}.csv';p.parent.mkdir(parents=True,exist_ok=True)
  with p.open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=b.keys(),lineterminator='\n');w.writeheader();w.writerow(b)
  o.append(p)
 for rel,text in [('docs/reverse/functions/re410-actor-ai-service-readiness-gate.md','# RE-410 actor AI readiness gate\n\nCandidate proof absent; code blocked.\n'),('docs/stories/RE-410-actor-ai-service-readiness-gate.md','# RE-410 actor AI readiness gate\n\n## Progress tracker\n\n- [x] RE-409 handoff validated.\n- [x] Proof denied.\n- [x] RE-411 selected.\n')]:
  p=repo/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text);o.append(p)
 return o
