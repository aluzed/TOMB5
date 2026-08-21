#!/usr/bin/env python3
"""Export metadata-only candidate context for RE-395 combat/camera candidate."""
from __future__ import annotations
import argparse,csv,hashlib
from collections import defaultdict
from dataclasses import asdict,dataclass,fields
from pathlib import Path
RE395_HANDOFF='docs/reverse/generated/re395-combat-camera-service-readiness-gate-handoff.csv'; RE395_CANDIDATES='docs/reverse/generated/re395-combat-camera-service-readiness-gate-candidates.csv'; GHIDRA='docs/reverse/generated/ghidra-functions.csv'; MAP='docs/reverse/generated/repo-function-map.csv'
CONTEXTS='docs/reverse/generated/re396-combat-camera-service-candidate-proof-contexts.csv'; PROOF='docs/reverse/generated/re396-combat-camera-service-candidate-proof-gate.csv'; SUMMARY='docs/reverse/generated/re396-combat-camera-service-candidate-proof-summary.csv'; HANDOFF='docs/reverse/generated/re396-combat-camera-service-candidate-proof-handoff.csv'; MD='docs/reverse/functions/re396-combat-camera-service-candidate-proof-export.md'; STORY='docs/stories/RE-396-combat-camera-service-candidate-proof-export.md'
ID='0aaa76206517'; NEXT='RE-397'; TOPIC='combat-camera-service-candidate-callsite-map'; FORBIDDEN_OUTPUT_FRAGMENTS=('0x','fun_','sub_','word_le_hex','payload_offset','dump row','opcode','machine word','call_address','branch target','call target','hex-address-fragment','raw_evidence','ghidra_entry','ghidra_name','source_line_text','unimplemented();')
@dataclass(frozen=True)
class Context: rank:int; candidate_id:str; context_kind:str; source_symbol:str; source_module:str; source_file:str; combat_camera_role:str; context_family:str; candidate_level_proof:str; ready_to_reopen_domain:str; source_patch_authorized:str; blocker_class:str
@dataclass(frozen=True)
class Proof: rank:int; candidate_id:str; source_symbol_context_count:int; caller_context_count:int; callee_context_count:int; direct_repo_symbol_count:int; candidate_level_proof_count:int; proof_gate:str; candidate_level_proof:str; ready_to_reopen_domain:str; source_patch_authorized:str; next_ticket:str; next_topic:str; stop_condition:str
@dataclass(frozen=True)
class SummaryRow: story_id:str; topic:str; upstream_handoff:str; selected_candidate_id:str; source_symbol_context_count:int; caller_context_count:int; callee_context_count:int; direct_repo_symbol_count:int; candidate_level_proof_count:int; ready_to_reopen_domain_count:int; source_patch_authorized_count:int; selected_domain:str; selected_pivot:str; next_ticket:str; next_topic:str; metadata_work_readiness:str; code_change_readiness:str; stop_condition:str
@dataclass(frozen=True)
class Bundle: context_rows:list[Context]; proof_rows:list[Proof]; summary:SummaryRow
def read(p:Path):
 with p.open(newline='',encoding='utf-8') as f:return list(csv.DictReader(f))
def hashid(row):return hashlib.sha1(f"{row['entry']}|{row['name']}".encode()).hexdigest()[:12]
def family(symbol):
 s=symbol.lower()
 if 'camera' in s:return 'camera-service'
 if 'missile' in s:return 'missile-service'
 if 'bodypart' in s:return 'bodypart-service'
 if 'detect' in s:return 'detection-service'
 if 'control' in s:return 'entity-control-context'
 return 'other'
def require(text):
 for x in FORBIDDEN_OUTPUT_FRAGMENTS:
  if x in text.lower():raise ValueError(f'forbidden output {x}')
def build_combat_camera_service_candidate_proof_export(repo:Path)->Bundle:
 repo=Path(repo); hand=read(repo/RE395_HANDOFF)
 if len(hand)!=1 or hand[0].get('selected_followup_candidate_id')!=ID or hand[0].get('next_ticket')!='RE-396' or hand[0].get('code_change_readiness')!='blocked':raise ValueError('RE-395 handoff drift')
 candidates=read(repo/RE395_CANDIDATES)
 if len(candidates)!=1 or candidates[0].get('candidate_id')!=ID or candidates[0].get('next_probe')!='candidate-proof-export':raise ValueError('RE-395 candidate drift')
 gh=[r for r in read(repo/GHIDRA) if hashid(r)==ID]
 if len(gh)!=1:raise ValueError('candidate identity drift')
 maps=read(repo/MAP); by=defaultdict(list)
 for r in maps:
  if r.get('mapping_status')=='mapped' and r.get('ghidra_name') and r.get('repo_function') not in {'','if','for','while','switch'}:by[r['ghidra_name']].append(r)
 direct=sum(1 for r in by.get(gh[0]['name'],[]))
 if direct:raise ValueError('unexpected direct repo proof')
 caller_names=[x for x in gh[0].get('callers','').split(';') if x]; callee_names=[x for x in gh[0].get('called_functions','').split(';') if x]
 def unique(names):
  seen=set(); out=[]
  for n in names:
   for r in by.get(n,[]):
    key=(r.get('file',''),r['repo_function'])
    if key not in seen:seen.add(key);out.append(r)
  return sorted(out,key=lambda r:(r.get('file',''),r['repo_function']))
 callers,callees=unique(caller_names),unique(callee_names)
 rows=[]
 for kind,items in [('caller',callers),('callee',callees)]:
  for r in items:
   sym=r['repo_function']; rows.append(Context(len(rows)+1,ID,kind,sym,r.get('file','').split('/',1)[0],r.get('file',''),f'{family(sym)}-{kind}-context',family(sym),'no','no','no','mapped-context-not-direct-candidate-proof'))
 if not rows:raise ValueError('missing mapped context')
 proof=[Proof(1,ID,len(rows),len(callers),len(callees),0,0,'blocked-unmapped-candidate-identity','no','no','no',NEXT,TOPIC,'candidate hash lacks direct repo proof; build source-backed callsite map next')]
 s=SummaryRow('RE-396','combat-camera-service-candidate-proof-export','RE-395',ID,len(rows),len(callers),len(callees),0,0,0,0,'none','none',NEXT,TOPIC,'ready','blocked','candidate-scoped context lacks direct source-backed proof; build a callsite map next')
 return Bundle(rows,proof,s)
def writecsv(p,rows,t):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=[x.name for x in fields(t)],lineterminator='\n');w.writeheader();[w.writerow(asdict(x)) for x in rows]
def write_all_artifacts(bundle,repo):
 repo=Path(repo); out={'contexts_csv':repo/CONTEXTS,'proof_csv':repo/PROOF,'summary_csv':repo/SUMMARY,'handoff_csv':repo/HANDOFF,'md':repo/MD,'story':repo/STORY};writecsv(out['contexts_csv'],bundle.context_rows,Context);writecsv(out['proof_csv'],bundle.proof_rows,Proof);writecsv(out['summary_csv'],[bundle.summary],SummaryRow);writecsv(out['handoff_csv'],[bundle.summary],SummaryRow)
 md=f'''# RE-396 combat camera service candidate proof export\n\nExported `{bundle.summary.source_symbol_context_count}` metadata-only source-symbolic context rows for candidate `{ID}`. No proof domain is reopened; direct repository proof remains absent.\n\n## Handoff\n\n- Next ticket: `{NEXT}`\n- Next topic: `{TOPIC}`\n- Code readiness: `blocked`\n'''
 story=f'''# RE-396 combat camera service candidate proof export\n\n## Progress tracker\n\n- [x] RE-395 candidate proof-export handoff validated.\n- [x] Candidate context reconstructed inside the generator only.\n- [x] Metadata-only context rows emitted.\n- [x] Domain/pivot/source-patch readiness kept blocked.\n- [x] Source-backed callsite-map follow-up selected.\n\n## Generated artifacts\n\n- `{CONTEXTS}`\n- `{PROOF}`\n- `{SUMMARY}`\n- `{HANDOFF}`\n- `{MD}`\n\n## Follow-up\n\n- `{NEXT}` / `{TOPIC}` for candidate `{ID}`.\n'''
 out['md'].parent.mkdir(parents=True,exist_ok=True);out['md'].write_text(md,encoding='utf-8');out['story'].parent.mkdir(parents=True,exist_ok=True);out['story'].write_text(story,encoding='utf-8')
 for p in out.values():require(p.read_text(encoding='utf-8'))
 return out
def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=Path.cwd());a=p.parse_args();repo=a.repo.resolve()
 for k,v in write_all_artifacts(build_combat_camera_service_candidate_proof_export(repo),repo).items():print(f'{k}: {v.relative_to(repo)}')
if __name__=='__main__':main()
