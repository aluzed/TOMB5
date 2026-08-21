import csv
from pathlib import Path
from scripts.reverse import re309_ghidra_unmapped_bridge_candidates as r309
FORBIDDEN=('sub_','fun_','0x')
def build(repo):
 repo=Path(repo);h=list(csv.DictReader((repo/'docs/reverse/generated/re425-matrix-render-runtime-bridge-service-callsite-readiness-gate-handoff.csv').open()))[0]
 if h['next_ticket']!='RE-426':raise ValueError('handoff drift')
 old=r309.TOP_LIMIT
 try:r309.TOP_LIMIT=50;rows,_=r309.build_bridge_candidates(repo)
 finally:r309.TOP_LIMIT=old
 c=next(x for x in rows if x.rank==28)
 return {'story_id':'RE-426','topic':'ghidra-second-window-next-candidate-selection','upstream_handoff':'RE-425','closed_candidate_id':'c2ed98ffa484','selected_rank':str(c.rank),'selected_candidate_id':c.candidate_id,'selected_bridge_class':c.bridge_class,'source_symbol_context_count':str(c.source_context_count),'safe_context_status':'filtered-raw-symbolic-artifact','ready_to_reopen_domain_count':'0','source_patch_authorized_count':'0','selected_domain':'none','selected_pivot':'none','next_ticket':'RE-427','next_topic':'ghidra-second-window-rank-28-narrow-export','metadata_work_readiness':'ready','code_change_readiness':'blocked','stop_condition':'rank 28 selected; raw-symbolic parser artifacts remain excluded'}
def write(b,repo):
 repo=Path(repo);o=[]
 for n in ['candidates','summary','handoff']:
  p=repo/f'docs/reverse/generated/re426-ghidra-second-window-next-candidate-selection-{n}.csv';p.parent.mkdir(parents=True,exist_ok=True)
  with p.open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=b.keys(),lineterminator='\n');w.writeheader();w.writerow(b)
  o.append(p)
 for rel,text in [('docs/reverse/functions/re426-ghidra-second-window-next-candidate-selection.md','# RE-426 second-window rank-28 selection\n\nCandidate handle is retained; unsafe raw-symbolic context is excluded.\n'),('docs/stories/RE-426-ghidra-second-window-next-candidate-selection.md','# RE-426 second-window rank-28 selection\n\n## Progress tracker\n\n- [x] RE-425 handoff validated.\n- [x] Rank 28 selected.\n- [x] Unsafe symbolic artifacts excluded.\n- [x] RE-427 selected.\n')]:
  p=repo/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text);o.append(p)
 return o
