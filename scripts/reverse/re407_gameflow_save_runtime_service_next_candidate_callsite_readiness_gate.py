import csv
from pathlib import Path
def build(repo):
 r=list(csv.DictReader((Path(repo)/'docs/reverse/generated/re406-gameflow-save-runtime-service-next-candidate-callsite-map-handoff.csv').open()))[0]
 if r['selected_candidate_id']!='64182b59acd1' or r['next_ticket']!='RE-407':raise ValueError('handoff drift')
 return {'story_id':'RE-407','topic':'gameflow-save-runtime-service-next-candidate-callsite-readiness-gate','upstream_handoff':'RE-406','selected_candidate_id':'64182b59acd1','candidate_level_proof_count':'0','ready_to_reopen_domain_count':'0','source_patch_authorized_count':'0','selected_domain':'none','selected_pivot':'none','next_ticket':'RE-408','next_topic':'post-gameflow-save-runtime-next-ghidra-cluster-selection','metadata_work_readiness':'ready','code_change_readiness':'blocked','stop_condition':'gameflow/save/runtime queue exhausted without candidate-level proof'}
def write(b,repo):
 repo=Path(repo);o=[]
 for n in ['gate','summary','handoff']:
  p=repo/f'docs/reverse/generated/re407-gameflow-save-runtime-service-next-candidate-callsite-readiness-gate-{n}.csv';p.parent.mkdir(parents=True,exist_ok=True)
  with p.open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=b.keys(),lineterminator='\n');w.writeheader();w.writerow(b)
  o.append(p)
 for rel,text in [('docs/reverse/functions/re407-gameflow-save-runtime-service-next-candidate-callsite-readiness-gate.md','# RE-407 gameflow runtime final readiness gate\n\nQueue exhausted without proof.\n'),('docs/stories/RE-407-gameflow-save-runtime-service-next-candidate-callsite-readiness-gate.md','# RE-407 gameflow runtime final readiness gate\n\n## Progress tracker\n\n- [x] RE-406 handoff validated.\n- [x] Final candidate blocked.\n- [x] RE-408 selected.\n')]:
  p=repo/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text);o.append(p)
 return o
