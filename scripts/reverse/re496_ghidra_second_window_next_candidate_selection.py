"""Fail-closed metadata-only RE-496 candidate selection."""
import csv,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from scripts.reverse import re309_ghidra_unmapped_bridge_candidates as candidates
BAD=('0x','fun_','sub_','opcode','machine word','raw dump','raw evidence','call_address','ghidra_entry','code.wad','gamewad.obj','secret','credential','asset','raw binary','source patch','address','copyright')
FIELDS=('story_id','topic','upstream_handoff','closed_candidate_id','selected_rank','selected_candidate_id','selected_bridge_class','source_symbol_context_count','safe_context_status','ready_to_reopen_domain_count','source_patch_authorized_count','selected_domain','selected_pivot','next_ticket','next_topic','metadata_work_readiness','code_change_readiness','stop_condition')
UPFIELDS=('story_id','topic','upstream_handoff','selected_candidate_id','selected_rank','selected_subcluster','source_symbol_context_count','bridge_class','safe_context_status','source_backed_callsite_count','candidate_level_proof_count','repository_symbol_direct_proof_count','ready_to_reopen_domain_count','source_patch_authorized_count','selected_domain','selected_pivot','next_ticket','next_topic','metadata_work_readiness','code_change_readiness','stop_condition')
def ranked(repo):
 old=candidates.TOP_LIMIT
 try:candidates.TOP_LIMIT=60;rows,_=candidates.build_bridge_candidates(Path(repo))
 finally:candidates.TOP_LIMIT=old
 return next((x for x in rows if x.rank==47),None)
def build(repo):
 p=Path(repo)/'docs/reverse/generated/re495-mapped-caller-callee-bridge-readiness-gate-handoff.csv'
 with p.open(encoding='utf-8',newline='') as h:r=csv.DictReader(h);assert tuple(r.fieldnames or ())==UPFIELDS,'handoff schema drift';rows=list(r)
 if len(rows)!=1:raise ValueError('handoff row-count drift')
 h=rows[0];expected={'story_id':'RE-495','topic':'mapped-caller-callee-bridge-readiness-gate','upstream_handoff':'RE-494','selected_candidate_id':'8ac39f9a6a85','selected_rank':'46','selected_subcluster':'mapped-caller-callee-bridge-readiness-gate','source_symbol_context_count':'5','bridge_class':'mapped-caller-callee-bridge','safe_context_status':'filtered-metadata-only','source_backed_callsite_count':'0','candidate_level_proof_count':'0','repository_symbol_direct_proof_count':'0','ready_to_reopen_domain_count':'0','source_patch_authorized_count':'0','selected_domain':'none','selected_pivot':'none','next_ticket':'RE-496','next_topic':'ghidra-second-window-next-candidate-selection','metadata_work_readiness':'ready','code_change_readiness':'blocked','stop_condition':'metadata-only safety gate denies proof-domain selection and source changes'}
 for k,v in expected.items():
  if h.get(k)!=v:raise ValueError(f'handoff drift: {k}')
 c=ranked(repo)
 if c is None or (c.candidate_id,c.bridge_class,c.source_context_count,c.ready_to_reopen_domain,c.source_patch_authorized)!=('afcb272bc095','mapped-caller-callee-bridge',5,'no','no'):raise ValueError('ranked candidate drift')
 o=dict(story_id='RE-496',topic='ghidra-second-window-next-candidate-selection',upstream_handoff='RE-495',closed_candidate_id=h['selected_candidate_id'],selected_rank='47',selected_candidate_id='afcb272bc095',selected_bridge_class='mapped-caller-callee-bridge',source_symbol_context_count='5',safe_context_status='filtered-metadata-only',ready_to_reopen_domain_count='0',source_patch_authorized_count='0',selected_domain='none',selected_pivot='none',next_ticket='RE-497',next_topic='ghidra-second-window-rank-47-narrow-export',metadata_work_readiness='ready',code_change_readiness='blocked',stop_condition='next ranked metadata candidate selected; source changes remain blocked');validate(o);return o
def validate(o):
 if tuple(o)!=FIELDS:raise ValueError('output schema drift')
 if any(x in '\n'.join(o.values()).lower() for x in BAD):raise ValueError('forbidden output fragment')
 if o['code_change_readiness']!='blocked' or o['source_patch_authorized_count']!='0' or o['safe_context_status']!='filtered-metadata-only':raise ValueError('output safety drift')
def write(o,repo):
 validate(o);repo=Path(repo);out=[]
 for s in ('candidates','summary','handoff'):
  p=repo/'docs/reverse/generated'/f're496-ghidra-second-window-next-candidate-selection-{s}.csv';p.parent.mkdir(parents=True,exist_ok=True)
  with p.open('w',encoding='utf-8',newline='') as h:w=csv.DictWriter(h,fieldnames=FIELDS,lineterminator='\n');w.writeheader();w.writerow(o)
  out.append(p)
 for p,t in {repo/'docs/reverse/functions/re496-ghidra-second-window-next-candidate-selection.md':'# RE-496 selection\n\nFiltered metadata-only decision; source and code work remain blocked.\n',repo/'docs/stories/RE-496-ghidra-second-window-next-candidate-selection.md':'# RE-496 selection\n\n## Progress tracker\n\n- [x] RE-495 handoff validated.\n- [x] Filtered metadata decision recorded.\n- [x] RE-497 selected; not executed.\n'}.items():p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t,encoding='utf-8');out.append(p)
 for p in out:
  if any(x in p.read_text(encoding='utf-8').lower() for x in BAD):raise ValueError('forbidden written fragment')
 return out
if __name__=='__main__':write(build(ROOT),ROOT)
