"""Fail-closed metadata-only RE-604 candidate selection."""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))
from scripts.reverse import re556_ghidra_second_window_next_candidate_selection as base

BAD, UPFIELDS, FIELDS = base.BAD, base.UPFIELDS, base.FIELDS
UPSTREAM='docs/reverse/generated/re603-mapped-caller-callee-bridge-readiness-gate-handoff.csv'
PREFIX='re604-ghidra-second-window-next-candidate-selection'
EXPECTED={
 'story_id':'RE-603','topic':'mapped-caller-callee-bridge-readiness-gate','upstream_handoff':'RE-602',
 'selected_candidate_id':'8d8c7aec748e','selected_rank':'82','selected_subcluster':'mapped-caller-callee-bridge-readiness-gate','source_symbol_context_count':'5','bridge_class':'mapped-caller-callee-bridge','safe_context_status':'filtered-metadata-only','source_backed_callsite_count':'0','candidate_level_proof_count':'0','repository_symbol_direct_proof_count':'0','ready_to_reopen_domain_count':'0','source_patch_authorized_count':'0','selected_domain':'none','selected_pivot':'none','next_ticket':'RE-604','next_topic':'ghidra-second-window-next-candidate-selection','metadata_work_readiness':'ready','code_change_readiness':'blocked','stop_condition':'metadata-only safety gate denies proof-domain selection and production changes'}

def build(repo):
 with (Path(repo)/UPSTREAM).open(encoding='utf-8',newline='') as h:
  reader=csv.DictReader(h)
  if tuple(reader.fieldnames or ()) != UPFIELDS: raise ValueError('handoff schema drift')
  rows=list(reader)
 if len(rows)!=1: raise ValueError('handoff row-count drift')
 for field,value in EXPECTED.items():
  if rows[0].get(field)!=value: raise ValueError(f'handoff drift: {field}')
 old_limit=base.candidates.TOP_LIMIT
 try:
  base.candidates.TOP_LIMIT=100; entries,_=base.candidates.build_bridge_candidates(Path(repo))
 finally: base.candidates.TOP_LIMIT=old_limit
 candidate=next((entry for entry in entries if entry.rank==83),None)
 actual=None if candidate is None else (candidate.candidate_id,candidate.bridge_class,candidate.source_context_count,candidate.ready_to_reopen_domain,candidate.source_patch_authorized)
 if actual != ('586681647d77','mapped-caller-callee-bridge',5,'no','no'): raise ValueError('ranked candidate drift')
 row=dict(story_id='RE-604',topic='ghidra-second-window-next-candidate-selection',upstream_handoff='RE-603',closed_candidate_id=rows[0]['selected_candidate_id'],selected_rank='83',selected_candidate_id='586681647d77',selected_bridge_class='mapped-caller-callee-bridge',source_symbol_context_count='5',safe_context_status='filtered-metadata-only',ready_to_reopen_domain_count='0',source_patch_authorized_count='0',selected_domain='none',selected_pivot='none',next_ticket='RE-605',next_topic='ghidra-second-window-rank-83-narrow-export',metadata_work_readiness='ready',code_change_readiness='blocked',stop_condition='next ranked metadata candidate selected; production changes remain blocked')
 validate(row); return row

def validate(row):
 if tuple(row)!=FIELDS: raise ValueError('output schema drift')
 if any(x in '\n'.join(map(str,row.values())).lower() for x in BAD): raise ValueError('forbidden output fragment')
 if (row['code_change_readiness'],row['source_patch_authorized_count'],row['safe_context_status']) != ('blocked','0','filtered-metadata-only'): raise ValueError('output safety drift')

def write(row,repo):
 validate(row); repo=Path(repo); outputs=[]
 for suffix in ('candidates','summary','handoff'):
  p=repo/'docs/reverse/generated'/f'{PREFIX}-{suffix}.csv'; p.parent.mkdir(parents=True,exist_ok=True)
  with p.open('w',encoding='utf-8',newline='') as h:
   w=csv.DictWriter(h,fieldnames=FIELDS,lineterminator='\n'); w.writeheader(); w.writerow(row)
  outputs.append(p)
 docs={repo/'docs/reverse/functions/re604-ghidra-second-window-next-candidate-selection.md':'# RE-604 selection\n\nFiltered metadata-only decision; production and code work remain blocked.\n',repo/'docs/stories/RE-604-ghidra-second-window-next-candidate-selection.md':'# RE-604 selection\n\n## Progress tracker\n\n- [x] RE-603 handoff validated.\n- [x] Rank-83 candidate selected from the fixed safe ranking.\n- [x] Filtered metadata-only safety retained.\n- [x] Production and code work remain blocked.\n- [x] RE-605 selected; not executed.\n'}
 for p,text in docs.items(): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(text,encoding='utf-8'); outputs.append(p)
 for p in outputs:
  if any(x in p.read_text(encoding='utf-8').lower() for x in BAD): raise ValueError('forbidden written fragment')
 return outputs

if __name__=='__main__': write(build(ROOT),ROOT)
