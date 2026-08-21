import csv
from pathlib import Path
from scripts.reverse import re309_ghidra_unmapped_bridge_candidates as re309

def build(repo):
 repo=Path(repo); h=list(csv.DictReader((repo/'docs/reverse/generated/re413-actor-ai-service-callsite-readiness-gate-handoff.csv').open()))[0]
 if h['next_ticket']!='TBD' or h['next_topic']!='actor-ai-cluster-exhausted': raise ValueError('RE-413 handoff drift')
 old=re309.TOP_LIMIT
 try:
  re309.TOP_LIMIT=50; rows,_=re309.build_bridge_candidates(repo)
 finally: re309.TOP_LIMIT=old
 selected=next(r for r in rows if r.rank==26)
 return {'story_id':'RE-414','topic':'ghidra-bridge-candidate-second-window-selection','upstream_handoff':'RE-413','prior_window_status':'exhausted-fail-closed','candidate_window_start':'26','candidate_window_end':'50','selected_rank':str(selected.rank),'selected_candidate_id':selected.candidate_id,'selected_source_context_count':str(selected.source_context_count),'selected_bridge_class':selected.bridge_class,'ready_to_reopen_domain_count':'0','source_patch_authorized_count':'0','selected_domain':'none','selected_pivot':'none','next_ticket':'RE-415','next_topic':'ghidra-second-window-candidate-narrow-export','metadata_work_readiness':'ready','code_change_readiness':'blocked','stop_condition':'second ranked window selected after all first-window candidates exhausted'}
def write(b,repo):
 repo=Path(repo); o=[]
 for n in ['candidates','summary','handoff']:
  p=repo/f'docs/reverse/generated/re414-ghidra-bridge-candidate-second-window-selection-{n}.csv';p.parent.mkdir(parents=True,exist_ok=True)
  with p.open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=b.keys(),lineterminator='\n');w.writeheader();w.writerow(b)
  o.append(p)
 for rel,text in [('docs/reverse/functions/re414-ghidra-bridge-candidate-second-window-selection.md','# RE-414 second Ghidra bridge candidate window\n\nThe initial 25-candidate window is exhausted fail-closed. Rank 26 is selected from a recomputed safe source-symbolic export.\n'),('docs/stories/RE-414-ghidra-bridge-candidate-second-window-selection.md','# RE-414 second Ghidra bridge candidate window\n\n## Progress tracker\n\n- [x] RE-413 exhaustion handoff validated.\n- [x] Candidate ranks 26–50 recomputed from safe metadata.\n- [x] Rank 26 selected for narrow export.\n')]:
  p=repo/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text);o.append(p)
 return o
