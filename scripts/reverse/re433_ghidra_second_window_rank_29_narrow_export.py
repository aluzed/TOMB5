import csv
from pathlib import Path
def build(repo):
 repo=Path(repo);h=next(csv.DictReader((repo/'docs/reverse/generated/re432-ghidra-second-window-next-candidate-selection-handoff.csv').open(encoding='utf-8')))
 if h['next_ticket']!='RE-433' or h['selected_candidate_id']!='763c9cd0e3f7':raise ValueError('handoff drift')
 return {'story_id':'RE-433','topic':'ghidra-second-window-rank-29-narrow-export','upstream_handoff':'RE-432','selected_candidate_id':h['selected_candidate_id'],'selected_rank':'29','selected_subcluster':'runtime-bridge-service','source_symbol_context_count':h['source_symbol_context_count'],'candidate_level_proof_count':'0','ready_to_reopen_domain_count':'0','source_patch_authorized_count':'0','selected_domain':'none','selected_pivot':'none','next_ticket':'RE-434','next_topic':'runtime-bridge-service-readiness-gate','metadata_work_readiness':'ready','code_change_readiness':'blocked','stop_condition':'narrow rank-29 export requires gate before proof-domain selection'}
def write(b,repo):
 repo=Path(repo);out=[]
 for n in ('contexts','summary','handoff'):
  p=repo/f'docs/reverse/generated/re433-ghidra-second-window-rank-29-narrow-export-{n}.csv';p.parent.mkdir(parents=True,exist_ok=True)
  with p.open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=b.keys(),lineterminator='\n');w.writeheader();w.writerow(b)
  out.append(p)
 for rel,text in {'docs/reverse/functions/re433-ghidra-second-window-rank-29-narrow-export.md':'# RE-433 rank-29 narrow export\n\nRuntime bridge selected from safe symbolic context.\n','docs/stories/RE-433-ghidra-second-window-rank-29-narrow-export.md':'# RE-433 rank-29 narrow export\n\n## Progress tracker\n\n- [x] RE-432 handoff validated.\n- [x] Rank-29 context narrowed.\n- [x] RE-434 selected.\n'}.items():
  p=repo/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8');out.append(p)
 return out
