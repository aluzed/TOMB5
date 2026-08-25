"""Fail-closed metadata-only RE-583 candidate selection."""
import csv, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from scripts.reverse import re556_ghidra_second_window_next_candidate_selection as base
BAD,UPFIELDS,FIELDS=base.BAD,base.UPFIELDS,base.FIELDS
UPSTREAM='docs/reverse/generated/re582-mapped-caller-bridge-readiness-gate-handoff.csv'
PREFIX='re583-ghidra-second-window-next-candidate-selection'
def build(repo):
 with (Path(repo)/UPSTREAM).open(encoding='utf-8',newline='') as h:
  reader=csv.DictReader(h)
  if tuple(reader.fieldnames or ())!=UPFIELDS: raise ValueError('handoff schema drift')
  rows=list(reader)
 expected={'story_id':'RE-582','topic':'mapped-caller-bridge-readiness-gate','upstream_handoff':'RE-581','selected_candidate_id':'792bbf9b7b74','selected_rank':'75','selected_subcluster':'mapped-caller-bridge-readiness-gate','source_symbol_context_count':'6','bridge_class':'mapped-caller-bridge','safe_context_status':'filtered-metadata-only','source_backed_callsite_count':'0','candidate_level_proof_count':'0','repository_symbol_direct_proof_count':'0','ready_to_reopen_domain_count':'0','source_patch_authorized_count':'0','selected_domain':'none','selected_pivot':'none','next_ticket':'RE-583','next_topic':'ghidra-second-window-next-candidate-selection','metadata_work_readiness':'ready','code_change_readiness':'blocked','stop_condition':'metadata-only safety gate denies proof-domain selection and source changes'}
 if len(rows)!=1 or any(rows[0].get(k)!=v for k,v in expected.items()): raise ValueError('handoff drift')
 old=base.candidates.TOP_LIMIT
 try:
  base.candidates.TOP_LIMIT=100;entries,_=base.candidates.build_bridge_candidates(Path(repo))
 finally: base.candidates.TOP_LIMIT=old
 c=next((x for x in entries if x.rank==76),None)
 actual=None if c is None else (c.candidate_id,c.bridge_class,c.source_context_count,c.ready_to_reopen_domain,c.source_patch_authorized)
 if actual!=('8f7269b61897','mapped-caller-callee-bridge',6,'no','no'): raise ValueError('ranked candidate drift')
 row=dict(story_id='RE-583',topic='ghidra-second-window-next-candidate-selection',upstream_handoff='RE-582',closed_candidate_id=rows[0]['selected_candidate_id'],selected_rank='76',selected_candidate_id='8f7269b61897',selected_bridge_class='mapped-caller-callee-bridge',source_symbol_context_count='6',safe_context_status='filtered-metadata-only',ready_to_reopen_domain_count='0',source_patch_authorized_count='0',selected_domain='none',selected_pivot='none',next_ticket='RE-584',next_topic='ghidra-second-window-rank-76-narrow-export',metadata_work_readiness='ready',code_change_readiness='blocked',stop_condition='next ranked metadata candidate selected; source changes remain blocked')
 validate(row);return row
def validate(row):
 if tuple(row)!=FIELDS: raise ValueError('output schema drift')
 if any(x in '\n'.join(map(str,row.values())).lower() for x in BAD): raise ValueError('forbidden output fragment')
 if (row['code_change_readiness'],row['source_patch_authorized_count'],row['safe_context_status'])!=('blocked','0','filtered-metadata-only'): raise ValueError('output safety drift')
def write(row,repo):
 validate(row);repo=Path(repo);out=[]
 for suffix in ('candidates','summary','handoff'):
  p=repo/'docs/reverse/generated'/f'{PREFIX}-{suffix}.csv';p.parent.mkdir(parents=True,exist_ok=True)
  with p.open('w',encoding='utf-8',newline='') as h:
   w=csv.DictWriter(h,fieldnames=FIELDS,lineterminator='\n');w.writeheader();w.writerow(row)
  out.append(p)
 docs={repo/'docs/reverse/functions/re583-ghidra-second-window-next-candidate-selection.md':'# RE-583 selection\n\nFiltered metadata-only decision; source and code work remain blocked.\n',repo/'docs/stories/RE-583-ghidra-second-window-next-candidate-selection.md':'# RE-583 selection\n\n## Progress tracker\n\n- [x] RE-582 handoff validated.\n- [x] Filtered metadata decision recorded.\n- [x] RE-584 selected; not executed.\n'}
 for p,t in docs.items(): p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t,encoding='utf-8');out.append(p)
 if any(x in p.read_text(encoding='utf-8').lower() for p in out for x in BAD): raise ValueError('forbidden written fragment')
 return out
if __name__=='__main__': write(build(ROOT),ROOT)
