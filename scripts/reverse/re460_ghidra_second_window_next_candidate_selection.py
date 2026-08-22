#!/usr/bin/env python3
"""Select the next safe second-window bridge candidate as metadata only."""
import csv
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from scripts.reverse import re309_ghidra_unmapped_bridge_candidates as r309
UPSTREAM='docs/reverse/generated/re459-mapped-caller-bridge-readiness-gate-handoff.csv'
PREFIX='re460-ghidra-second-window-next-candidate-selection'
FORBIDDEN_OUTPUT_FRAGMENTS=('0x','fun_','sub_','word_le_hex','payload_offset','opcode','machine word','raw dump','raw_evidence','call_address','branch target','call target','ghidra_entry','ghidra_name','source_line_text','code.wad','gamewad.obj','secret','asset','raw binary','address','symbol evidence','copyright')
UPSTREAM_FIELDS=('story_id','topic','upstream_handoff','selected_candidate_id','selected_rank','selected_subcluster','source_symbol_context_count','bridge_class','safe_context_status','source_backed_callsite_count','candidate_level_proof_count','repository_symbol_direct_proof_count','ready_to_reopen_domain_count','source_patch_authorized_count','selected_domain','selected_pivot','next_ticket','next_topic','metadata_work_readiness','code_change_readiness','stop_condition')
FIELDS=('story_id','topic','upstream_handoff','closed_candidate_id','selected_rank','selected_candidate_id','selected_bridge_class','source_symbol_context_count','safe_context_status','ready_to_reopen_domain_count','source_patch_authorized_count','selected_domain','selected_pivot','next_ticket','next_topic','metadata_work_readiness','code_change_readiness','stop_condition')
def one_row(p):
 with p.open(encoding='utf-8',newline='') as f:
  rd=csv.DictReader(f)
  if tuple(rd.fieldnames or ())!=UPSTREAM_FIELDS: raise ValueError('handoff schema drift')
  rows=list(rd)
 if len(rows)!=1: raise ValueError('handoff row-count drift')
 return rows[0]
def rank(repo,n):
 old=r309.TOP_LIMIT
 try:r309.TOP_LIMIT=50;rows,_=r309.build_bridge_candidates(repo)
 finally:r309.TOP_LIMIT=old
 return next((x for x in rows if x.rank==n),None)
def build(repo):
 h=one_row(Path(repo)/UPSTREAM)
 expected={'story_id':'RE-459','topic':'mapped-caller-bridge-readiness-gate','upstream_handoff':'RE-458','selected_candidate_id':'aaf42cb3b10b','selected_rank':'34','selected_subcluster':'mapped-caller-bridge-readiness-gate','source_symbol_context_count':'9','bridge_class':'mapped-caller-bridge','safe_context_status':'filtered-metadata-only','next_ticket':'RE-460','next_topic':'ghidra-second-window-next-candidate-selection','metadata_work_readiness':'ready','code_change_readiness':'blocked'}
 for k,v in expected.items():
  if h.get(k)!=v: raise ValueError(f'handoff drift: {k}')
 if any(h.get(k)!='0' for k in ('source_backed_callsite_count','candidate_level_proof_count','repository_symbol_direct_proof_count','ready_to_reopen_domain_count','source_patch_authorized_count')):raise ValueError('safety-count drift')
 c=rank(Path(repo),35)
 if c is None or (c.candidate_id,c.bridge_class,c.source_context_count)!=('ede72eed0265','mapped-caller-bridge',9):raise ValueError('rank 35 candidate drift')
 if c.ready_to_reopen_domain!='no' or c.source_patch_authorized!='no':raise ValueError('rank 35 readiness drift')
 return {'story_id':'RE-460','topic':'ghidra-second-window-next-candidate-selection','upstream_handoff':'RE-459','closed_candidate_id':h['selected_candidate_id'],'selected_rank':str(c.rank),'selected_candidate_id':c.candidate_id,'selected_bridge_class':c.bridge_class,'source_symbol_context_count':str(c.source_context_count),'safe_context_status':'filtered-metadata-only','ready_to_reopen_domain_count':'0','source_patch_authorized_count':'0','selected_domain':'none','selected_pivot':'none','next_ticket':'RE-461','next_topic':'ghidra-second-window-rank-35-narrow-export','metadata_work_readiness':'ready','code_change_readiness':'blocked','stop_condition':'rank 35 selected; source and code work remain blocked pending a narrow metadata gate'}
def validate_output(r):
 if tuple(r)!=FIELDS:raise ValueError('output schema drift')
 if any(x in '\n'.join(str(v).lower() for v in r.values()) for x in FORBIDDEN_OUTPUT_FRAGMENTS):raise ValueError('forbidden output fragment')
 identity={'story_id':'RE-460','upstream_handoff':'RE-459','closed_candidate_id':'aaf42cb3b10b','selected_rank':'35','selected_candidate_id':'ede72eed0265','next_ticket':'RE-461','next_topic':'ghidra-second-window-rank-35-narrow-export','metadata_work_readiness':'ready'}
 if any(r.get(k)!=v for k,v in identity.items()):raise ValueError('output identity drift')
 safety={'safe_context_status':'filtered-metadata-only','ready_to_reopen_domain_count':'0','source_patch_authorized_count':'0','selected_domain':'none','selected_pivot':'none','code_change_readiness':'blocked'}
 if any(r.get(k)!=v for k,v in safety.items()):raise ValueError('output safety drift')
def write(r,repo):
 validate_output(r);repo=Path(repo);out=[]
 for s in ('candidates','summary','handoff'):
  p=repo/f'docs/reverse/generated/{PREFIX}-{s}.csv';p.parent.mkdir(parents=True,exist_ok=True)
  with p.open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=r.keys(),lineterminator='\n');w.writeheader();w.writerow(r)
  out.append(p)
 docs={'docs/reverse/functions/re460-ghidra-second-window-next-candidate-selection.md':'# RE-460 second-window next candidate selection\n\nRank 35 is retained as a metadata-only candidate; source and code work remain blocked.\n','docs/stories/RE-460-ghidra-second-window-next-candidate-selection.md':'# RE-460 second-window next candidate selection\n\n## Progress tracker\n\n- [x] RE-459 handoff validated.\n- [x] Rank 34 closure retained.\n- [x] Rank 35 metadata candidate selected.\n- [x] Source and code work remain blocked.\n- [x] RE-461 selected; not executed.\n'}
 for rel,text in docs.items():p=repo/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8');out.append(p)
 for p in out:
  if any(x in p.read_text(encoding='utf-8').lower() for x in FORBIDDEN_OUTPUT_FRAGMENTS):raise ValueError('forbidden written fragment')
 return out
if __name__=='__main__':write(build(ROOT),ROOT)
