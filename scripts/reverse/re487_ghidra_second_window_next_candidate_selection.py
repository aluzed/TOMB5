"""Fail-closed metadata-only selection for RE-487."""
import csv
from pathlib import Path
from scripts.reverse import re309_ghidra_unmapped_bridge_candidates as candidates
FORBIDDEN_OUTPUT_FRAGMENTS=('0x','fun_','sub_','word_le_hex','payload_offset','opcode','machine word','raw dump','raw evidence','call_address','branch target','call target','ghidra_entry','ghidra_name','source_line_text','code.wad','gamewad.obj','secret','private key','credential','asset','raw binary','source patch','address','symbol evidence','copyright')
FIELDS=('story_id','topic','upstream_handoff','closed_candidate_id','selected_rank','selected_candidate_id','selected_bridge_class','source_symbol_context_count','safe_context_status','ready_to_reopen_domain_count','source_patch_authorized_count','selected_domain','selected_pivot','next_ticket','next_topic','metadata_work_readiness','code_change_readiness','stop_condition')
UPSTREAM_FIELDS=('story_id','topic','upstream_handoff','selected_candidate_id','selected_rank','selected_subcluster','source_symbol_context_count','bridge_class','safe_context_status','source_backed_callsite_count','candidate_level_proof_count','repository_symbol_direct_proof_count','ready_to_reopen_domain_count','source_patch_authorized_count','selected_domain','selected_pivot','next_ticket','next_topic','metadata_work_readiness','code_change_readiness','stop_condition')
TICKET='RE-487'; TOPIC='ghidra-second-window-next-candidate-selection'; UPSTREAM='RE-486'; CLOSED='bc923a17e1b0'; RANK='44'; CANDIDATE='967dd5c009c5'; BRIDGE='mapped-caller-callee-bridge'; CONTEXTS='8'; NEXT='RE-488'; NEXT_TOPIC='ghidra-second-window-rank-44-narrow-export'
def ranked_candidate(repo,rank):
 old=candidates.TOP_LIMIT
 try:
  candidates.TOP_LIMIT=50; rows,_=candidates.build_bridge_candidates(Path(repo))
 finally: candidates.TOP_LIMIT=old
 return next((r for r in rows if r.rank==int(rank)),None)
def read_upstream(repo):
 p=Path(repo)/'docs/reverse/generated/re486-mapped-callee-bridge-readiness-gate-handoff.csv'
 with p.open(encoding='utf-8',newline='') as f:
  r=csv.DictReader(f)
  if tuple(r.fieldnames or ())!=UPSTREAM_FIELDS: raise ValueError('handoff schema drift')
  rows=list(r)
 if len(rows)!=1: raise ValueError('handoff row-count drift')
 row=rows[0]
 expected={'story_id':UPSTREAM,'topic':'mapped-callee-bridge-readiness-gate','upstream_handoff':'RE-485','selected_candidate_id':CLOSED,'selected_rank':'43','selected_subcluster':'mapped-callee-bridge-readiness-gate','source_symbol_context_count':'8','bridge_class':'mapped-callee-bridge','safe_context_status':'filtered-metadata-only','source_backed_callsite_count':'0','candidate_level_proof_count':'0','repository_symbol_direct_proof_count':'0','ready_to_reopen_domain_count':'0','source_patch_authorized_count':'0','selected_domain':'none','selected_pivot':'none','next_ticket':TICKET,'next_topic':TOPIC,'metadata_work_readiness':'ready','code_change_readiness':'blocked','stop_condition':'metadata-only safety gate denies proof-domain selection and source changes'}
 for k,v in expected.items():
  if row.get(k)!=v: raise ValueError(f'handoff drift: {k}')
 return row
def build(repo):
 row=read_upstream(repo); c=ranked_candidate(repo,RANK)
 if c is None or (c.candidate_id,c.bridge_class,c.source_context_count)!=(CANDIDATE,BRIDGE,int(CONTEXTS)): raise ValueError('ranked candidate drift')
 if c.ready_to_reopen_domain!='no' or c.source_patch_authorized!='no': raise ValueError('candidate readiness drift')
 result=dict(story_id=TICKET,topic=TOPIC,upstream_handoff=UPSTREAM,closed_candidate_id=row['selected_candidate_id'],selected_rank=RANK,selected_candidate_id=CANDIDATE,selected_bridge_class=BRIDGE,source_symbol_context_count=CONTEXTS,safe_context_status='filtered-metadata-only',ready_to_reopen_domain_count='0',source_patch_authorized_count='0',selected_domain='none',selected_pivot='none',next_ticket=NEXT,next_topic=NEXT_TOPIC,metadata_work_readiness='ready',code_change_readiness='blocked',stop_condition='next ranked metadata candidate selected; source changes remain blocked')
 validate_output(result); return result
def validate_output(r):
 if tuple(r)!=FIELDS: raise ValueError('output schema drift')
 expected={'story_id':TICKET,'topic':TOPIC,'upstream_handoff':UPSTREAM,'closed_candidate_id':CLOSED,'selected_rank':RANK,'selected_candidate_id':CANDIDATE,'selected_bridge_class':BRIDGE,'source_symbol_context_count':CONTEXTS,'safe_context_status':'filtered-metadata-only','ready_to_reopen_domain_count':'0','source_patch_authorized_count':'0','selected_domain':'none','selected_pivot':'none','next_ticket':NEXT,'next_topic':NEXT_TOPIC,'metadata_work_readiness':'ready','code_change_readiness':'blocked','stop_condition':'next ranked metadata candidate selected; source changes remain blocked'}
 for k,v in expected.items():
  if r.get(k)!=v: raise ValueError(f'output safety drift: {k}')
 if any(x in '\n'.join(map(str,r.values())).lower() for x in FORBIDDEN_OUTPUT_FRAGMENTS): raise ValueError('forbidden output fragment')
def write(r,repo):
 validate_output(r); repo=Path(repo); paths=[]; prefix='re487-ghidra-second-window-next-candidate-selection'
 for suffix in ('candidates','summary','handoff'):
  p=repo/'docs/reverse/generated'/f'{prefix}-{suffix}.csv';p.parent.mkdir(parents=True,exist_ok=True)
  with p.open('w',encoding='utf-8',newline='') as f: w=csv.DictWriter(f,fieldnames=FIELDS,lineterminator='\n');w.writeheader();w.writerow(r)
  paths.append(p)
 docs={repo/'docs/reverse/functions/re487-ghidra-second-window-next-candidate-selection.md':'# RE-487 ghidra-second-window-next-candidate-selection\n\nFiltered metadata-only decision; source and code work remain blocked.\n',repo/'docs/stories/RE-487-ghidra-second-window-next-candidate-selection.md':'# RE-487 ghidra-second-window-next-candidate-selection\n\n## Progress tracker\n\n- [x] RE-486 handoff validated.\n- [x] Filtered metadata decision recorded.\n- [x] Safety guard retained.\n- [x] Source and code work remain blocked.\n- [x] RE-488 selected; not executed.\n'}
 for p,t in docs.items():p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t,encoding='utf-8');paths.append(p)
 for p in paths:
  if any(x in p.read_text(encoding='utf-8').lower() for x in FORBIDDEN_OUTPUT_FRAGMENTS):raise ValueError('forbidden written fragment')
 return paths
if __name__=='__main__':
 root=Path(__file__).resolve().parents[2];write(build(root),root)
