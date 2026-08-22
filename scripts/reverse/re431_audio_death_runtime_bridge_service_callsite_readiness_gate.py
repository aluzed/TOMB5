import csv
from pathlib import Path
def build(repo):
 repo=Path(repo);h=next(csv.DictReader((repo/'docs/reverse/generated/re430-audio-death-runtime-bridge-service-candidate-callsite-map-handoff.csv').open(encoding='utf-8')))
 if h['next_ticket']!='RE-431' or h['selected_candidate_id']!='61b63f61c1fd':raise ValueError('handoff drift')
 if any(h[x]!='0' for x in ('source_backed_callsite_count','candidate_level_proof_count','ready_to_reopen_domain_count','source_patch_authorized_count')) or h['code_change_readiness']!='blocked':raise ValueError('safety drift')
 return {'story_id':'RE-431','topic':'audio-death-runtime-bridge-service-callsite-readiness-gate','upstream_handoff':'RE-430','selected_candidate_id':h['selected_candidate_id'],'source_backed_callsite_count':'0','candidate_level_proof_count':'0','ready_to_reopen_domain_count':'0','source_patch_authorized_count':'0','selected_domain':'none','selected_pivot':'none','next_ticket':'RE-432','next_topic':'ghidra-second-window-next-candidate-selection','metadata_work_readiness':'ready','code_change_readiness':'blocked','stop_condition':'audio/death candidate has no safe source-backed callsites'}
def write(b,repo):
 repo=Path(repo);out=[]
 for n in ('gate','summary','handoff'):
  p=repo/f'docs/reverse/generated/re431-audio-death-runtime-bridge-service-callsite-readiness-gate-{n}.csv';p.parent.mkdir(parents=True,exist_ok=True)
  with p.open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=b.keys(),lineterminator='\n');w.writeheader();w.writerow(b)
  out.append(p)
 for rel,text in {'docs/reverse/functions/re431-audio-death-runtime-bridge-service-callsite-readiness-gate.md':'# RE-431 audio/death callsite readiness gate\n\nNo safe candidate callsites; source changes blocked.\n','docs/stories/RE-431-audio-death-runtime-bridge-service-callsite-readiness-gate.md':'# RE-431 audio/death callsite readiness gate\n\n## Progress tracker\n\n- [x] RE-430 handoff validated.\n- [x] Source changes blocked.\n- [x] RE-432 selected.\n'}.items():
  p=repo/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8');out.append(p)
 return out
