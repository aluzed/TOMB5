import csv
from pathlib import Path

def build(repo):
 repo=Path(repo)
 h=next(csv.DictReader((repo/'docs/reverse/generated/re428-audio-death-runtime-bridge-service-readiness-gate-handoff.csv').open(encoding='utf-8')))
 if h['next_ticket']!='RE-429' or h['selected_candidate_id']!='61b63f61c1fd': raise ValueError('handoff drift')
 if any((h['candidate_level_proof_count']!='0',h['ready_to_reopen_domain_count']!='0',h['source_patch_authorized_count']!='0',h['code_change_readiness']!='blocked')): raise ValueError('safety-gate drift')
 if h['source_symbol_context_count'] != '10': raise ValueError('context-count drift')
 return {'story_id':'RE-429','topic':'audio-death-runtime-bridge-service-candidate-proof-export','upstream_handoff':'RE-428','selected_candidate_id':h['selected_candidate_id'],'source_symbol_context_count':h['source_symbol_context_count'],'candidate_level_proof_count':'0','repository_symbol_direct_proof_count':'0','ready_to_reopen_domain_count':'0','source_patch_authorized_count':'0','selected_domain':'none','selected_pivot':'none','next_ticket':'RE-430','next_topic':'audio-death-runtime-bridge-service-candidate-callsite-map','metadata_work_readiness':'ready','code_change_readiness':'blocked','stop_condition':'audio/death symbolic context has no direct candidate proof'}
def write(b,repo):
 repo=Path(repo); out=[]
 for n in ('contexts','summary','handoff'):
  p=repo/f'docs/reverse/generated/re429-audio-death-runtime-bridge-service-candidate-proof-{n}.csv';p.parent.mkdir(parents=True,exist_ok=True)
  with p.open('w',newline='',encoding='utf-8') as f:
   w=csv.DictWriter(f,fieldnames=b.keys(),lineterminator='\n');w.writeheader();w.writerow(b)
  out.append(p)
 for rel,text in {'docs/reverse/functions/re429-audio-death-runtime-bridge-service-candidate-proof-export.md':'# RE-429 audio/death bridge proof export\n\nNo direct candidate proof is available.\n','docs/stories/RE-429-audio-death-runtime-bridge-service-candidate-proof-export.md':'# RE-429 audio/death bridge proof export\n\n## Progress tracker\n\n- [x] RE-428 handoff validated.\n- [x] Context export completed.\n- [x] RE-430 selected.\n'}.items():
  p=repo/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8');out.append(p)
 return out
