"""Fail-closed metadata-only readiness gate for RE-495."""
import csv
from pathlib import Path
BAD=('0x','fun_','sub_','word_le_hex','payload_offset','opcode','machine word','raw dump','raw evidence','raw_evidence','call_address','branch target','call target','ghidra_entry','ghidra_name','source_line_text','code.wad','gamewad.obj','secret','private key','credential','asset','raw binary','source patch','address','symbol evidence','copyright')
FORBIDDEN_OUTPUT_FRAGMENTS=BAD
FIELDS=('story_id','topic','upstream_handoff','selected_candidate_id','selected_rank','selected_subcluster','source_symbol_context_count','bridge_class','safe_context_status','source_backed_callsite_count','candidate_level_proof_count','repository_symbol_direct_proof_count','ready_to_reopen_domain_count','source_patch_authorized_count','selected_domain','selected_pivot','next_ticket','next_topic','metadata_work_readiness','code_change_readiness','stop_condition')
UPSTREAM_FIELDS=('story_id','topic','upstream_handoff','selected_candidate_id','selected_rank','selected_subcluster','source_symbol_context_count','bridge_class','safe_context_status','candidate_level_proof_count','ready_to_reopen_domain_count','source_patch_authorized_count','selected_domain','selected_pivot','next_ticket','next_topic','metadata_work_readiness','code_change_readiness','stop_condition')
TICKET='RE-495';TOPIC='mapped-caller-callee-bridge-readiness-gate';UPSTREAM='RE-494';CANDIDATE='8ac39f9a6a85';RANK='46';CONTEXTS='5';BRIDGE='mapped-caller-callee-bridge';NEXT='RE-496';NEXT_TOPIC='ghidra-second-window-next-candidate-selection';STOP='metadata-only safety gate denies proof-domain selection and source changes'
def read_upstream(repo):
 with (Path(repo)/'docs/reverse/generated/re494-ghidra-second-window-rank-46-narrow-export-handoff.csv').open(encoding='utf-8',newline='') as h:
  reader=csv.DictReader(h)
  if tuple(reader.fieldnames or ())!=UPSTREAM_FIELDS:raise ValueError('handoff schema drift')
  rows=list(reader)
 if len(rows)!=1:raise ValueError('handoff row-count drift')
 r=rows[0];expected={'story_id':UPSTREAM,'topic':'ghidra-second-window-rank-46-narrow-export','upstream_handoff':'RE-493','selected_candidate_id':CANDIDATE,'selected_rank':RANK,'selected_subcluster':TOPIC,'source_symbol_context_count':CONTEXTS,'bridge_class':BRIDGE,'safe_context_status':'filtered-metadata-only','candidate_level_proof_count':'0','ready_to_reopen_domain_count':'0','source_patch_authorized_count':'0','selected_domain':'none','selected_pivot':'none','next_ticket':TICKET,'next_topic':TOPIC,'metadata_work_readiness':'ready','code_change_readiness':'blocked','stop_condition':'narrow rank-46 export requires readiness gate before proof-domain selection'}
 for k,v in expected.items():
  if r.get(k)!=v:raise ValueError(f'handoff drift: {k}')
 return r
def build(repo):
 read_upstream(repo);r=dict(story_id=TICKET,topic=TOPIC,upstream_handoff=UPSTREAM,selected_candidate_id=CANDIDATE,selected_rank=RANK,selected_subcluster=TOPIC,source_symbol_context_count=CONTEXTS,bridge_class=BRIDGE,safe_context_status='filtered-metadata-only',source_backed_callsite_count='0',candidate_level_proof_count='0',repository_symbol_direct_proof_count='0',ready_to_reopen_domain_count='0',source_patch_authorized_count='0',selected_domain='none',selected_pivot='none',next_ticket=NEXT,next_topic=NEXT_TOPIC,metadata_work_readiness='ready',code_change_readiness='blocked',stop_condition=STOP);validate_output(r);return r
def validate_output(r):
 if tuple(r)!=FIELDS:raise ValueError('output schema drift')
 expected={'story_id':TICKET,'topic':TOPIC,'upstream_handoff':UPSTREAM,'selected_candidate_id':CANDIDATE,'selected_rank':RANK,'selected_subcluster':TOPIC,'source_symbol_context_count':CONTEXTS,'bridge_class':BRIDGE,'safe_context_status':'filtered-metadata-only','source_backed_callsite_count':'0','candidate_level_proof_count':'0','repository_symbol_direct_proof_count':'0','ready_to_reopen_domain_count':'0','source_patch_authorized_count':'0','selected_domain':'none','selected_pivot':'none','next_ticket':NEXT,'next_topic':NEXT_TOPIC,'metadata_work_readiness':'ready','code_change_readiness':'blocked','stop_condition':STOP}
 if any(x in '\n'.join(map(str,r.values())).lower() for x in BAD):raise ValueError('forbidden output fragment')
 for k,v in expected.items():
  if r.get(k)!=v:raise ValueError(f'output safety drift: {k}')
def write(r,repo):
 validate_output(r);repo=Path(repo);out=[];prefix='re495-mapped-caller-callee-bridge-readiness-gate'
 for suffix in ('gate','summary','handoff'):
  p=repo/'docs/reverse/generated'/f'{prefix}-{suffix}.csv';p.parent.mkdir(parents=True,exist_ok=True)
  with p.open('w',encoding='utf-8',newline='') as h:w=csv.DictWriter(h,fieldnames=FIELDS,lineterminator='\n');w.writeheader();w.writerow(r)
  out.append(p)
 docs={repo/'docs/reverse/functions/re495-mapped-caller-callee-bridge-readiness-gate.md':'# RE-495 readiness gate\n\nFiltered metadata-only decision; source and code work remain blocked.\n',repo/'docs/stories/RE-495-mapped-caller-callee-bridge-readiness-gate.md':'# RE-495 readiness gate\n\n## Progress tracker\n\n- [x] RE-494 handoff validated.\n- [x] Filtered metadata decision recorded.\n- [x] Safety guard retained.\n- [x] Source and code work remain blocked.\n- [x] RE-496 selected; not executed.\n'}
 for p,text in docs.items():p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8');out.append(p)
 for p in out:
  if any(x in p.read_text(encoding='utf-8').lower() for x in BAD):raise ValueError('forbidden written fragment')
 return out
if __name__=='__main__':
 ROOT=Path(__file__).resolve().parents[2];write(build(ROOT),ROOT)
