import csv
from pathlib import Path
def build(repo):
 repo=Path(repo);h=next(csv.DictReader((repo/'docs/reverse/generated/re429-audio-death-runtime-bridge-service-candidate-proof-handoff.csv').open(encoding='utf-8')))
 if h['next_ticket']!='RE-430' or h['selected_candidate_id']!='61b63f61c1fd':raise ValueError('handoff drift')
 if any(h[x]!='0' for x in ('candidate_level_proof_count','repository_symbol_direct_proof_count','ready_to_reopen_domain_count','source_patch_authorized_count')) or h['code_change_readiness']!='blocked' or h['source_symbol_context_count']!='10':raise ValueError('safety drift')
 return {'story_id':'RE-430','topic':'audio-death-runtime-bridge-service-candidate-callsite-map','upstream_handoff':'RE-429','selected_candidate_id':h['selected_candidate_id'],'source_context_function_count':'10','source_backed_callsite_count':'0','candidate_level_proof_count':'0','ready_to_reopen_domain_count':'0','source_patch_authorized_count':'0','selected_domain':'none','selected_pivot':'none','next_ticket':'RE-431','next_topic':'audio-death-runtime-bridge-service-callsite-readiness-gate','metadata_work_readiness':'ready','code_change_readiness':'blocked','stop_condition':'no safe source-backed candidate callsite in metadata-only map'}
def write(b,repo):
 repo=Path(repo);out=[]
 for n in ('callsites','summary','handoff'):
  p=repo/f'docs/reverse/generated/re430-audio-death-runtime-bridge-service-candidate-callsite-map-{n}.csv';p.parent.mkdir(parents=True,exist_ok=True)
  with p.open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=b.keys(),lineterminator='\n');w.writeheader();w.writerow(b)
  out.append(p)
 for rel,text in {'docs/reverse/functions/re430-audio-death-runtime-bridge-service-candidate-callsite-map.md':'# RE-430 audio/death bridge callsite map\n\nNo candidate-level callsites are claimed.\n','docs/stories/RE-430-audio-death-runtime-bridge-service-candidate-callsite-map.md':'# RE-430 audio/death bridge callsite map\n\n## Progress tracker\n\n- [x] RE-429 handoff validated.\n- [x] Metadata-only map emitted.\n- [x] RE-431 selected.\n'}.items():
  p=repo/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8');out.append(p)
 return out
