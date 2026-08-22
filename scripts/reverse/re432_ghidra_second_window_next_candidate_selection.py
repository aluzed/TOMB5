import csv
from pathlib import Path
from scripts.reverse import re309_ghidra_unmapped_bridge_candidates as r309
def build(repo):
 repo=Path(repo);h=next(csv.DictReader((repo/'docs/reverse/generated/re431-audio-death-runtime-bridge-service-callsite-readiness-gate-handoff.csv').open(encoding='utf-8')))
 if h['next_ticket']!='RE-432':raise ValueError('handoff drift')
 old=r309.TOP_LIMIT
 try:r309.TOP_LIMIT=50;rows,_=r309.build_bridge_candidates(repo)
 finally:r309.TOP_LIMIT=old
 c=next(x for x in rows if x.rank==29)
 return {'story_id':'RE-432','topic':'ghidra-second-window-next-candidate-selection','upstream_handoff':'RE-431','closed_candidate_id':'61b63f61c1fd','selected_rank':str(c.rank),'selected_candidate_id':c.candidate_id,'selected_bridge_class':c.bridge_class,'source_symbol_context_count':str(c.source_context_count),'safe_context_status':'filtered-raw-symbolic-artifact','ready_to_reopen_domain_count':'0','source_patch_authorized_count':'0','selected_domain':'none','selected_pivot':'none','next_ticket':'RE-433','next_topic':'ghidra-second-window-rank-29-narrow-export','metadata_work_readiness':'ready','code_change_readiness':'blocked','stop_condition':'rank 29 selected; raw-symbolic artifacts remain excluded'}
def write(b,repo):
 repo=Path(repo);out=[]
 for n in ('candidates','summary','handoff'):
  p=repo/f'docs/reverse/generated/re432-ghidra-second-window-next-candidate-selection-{n}.csv';p.parent.mkdir(parents=True,exist_ok=True)
  with p.open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=b.keys(),lineterminator='\n');w.writeheader();w.writerow(b)
  out.append(p)
 for rel,text in {'docs/reverse/functions/re432-ghidra-second-window-next-candidate-selection.md':'# RE-432 rank-29 selection\n\nCandidate handle retained; unsafe symbolic artifacts excluded.\n','docs/stories/RE-432-ghidra-second-window-next-candidate-selection.md':'# RE-432 rank-29 selection\n\n## Progress tracker\n\n- [x] RE-431 handoff validated.\n- [x] Rank 29 selected.\n- [x] Unsafe symbolic artifacts excluded.\n- [x] RE-433 selected.\n'}.items():
  p=repo/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8');out.append(p)
 return out
