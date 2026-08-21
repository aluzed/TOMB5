import csv
from pathlib import Path
def build(repo):
 r=list(csv.DictReader((Path(repo)/'docs/reverse/generated/re417-collision-runtime-bridge-service-candidate-proof-handoff.csv').open()))[0]
 if r['selected_candidate_id']!='9d570ef9a5a7' or r['next_ticket']!='RE-418':raise ValueError('handoff drift')
 return {'story_id':'RE-418','topic':'collision-runtime-bridge-service-candidate-callsite-map','upstream_handoff':'RE-417','selected_candidate_id':'9d570ef9a5a7','source_context_function_count':r['source_symbol_context_count'],'source_backed_callsite_count':'0','candidate_level_proof_count':'0','ready_to_reopen_domain_count':'0','source_patch_authorized_count':'0','selected_domain':'none','selected_pivot':'none','next_ticket':'RE-419','next_topic':'collision-runtime-bridge-service-callsite-readiness-gate','metadata_work_readiness':'ready','code_change_readiness':'blocked','stop_condition':'no safe source-backed candidate callsite is available in this metadata-only pass'}
def write(b,repo):
 repo=Path(repo);o=[]
 contexts=list(csv.DictReader((repo/'docs/reverse/generated/re417-collision-runtime-bridge-service-candidate-proof-contexts.csv').open()))
 p=repo/'docs/reverse/generated/re418-collision-runtime-bridge-service-candidate-callsite-map-contexts.csv'
 with p.open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=['candidate_id','source_symbol'],lineterminator='\n');w.writeheader();w.writerows(contexts)
 o.append(p)
 for n in ['callsites','summary','handoff']:
  p=repo/f'docs/reverse/generated/re418-collision-runtime-bridge-service-candidate-callsite-map-{n}.csv'
  with p.open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=b.keys(),lineterminator='\n');w.writeheader();w.writerow(b)
  o.append(p)
 for rel,text in [('docs/reverse/functions/re418-collision-runtime-bridge-service-candidate-callsite-map.md','# RE-418 collision/runtime bridge callsite map\n\nSafe context is retained; no candidate-level callsite is claimed.\n'),('docs/stories/RE-418-collision-runtime-bridge-service-candidate-callsite-map.md','# RE-418 collision/runtime bridge callsite map\n\n## Progress tracker\n\n- [x] RE-417 handoff validated.\n- [x] Safe contexts retained.\n- [x] No candidate-level callsites claimed.\n- [x] RE-419 selected.\n')]:
  p=repo/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text);o.append(p)
 return o
