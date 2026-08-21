from __future__ import annotations
import csv
from dataclasses import dataclass,asdict,fields
from pathlib import Path
BASE='docs/reverse/generated/re398-combat-camera-service-callsite-readiness-gate'
@dataclass(frozen=True)
class Gate: rank:int;gate_class:str;source_backed_callsite_count:int;candidate_level_proof_count:int;gate_decision:str;ready_to_reopen_domain:str;source_patch_authorized:str;next_ticket:str;next_topic:str
@dataclass(frozen=True)
class Summary: story_id:str;topic:str;upstream_handoff:str;selected_candidate_id:str;source_context_function_count:int;source_backed_callsite_count:int;implemented_context_function_count:int;stub_context_function_count:int;candidate_level_proof_count:int;ready_to_reopen_domain_count:int;source_patch_authorized_count:int;selected_domain:str;selected_pivot:str;next_ticket:str;next_topic:str;metadata_work_readiness:str;code_change_readiness:str;stop_condition:str
@dataclass(frozen=True)
class Bundle: gate_rows:list[Gate];summary:Summary
def build_combat_camera_service_callsite_readiness_gate(repo:Path)->Bundle:
 r=list(csv.DictReader((Path(repo)/'docs/reverse/generated/re397-combat-camera-service-candidate-callsite-map-handoff.csv').open()))[0]
 if r['story_id']!='RE-397' or r['next_ticket']!='RE-398' or r['candidate_level_proof_count']!='0':raise ValueError('handoff drift')
 s=Summary('RE-398','combat-camera-service-callsite-readiness-gate','RE-397',r['selected_candidate_id'],int(r['source_context_function_count']),int(r['source_backed_callsite_count']),int(r['implemented_context_function_count']),int(r['stub_context_function_count']),0,0,0,'none','none','TBD','combat-camera-service-candidate-queue-exhausted','ready','blocked','combat/camera queue exhausted without candidate-level proof')
 return Bundle([Gate(1,'candidate-level-proof-missing',s.source_backed_callsite_count,0,'close-exhausted-subcluster','no','no','TBD','combat-camera-service-candidate-queue-exhausted')],s)
def write_all_artifacts(b,repo):
 repo=Path(repo);o={'gate_csv':repo/(BASE+'-gate.csv'),'summary_csv':repo/(BASE+'-summary.csv'),'handoff_csv':repo/(BASE+'-handoff.csv'),'md':repo/'docs/reverse/functions/re398-combat-camera-service-callsite-readiness-gate.md','story':repo/'docs/stories/RE-398-combat-camera-service-callsite-readiness-gate.md'}
 for key,rows,t in [('gate_csv',b.gate_rows,Gate),('summary_csv',[b.summary],Summary),('handoff_csv',[b.summary],Summary)]:
  p=o[key];p.parent.mkdir(parents=True,exist_ok=True)
  with p.open('w',newline='',encoding='utf-8') as h:w=csv.DictWriter(h,fieldnames=[x.name for x in fields(t)],lineterminator='\n');w.writeheader();[w.writerow(asdict(x)) for x in rows]
 o['md'].parent.mkdir(parents=True,exist_ok=True);o['md'].write_text('# RE-398 combat camera callsite readiness gate\n\nCallsite volume is not candidate-level proof; code readiness remains blocked.\n')
 o['story'].parent.mkdir(parents=True,exist_ok=True);o['story'].write_text('# RE-398 combat camera callsite readiness gate\n\n## Progress tracker\n\n- [x] RE-397 handoff validated.\n- [x] Candidate-level proof denied.\n- [x] Queue closed fail-closed.\n')
 return o
