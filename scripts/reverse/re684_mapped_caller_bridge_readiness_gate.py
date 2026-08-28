"""Fail-closed metadata-only RE-684 readiness gate."""
import csv, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from scripts.reverse import re678_mapped_caller_callee_bridge_readiness_gate as base
BAD,UPFIELDS,FIELDS=base.BAD,base.UPFIELDS,base.FIELDS
UPSTREAM='docs/reverse/generated/re683-ghidra-second-window-rank-109-narrow-export-handoff.csv'
PREFIX='re684-mapped-caller-bridge-readiness-gate'
EXPECTED={'story_id':'RE-683','topic':'ghidra-second-window-rank-109-narrow-export','upstream_handoff':'RE-682','selected_candidate_id':'08963c88efc1','selected_rank':'109','selected_subcluster':'mapped-caller-bridge-readiness-gate','source_symbol_context_count':'4','bridge_class':'mapped-caller-bridge','safe_context_status':'filtered-metadata-only','candidate_level_proof_count':'0','ready_to_reopen_domain_count':'0','source_patch_authorized_count':'0','selected_domain':'none','selected_pivot':'none','next_ticket':'RE-684','next_topic':'mapped-caller-bridge-readiness-gate','metadata_work_readiness':'ready','code_change_readiness':'blocked','stop_condition':'narrow rank-109 export requires readiness gate before proof-domain selection'}
OUTPUT={'story_id':'RE-684','topic':'mapped-caller-bridge-readiness-gate','upstream_handoff':'RE-683','selected_candidate_id':'08963c88efc1','selected_rank':'109','selected_subcluster':'mapped-caller-bridge-readiness-gate','source_symbol_context_count':'4','bridge_class':'mapped-caller-bridge','safe_context_status':'filtered-metadata-only','source_backed_callsite_count':'0','candidate_level_proof_count':'0','repository_symbol_direct_proof_count':'0','ready_to_reopen_domain_count':'0','source_patch_authorized_count':'0','selected_domain':'none','selected_pivot':'none','next_ticket':'RE-685','next_topic':'ghidra-second-window-next-candidate-selection','metadata_work_readiness':'ready','code_change_readiness':'blocked','stop_condition':'metadata-only safety gate denies proof-domain selection and production changes'}
def build(repo):
 with (Path(repo)/UPSTREAM).open(encoding='utf-8',newline='') as f:
  reader=csv.DictReader(f)
  if tuple(reader.fieldnames or ())!=UPFIELDS: raise ValueError('handoff schema drift')
  rows=list(reader)
 if any(None in r for r in rows): raise ValueError('handoff row schema drift')
 if len(rows)!=1: raise ValueError('handoff row-count drift')
 for field,value in EXPECTED.items():
  if rows[0].get(field)!=value: raise ValueError(f'handoff drift: {field}')
 row=dict(OUTPUT);validate(row);return row
def validate(row):
 if tuple(row)!=FIELDS: raise ValueError('output schema drift')
 if row!=OUTPUT: raise ValueError('output drift')
 if any(x in '\n'.join(row.values()).lower() for x in BAD): raise ValueError('forbidden output fragment')
def write(row,repo):
 validate(row);repo=Path(repo);out=[]
 for suffix in ('gate','summary','handoff'):
  p=repo/'docs/reverse/generated'/f'{PREFIX}-{suffix}.csv';p.parent.mkdir(parents=True,exist_ok=True)
  with p.open('w',encoding='utf-8',newline='') as f:
   w=csv.DictWriter(f,fieldnames=FIELDS,lineterminator='\n');w.writeheader();w.writerow(row)
  out.append(p)
 docs={repo/'docs/reverse/functions/re684-mapped-caller-bridge-readiness-gate.md':'# RE-684 readiness gate\n\nFiltered metadata-only decision; production and code work remain blocked.\n',repo/'docs/stories/RE-684-mapped-caller-bridge-readiness-gate.md':'# RE-684 readiness gate\n\n## Progress tracker\n\n- [x] RE-683 handoff validated.\n- [x] Filtered metadata decision recorded.\n- [x] Safety guard retained.\n- [x] Production and code work remain blocked.\n- [x] RE-685 selected; not executed.\n'}
 for p,t in docs.items(): p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t,encoding='utf-8');out.append(p)
 for p in out:
  if any(x in p.read_text(encoding='utf-8').lower() for x in BAD): raise ValueError('forbidden written fragment')
 return out
if __name__=='__main__':write(build(ROOT),ROOT)
