from __future__ import annotations
import csv,re
from dataclasses import dataclass,asdict,fields
from pathlib import Path
ID='0aaa76206517'; BASE='docs/reverse/generated/re397-combat-camera-service-candidate-callsite-map'
@dataclass(frozen=True)
class F: rank:int;candidate_id:str;caller_symbol:str;source_file:str;function_status:str;source_backed_callsite_count:int
@dataclass(frozen=True)
class C: rank:int;candidate_id:str;caller_symbol:str;source_file:str;source_line_number:int;callee_symbol:str;callsite_family:str;candidate_level_proof:str;ready_to_reopen_domain:str;source_patch_authorized:str
@dataclass(frozen=True)
class S: story_id:str;topic:str;upstream_handoff:str;selected_candidate_id:str;source_context_function_count:int;source_backed_callsite_count:int;implemented_context_function_count:int;stub_context_function_count:int;candidate_level_proof_count:int;ready_to_reopen_domain_count:int;source_patch_authorized_count:int;selected_domain:str;selected_pivot:str;next_ticket:str;next_topic:str;metadata_work_readiness:str;code_change_readiness:str;stop_condition:str
@dataclass(frozen=True)
class B: function_rows:list[F];callsite_rows:list[C];summary:S
def build_combat_camera_service_candidate_callsite_map(repo:Path)->B:
 repo=Path(repo); rows=list(csv.DictReader((repo/'docs/reverse/generated/re396-combat-camera-service-candidate-proof-contexts.csv').open()))
 if len(rows)!=17 or {r['candidate_id'] for r in rows}!={ID}:raise ValueError('RE-396 context drift')
 fs=[];cs=[]
 for r in rows:
  p=repo/r['source_file']; text=p.read_text(encoding='utf-8',errors='ignore') if p.exists() else ''
  matches=list(re.finditer(r'\b([A-Za-z_][A-Za-z0-9_]*)\s*\(',text))
  calls=[m for m in matches if m.group(1) not in {'if','for','while','switch','return','sizeof'} and not m.group(1).lower().startswith(('sub_','fun_'))]
  fs.append(F(len(fs)+1,ID,r['source_symbol'],r['source_file'],'source-with-calls' if calls else 'source-no-callsite',len(calls)))
  for m in calls:cs.append(C(len(cs)+1,ID,r['source_symbol'],r['source_file'],text.count('\n',0,m.start())+1,m.group(1),'combat-camera-context','no','no','no'))
 s=S('RE-397','combat-camera-service-candidate-callsite-map','RE-396',ID,len(fs),len(cs),sum(x.function_status=='source-with-calls' for x in fs),0,0,0,0,'none','none','RE-398','combat-camera-service-callsite-readiness-gate','ready','blocked','source-backed callsites require a readiness gate before domain selection')
 return B(fs,cs,s)
def wc(p,rows,t):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('w',newline='',encoding='utf-8') as h:
  w=csv.DictWriter(h,fieldnames=[x.name for x in fields(t)],lineterminator='\n');w.writeheader();[w.writerow(asdict(x)) for x in rows]
def write_all_artifacts(b:B,repo:Path):
 repo=Path(repo);o={'functions_csv':repo/(BASE+'-functions.csv'),'callsites_csv':repo/(BASE+'-callsites.csv'),'gate_csv':repo/(BASE+'-gate.csv'),'summary_csv':repo/(BASE+'-summary.csv'),'handoff_csv':repo/(BASE+'-handoff.csv'),'md':repo/'docs/reverse/functions/re397-combat-camera-service-candidate-callsite-map.md','story':repo/'docs/stories/RE-397-combat-camera-service-candidate-callsite-map.md'};wc(o['functions_csv'],b.function_rows,F);wc(o['callsites_csv'],b.callsite_rows,C);wc(o['gate_csv'],[b.summary],S);wc(o['summary_csv'],[b.summary],S);wc(o['handoff_csv'],[b.summary],S);o['md'].parent.mkdir(parents=True,exist_ok=True);o['md'].write_text('# RE-397 combat camera callsite map\n\nSource-backed callsite rows are not source-patch authorization.\n',encoding='utf-8');o['story'].parent.mkdir(parents=True,exist_ok=True);o['story'].write_text('# RE-397 combat camera callsite map\n\n## Progress tracker\n\n- [x] RE-396 handoff validated.\n- [x] Source-backed callsite metadata emitted.\n- [x] Readiness remains blocked.\n- [x] RE-398 selected.\n',encoding='utf-8');return o
