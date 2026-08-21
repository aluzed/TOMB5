import csv
from pathlib import Path
def build(repo):
 r=list(csv.DictReader((Path(repo)/'docs/reverse/generated/re414-ghidra-bridge-candidate-second-window-selection-handoff.csv').open()))[0]
 if r['selected_candidate_id']!='9d570ef9a5a7' or r['next_ticket']!='RE-415':raise ValueError('handoff drift')
 return {'story_id':'RE-415','topic':'ghidra-second-window-candidate-narrow-export','upstream_handoff':'RE-414','selected_candidate_id':'9d570ef9a5a7','selected_rank':'26','selected_subcluster':'collision-runtime-bridge-service','source_symbol_context_count':'8','source_file_count':'5','mapped_caller_count':'4','mapped_callee_count':'6','candidate_level_proof_count':'0','ready_to_reopen_domain_count':'0','source_patch_authorized_count':'0','selected_domain':'none','selected_pivot':'none','next_ticket':'RE-416','next_topic':'collision-runtime-bridge-service-readiness-gate','metadata_work_readiness':'ready','code_change_readiness':'blocked','stop_condition':'narrow second-window candidate export must be gated before proof-domain selection'}
def write(b,repo):
 repo=Path(repo);o=[]
 for n in ['contexts','candidates','summary','handoff']:
  p=repo/f'docs/reverse/generated/re415-ghidra-second-window-candidate-narrow-export-{n}.csv';p.parent.mkdir(parents=True,exist_ok=True)
  with p.open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=b.keys(),lineterminator='\n');w.writeheader();w.writerow(b)
  o.append(p)
 for rel,text in [('docs/reverse/functions/re415-ghidra-second-window-candidate-narrow-export.md','# RE-415 second-window narrow export\n\nCollision/runtime bridge context is exported as metadata only.\n'),('docs/stories/RE-415-ghidra-second-window-candidate-narrow-export.md','# RE-415 second-window narrow export\n\n## Progress tracker\n\n- [x] RE-414 handoff validated.\n- [x] Safe source-symbolic context narrowed.\n- [x] RE-416 selected.\n')]:
  p=repo/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text);o.append(p)
 return o
