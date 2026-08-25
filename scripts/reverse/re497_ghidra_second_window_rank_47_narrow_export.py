"""Produce the fail-closed, metadata-only RE-497 rank-47 narrow export."""
import csv
from pathlib import Path
BAD=('0x','fun_','sub_','word_le_hex','payload_offset','opcode','machine word','raw dump','raw evidence','raw_evidence','call_address','branch target','call target','ghidra_entry','ghidra_name','source_line_text','code.wad','gamewad.obj','secret','private key','credential','asset','raw binary','source patch','address','symbol evidence','copyright')
FORBIDDEN_OUTPUT_FRAGMENTS=BAD
UPSTREAM='docs/reverse/generated/re496-ghidra-second-window-next-candidate-selection-handoff.csv';PREFIX='re497-ghidra-second-window-rank-47-narrow-export'
UPFIELDS=('story_id','topic','upstream_handoff','closed_candidate_id','selected_rank','selected_candidate_id','selected_bridge_class','source_symbol_context_count','safe_context_status','ready_to_reopen_domain_count','source_patch_authorized_count','selected_domain','selected_pivot','next_ticket','next_topic','metadata_work_readiness','code_change_readiness','stop_condition')
FIELDS=('story_id','topic','upstream_handoff','selected_candidate_id','selected_rank','selected_subcluster','source_symbol_context_count','bridge_class','safe_context_status','candidate_level_proof_count','ready_to_reopen_domain_count','source_patch_authorized_count','selected_domain','selected_pivot','next_ticket','next_topic','metadata_work_readiness','code_change_readiness','stop_condition')
TICKET='RE-497';TOPIC='ghidra-second-window-rank-47-narrow-export';NEXT='RE-498';NEXT_TOPIC='mapped-caller-callee-bridge-readiness-gate';CANDIDATE='afcb272bc095';RANK='47';BRIDGE='mapped-caller-callee-bridge';CONTEXTS='5';STOP='narrow rank-47 export requires readiness gate before proof-domain selection'
def read_upstream(repo):
 with (Path(repo)/UPSTREAM).open(encoding='utf-8',newline='') as h:r=csv.DictReader(h);assert tuple(r.fieldnames or ())==UPFIELDS,'handoff schema drift';rows=list(r)
 if len(rows)!=1:raise ValueError('handoff row-count drift')
 r=rows[0];expected={'story_id':'RE-496','topic':'ghidra-second-window-next-candidate-selection','upstream_handoff':'RE-495','closed_candidate_id':'8ac39f9a6a85','selected_rank':RANK,'selected_candidate_id':CANDIDATE,'selected_bridge_class':BRIDGE,'source_symbol_context_count':CONTEXTS,'safe_context_status':'filtered-metadata-only','ready_to_reopen_domain_count':'0','source_patch_authorized_count':'0','selected_domain':'none','selected_pivot':'none','next_ticket':TICKET,'next_topic':TOPIC,'metadata_work_readiness':'ready','code_change_readiness':'blocked','stop_condition':'next ranked metadata candidate selected; source changes remain blocked'}
 for k,v in expected.items():
  if r.get(k)!=v:raise ValueError(f'handoff drift: {k}')
 return r
def build(repo):
 r=read_upstream(repo);o=dict(story_id=TICKET,topic=TOPIC,upstream_handoff='RE-496',selected_candidate_id=r['selected_candidate_id'],selected_rank=r['selected_rank'],selected_subcluster=NEXT_TOPIC,source_symbol_context_count=r['source_symbol_context_count'],bridge_class=r['selected_bridge_class'],safe_context_status='filtered-metadata-only',candidate_level_proof_count='0',ready_to_reopen_domain_count='0',source_patch_authorized_count='0',selected_domain='none',selected_pivot='none',next_ticket=NEXT,next_topic=NEXT_TOPIC,metadata_work_readiness='ready',code_change_readiness='blocked',stop_condition=STOP);validate(o);return o
def validate(o):
 if tuple(o)!=FIELDS:raise ValueError('output schema drift')
 if any(x in '\n'.join(map(str,o.values())).lower() for x in BAD):raise ValueError('forbidden output fragment')
 expected={'story_id':TICKET,'topic':TOPIC,'upstream_handoff':'RE-496','selected_candidate_id':CANDIDATE,'selected_rank':RANK,'selected_subcluster':NEXT_TOPIC,'source_symbol_context_count':CONTEXTS,'bridge_class':BRIDGE,'safe_context_status':'filtered-metadata-only','candidate_level_proof_count':'0','ready_to_reopen_domain_count':'0','source_patch_authorized_count':'0','selected_domain':'none','selected_pivot':'none','next_ticket':NEXT,'next_topic':NEXT_TOPIC,'metadata_work_readiness':'ready','code_change_readiness':'blocked','stop_condition':STOP}
 for k,v in expected.items():
  if o.get(k)!=v:raise ValueError(f'output safety drift: {k}')
def write(o,repo):
 validate(o);repo=Path(repo);out=[]
 for s in ('contexts','summary','handoff'):
  p=repo/'docs/reverse/generated'/f'{PREFIX}-{s}.csv';p.parent.mkdir(parents=True,exist_ok=True)
  with p.open('w',encoding='utf-8',newline='') as h:w=csv.DictWriter(h,fieldnames=FIELDS,lineterminator='\n');w.writeheader();w.writerow(o)
  out.append(p)
 for p,t in {repo/'docs/reverse/functions/re497-ghidra-second-window-rank-47-narrow-export.md':'# RE-497 rank-47 narrow export\n\nThe selected candidate is filtered metadata only; source and code work remain blocked.\n',repo/'docs/stories/RE-497-ghidra-second-window-rank-47-narrow-export.md':'# RE-497 rank-47 narrow export\n\n## Progress tracker\n\n- [x] RE-496 handoff validated.\n- [x] Rank-47 context narrowed.\n- [x] Filtered metadata-only safety retained.\n- [x] Source and code work remain blocked.\n- [x] RE-498 selected; not executed.\n'}.items():p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t,encoding='utf-8');out.append(p)
 for p in out:
  if any(x in p.read_text(encoding='utf-8').lower() for x in BAD):raise ValueError('forbidden written fragment')
 return out
if __name__=='__main__':
 ROOT=Path(__file__).resolve().parents[2];write(build(ROOT),ROOT)
