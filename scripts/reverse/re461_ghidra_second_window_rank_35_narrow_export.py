#!/usr/bin/env python3
"""Produce the safe, metadata-only RE-461 rank-35 narrow export."""
import csv
from pathlib import Path
UPSTREAM='docs/reverse/generated/re460-ghidra-second-window-next-candidate-selection-handoff.csv'
PREFIX='re461-ghidra-second-window-rank-35-narrow-export'
FORBIDDEN_OUTPUT_FRAGMENTS=('0x','fun_','sub_','word_le_hex','payload_offset','opcode','machine word','raw dump','raw_evidence','call_address','branch target','call target','ghidra_entry','ghidra_name','source_line_text','code.wad','gamewad.obj','secret','asset','raw binary','address','symbol evidence','copyright')
UPSTREAM_FIELDS=('story_id','topic','upstream_handoff','closed_candidate_id','selected_rank','selected_candidate_id','selected_bridge_class','source_symbol_context_count','safe_context_status','ready_to_reopen_domain_count','source_patch_authorized_count','selected_domain','selected_pivot','next_ticket','next_topic','metadata_work_readiness','code_change_readiness','stop_condition')
FIELDS=('story_id','topic','upstream_handoff','selected_candidate_id','selected_rank','selected_subcluster','source_symbol_context_count','bridge_class','safe_context_status','candidate_level_proof_count','ready_to_reopen_domain_count','source_patch_authorized_count','selected_domain','selected_pivot','next_ticket','next_topic','metadata_work_readiness','code_change_readiness','stop_condition')
def one_row(p):
 with p.open(encoding='utf-8',newline='') as f:
  rd=csv.DictReader(f)
  if tuple(rd.fieldnames or ())!=UPSTREAM_FIELDS:raise ValueError('handoff schema drift')
  rows=list(rd)
 if len(rows)!=1:raise ValueError('handoff row-count drift')
 return rows[0]
def build(repo):
 h=one_row(Path(repo)/UPSTREAM)
 expected={'story_id':'RE-460','topic':'ghidra-second-window-next-candidate-selection','upstream_handoff':'RE-459','closed_candidate_id':'aaf42cb3b10b','selected_rank':'35','selected_candidate_id':'ede72eed0265','selected_bridge_class':'mapped-caller-bridge','source_symbol_context_count':'9','safe_context_status':'filtered-metadata-only','ready_to_reopen_domain_count':'0','source_patch_authorized_count':'0','selected_domain':'none','selected_pivot':'none','next_ticket':'RE-461','next_topic':'ghidra-second-window-rank-35-narrow-export','metadata_work_readiness':'ready','code_change_readiness':'blocked'}
 for k,v in expected.items():
  if h.get(k)!=v:raise ValueError(f'handoff drift: {k}')
 return {'story_id':'RE-461','topic':'ghidra-second-window-rank-35-narrow-export','upstream_handoff':'RE-460','selected_candidate_id':h['selected_candidate_id'],'selected_rank':h['selected_rank'],'selected_subcluster':'mapped-caller-bridge-readiness-gate','source_symbol_context_count':h['source_symbol_context_count'],'bridge_class':h['selected_bridge_class'],'safe_context_status':h['safe_context_status'],'candidate_level_proof_count':'0','ready_to_reopen_domain_count':'0','source_patch_authorized_count':'0','selected_domain':'none','selected_pivot':'none','next_ticket':'RE-462','next_topic':'mapped-caller-bridge-readiness-gate','metadata_work_readiness':'ready','code_change_readiness':'blocked','stop_condition':'narrow rank-35 export requires readiness gate before proof-domain selection'}
def validate_output(r):
 if tuple(r)!=FIELDS:raise ValueError('output schema drift')
 if any(x in '\n'.join(str(v).lower() for v in r.values()) for x in FORBIDDEN_OUTPUT_FRAGMENTS):raise ValueError('forbidden output fragment')
 identity={'story_id':'RE-461','topic':'ghidra-second-window-rank-35-narrow-export','upstream_handoff':'RE-460','selected_candidate_id':'ede72eed0265','selected_rank':'35','selected_subcluster':'mapped-caller-bridge-readiness-gate','next_ticket':'RE-462','next_topic':'mapped-caller-bridge-readiness-gate','metadata_work_readiness':'ready'}
 if any(r.get(k)!=v for k,v in identity.items()):raise ValueError('output identity drift')
 safety={'safe_context_status':'filtered-metadata-only','candidate_level_proof_count':'0','ready_to_reopen_domain_count':'0','source_patch_authorized_count':'0','selected_domain':'none','selected_pivot':'none','code_change_readiness':'blocked'}
 if any(r.get(k)!=v for k,v in safety.items()):raise ValueError('output safety drift')
def write(r,repo):
 validate_output(r);repo=Path(repo);out=[]
 for s in ('contexts','summary','handoff'):
  p=repo/f'docs/reverse/generated/{PREFIX}-{s}.csv';p.parent.mkdir(parents=True,exist_ok=True)
  with p.open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=r.keys(),lineterminator='\n');w.writeheader();w.writerow(r)
  out.append(p)
 docs={'docs/reverse/functions/re461-ghidra-second-window-rank-35-narrow-export.md':'# RE-461 rank-35 narrow export\n\nThe selected candidate is filtered metadata only; source and code work remain blocked.\n','docs/stories/RE-461-ghidra-second-window-rank-35-narrow-export.md':'# RE-461 rank-35 narrow export\n\n## Progress tracker\n\n- [x] RE-460 handoff validated.\n- [x] Rank-35 context narrowed.\n- [x] Filtered metadata-only safety retained.\n- [x] Source and code work remain blocked.\n- [x] RE-462 selected; not executed.\n'}
 for rel,text in docs.items():p=repo/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8');out.append(p)
 for p in out:
  if any(x in p.read_text(encoding='utf-8').lower() for x in FORBIDDEN_OUTPUT_FRAGMENTS):raise ValueError('forbidden written fragment')
 return out
if __name__=='__main__':
 root=Path(__file__).resolve().parents[2];write(build(root),root)
