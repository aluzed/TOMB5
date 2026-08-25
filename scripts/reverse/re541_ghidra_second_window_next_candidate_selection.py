"""Fail-closed metadata-only RE-541 candidate selection."""
import csv
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from scripts.reverse import re309_ghidra_unmapped_bridge_candidates as candidates
BAD=('0x','fun_','sub_','word_le_hex','payload_offset','opcode','machine word','raw dump','raw evidence','raw_evidence','call_address','branch target','call target','ghidra_entry','ghidra_name','source_line_text','code.wad','gamewad.obj','secret','private key','credential','asset','raw binary','source patch','address','symbol evidence','copyright')
UPSTREAM='docs/reverse/generated/re540-mapped-callee-bridge-readiness-gate-handoff.csv';PREFIX='re541-ghidra-second-window-next-candidate-selection'
UPFIELDS=('story_id','topic','upstream_handoff','selected_candidate_id','selected_rank','selected_subcluster','source_symbol_context_count','bridge_class','safe_context_status','source_backed_callsite_count','candidate_level_proof_count','repository_symbol_direct_proof_count','ready_to_reopen_domain_count','source_patch_authorized_count','selected_domain','selected_pivot','next_ticket','next_topic','metadata_work_readiness','code_change_readiness','stop_condition')
FIELDS=('story_id','topic','upstream_handoff','closed_candidate_id','selected_rank','selected_candidate_id','selected_bridge_class','source_symbol_context_count','safe_context_status','ready_to_reopen_domain_count','source_patch_authorized_count','selected_domain','selected_pivot','next_ticket','next_topic','metadata_work_readiness','code_change_readiness','stop_condition')
def ranked(repo):
 old=candidates.TOP_LIMIT
 try:
  candidates.TOP_LIMIT=80;rows,_=candidates.build_bridge_candidates(Path(repo))
 finally: candidates.TOP_LIMIT=old
 return next((r for r in rows if r.rank==62),None)
def build(repo):
 with (Path(repo)/UPSTREAM).open(encoding='utf-8',newline='') as h:
  reader=csv.DictReader(h)
  if tuple(reader.fieldnames or ())!=UPFIELDS:raise ValueError('handoff schema drift')
  rows=list(reader)
 if len(rows)!=1:raise ValueError('handoff row-count drift')
 expected={'story_id':'RE-540','topic':'mapped-callee-bridge-readiness-gate','upstream_handoff':'RE-539','selected_candidate_id':'70f02d5b6c66','selected_rank':'61','selected_subcluster':'mapped-callee-bridge-readiness-gate','source_symbol_context_count':'4','bridge_class':'mapped-callee-bridge','safe_context_status':'filtered-metadata-only','source_backed_callsite_count':'0','candidate_level_proof_count':'0','repository_symbol_direct_proof_count':'0','ready_to_reopen_domain_count':'0','source_patch_authorized_count':'0','selected_domain':'none','selected_pivot':'none','next_ticket':'RE-541','next_topic':'ghidra-second-window-next-candidate-selection','metadata_work_readiness':'ready','code_change_readiness':'blocked','stop_condition':'metadata-only safety gate denies proof-domain selection and source changes'}
 if any(rows[0].get(k)!=v for k,v in expected.items()):raise ValueError('handoff drift')
 c=ranked(repo)
 if c is None or (c.candidate_id,c.bridge_class,c.source_context_count,c.ready_to_reopen_domain,c.source_patch_authorized)!=('605d53c8fbfb','mapped-caller-callee-bridge',6,'no','no'):raise ValueError('ranked candidate drift')
 row=dict(story_id='RE-541',topic='ghidra-second-window-next-candidate-selection',upstream_handoff='RE-540',closed_candidate_id=rows[0]['selected_candidate_id'],selected_rank='62',selected_candidate_id='605d53c8fbfb',selected_bridge_class='mapped-caller-callee-bridge',source_symbol_context_count='6',safe_context_status='filtered-metadata-only',ready_to_reopen_domain_count='0',source_patch_authorized_count='0',selected_domain='none',selected_pivot='none',next_ticket='RE-542',next_topic='ghidra-second-window-rank-62-narrow-export',metadata_work_readiness='ready',code_change_readiness='blocked',stop_condition='next ranked metadata candidate selected; source changes remain blocked');validate(row);return row
def validate(row):
 if tuple(row)!=FIELDS:raise ValueError('output schema drift')
 if any(x in '\n'.join(map(str,row.values())).lower() for x in BAD):raise ValueError('forbidden output fragment')
 if (row['code_change_readiness'],row['source_patch_authorized_count'],row['safe_context_status'])!=('blocked','0','filtered-metadata-only'):raise ValueError('output safety drift')
def write(row,repo):
 validate(row);repo=Path(repo);out=[]
 for s in ('candidates','summary','handoff'):
  p=repo/'docs/reverse/generated'/f'{PREFIX}-{s}.csv';p.parent.mkdir(parents=True,exist_ok=True)
  with p.open('w',encoding='utf-8',newline='') as h:w=csv.DictWriter(h,fieldnames=FIELDS,lineterminator='\n');w.writeheader();w.writerow(row)
  out.append(p)
 docs={repo/'docs/reverse/functions/re541-ghidra-second-window-next-candidate-selection.md':'# RE-541 selection\n\nFiltered metadata-only decision; source and code work remain blocked.\n',repo/'docs/stories/RE-541-ghidra-second-window-next-candidate-selection.md':'# RE-541 selection\n\n## Progress tracker\n\n- [x] RE-540 handoff validated.\n- [x] Filtered metadata decision recorded.\n- [x] RE-542 selected; not executed.\n'}
 for p,t in docs.items():p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t,encoding='utf-8');out.append(p)
 if any(x in p.read_text(encoding='utf-8').lower() for p in out for x in BAD):raise ValueError('forbidden written fragment')
 return out
if __name__=='__main__':write(build(ROOT),ROOT)
