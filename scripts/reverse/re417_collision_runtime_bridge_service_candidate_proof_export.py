import csv
from pathlib import Path
from scripts.reverse import re309_ghidra_unmapped_bridge_candidates as re309

def build(repo):
 repo=Path(repo); h=list(csv.DictReader((repo/'docs/reverse/generated/re416-collision-runtime-bridge-service-readiness-gate-handoff.csv').open()))[0]
 if h['selected_candidate_id']!='9d570ef9a5a7' or h['next_ticket']!='RE-417': raise ValueError('handoff drift')
 old=re309.TOP_LIMIT
 try:
  re309.TOP_LIMIT=50; rows,_=re309.build_bridge_candidates(repo)
 finally: re309.TOP_LIMIT=old
 c=next(x for x in rows if x.candidate_id==h['selected_candidate_id'])
 return {'story_id':'RE-417','topic':'collision-runtime-bridge-service-candidate-proof-export','upstream_handoff':'RE-416','selected_candidate_id':c.candidate_id,'source_symbol_context_count':str(c.source_context_count),'source_file_count':str(c.source_file_count),'mapped_caller_count':str(c.mapped_caller_count),'mapped_callee_count':str(c.mapped_callee_count),'candidate_level_proof_count':'0','repository_symbol_direct_proof_count':'0','ready_to_reopen_domain_count':'0','source_patch_authorized_count':'0','selected_domain':'none','selected_pivot':'none','next_ticket':'RE-418','next_topic':'collision-runtime-bridge-service-candidate-callsite-map','metadata_work_readiness':'ready','code_change_readiness':'blocked','stop_condition':'safe source-symbolic context is prioritization only, not candidate proof'}
def write(b,repo):
 repo=Path(repo);o=[]
 old=re309.TOP_LIMIT
 try:
  re309.TOP_LIMIT=50; rows,_=re309.build_bridge_candidates(repo)
 finally: re309.TOP_LIMIT=old
 contexts=next(x for x in rows if x.candidate_id==b['selected_candidate_id']).safe_source_context.split(';')
 paths={'contexts':repo/'docs/reverse/generated/re417-collision-runtime-bridge-service-candidate-proof-contexts.csv','summary':repo/'docs/reverse/generated/re417-collision-runtime-bridge-service-candidate-proof-summary.csv','handoff':repo/'docs/reverse/generated/re417-collision-runtime-bridge-service-candidate-proof-handoff.csv'}
 with paths['contexts'].open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=['candidate_id','source_symbol'],lineterminator='\n');w.writeheader();w.writerows({'candidate_id':b['selected_candidate_id'],'source_symbol':x} for x in contexts)
 for n in ('summary','handoff'):
  with paths[n].open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=b.keys(),lineterminator='\n');w.writeheader();w.writerow(b)
 o.extend(paths.values())
 for rel,text in [('docs/reverse/functions/re417-collision-runtime-bridge-service-candidate-proof-export.md','# RE-417 collision/runtime bridge proof export\n\nOnly safe source-symbolic context is emitted; no candidate-level proof was found.\n'),('docs/stories/RE-417-collision-runtime-bridge-service-candidate-proof-export.md','# RE-417 collision/runtime bridge proof export\n\n## Progress tracker\n\n- [x] RE-416 handoff validated.\n- [x] Context reconstructed from the safe Ghidra bridge export.\n- [x] Candidate proof remains blocked.\n- [x] RE-418 selected.\n')]:
  p=repo/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text);o.append(p)
 return o
