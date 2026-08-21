import csv
from pathlib import Path
def build(repo):
 r=list(csv.DictReader((Path(repo)/'docs/reverse/generated/re420-ghidra-second-window-next-candidate-selection-handoff.csv').open()))[0]
 if r['selected_candidate_id']!='c2ed98ffa484' or r['next_ticket']!='RE-421':raise ValueError('handoff drift')
 return {'story_id':'RE-421','topic':'ghidra-second-window-rank-27-narrow-export','upstream_handoff':'RE-420','selected_candidate_id':'c2ed98ffa484','selected_rank':'27','selected_subcluster':'matrix-render-runtime-bridge-service','source_symbol_context_count':'10','bridge_class':'mapped-callee-bridge','candidate_level_proof_count':'0','ready_to_reopen_domain_count':'0','source_patch_authorized_count':'0','selected_domain':'none','selected_pivot':'none','next_ticket':'RE-422','next_topic':'matrix-render-runtime-bridge-service-readiness-gate','metadata_work_readiness':'ready','code_change_readiness':'blocked','stop_condition':'narrow rank-27 export requires gate before proof-domain selection'}
def write(b,repo):
 repo=Path(repo);o=[]
 for n in ['contexts','summary','handoff']:
  p=repo/f'docs/reverse/generated/re421-ghidra-second-window-rank-27-narrow-export-{n}.csv';p.parent.mkdir(parents=True,exist_ok=True)
  with p.open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=b.keys(),lineterminator='\n');w.writeheader();w.writerow(b)
  o.append(p)
 for rel,text in [('docs/reverse/functions/re421-ghidra-second-window-rank-27-narrow-export.md','# RE-421 rank-27 narrow export\n\nMatrix/render runtime bridge selected from safe symbolic context.\n'),('docs/stories/RE-421-ghidra-second-window-rank-27-narrow-export.md','# RE-421 rank-27 narrow export\n\n## Progress tracker\n\n- [x] RE-420 handoff validated.\n- [x] Rank-27 context narrowed.\n- [x] RE-422 selected.\n')]:
  p=repo/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text);o.append(p)
 return o
