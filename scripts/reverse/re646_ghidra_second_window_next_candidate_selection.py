"""Fail-closed metadata-only RE-646 candidate selection."""
import csv
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from scripts.reverse import re643_ghidra_second_window_next_candidate_selection as base
BAD,UPFIELDS,FIELDS=base.BAD,base.UPFIELDS,base.FIELDS
UPSTREAM='docs/reverse/generated/re645-mapped-caller-bridge-readiness-gate-handoff.csv'
PREFIX='re646-ghidra-second-window-next-candidate-selection'
EXPECTED={'story_id':'RE-645','topic':'mapped-caller-bridge-readiness-gate','upstream_handoff':'RE-644','selected_candidate_id':'7129784944ab','selected_rank':'96','selected_subcluster':'mapped-caller-bridge-readiness-gate','source_symbol_context_count':'5','bridge_class':'mapped-caller-bridge','safe_context_status':'filtered-metadata-only','source_backed_callsite_count':'0','candidate_level_proof_count':'0','repository_symbol_direct_proof_count':'0','ready_to_reopen_domain_count':'0','source_patch_authorized_count':'0','selected_domain':'none','selected_pivot':'none','next_ticket':'RE-646','next_topic':'ghidra-second-window-next-candidate-selection','metadata_work_readiness':'ready','code_change_readiness':'blocked','stop_condition':'metadata-only safety gate denies proof-domain selection and production changes'}
def build(repo):
 with (Path(repo)/UPSTREAM).open(encoding='utf-8',newline='') as h:
  reader=csv.DictReader(h)
  if tuple(reader.fieldnames or ())!=UPFIELDS: raise ValueError('handoff schema drift')
  rows=list(reader)
 if len(rows)!=1: raise ValueError('handoff row-count drift')
 for f,v in EXPECTED.items():
  if rows[0].get(f)!=v: raise ValueError(f'handoff drift: {f}')
 old=base.candidate_source.candidates.TOP_LIMIT
 try:
  base.candidate_source.candidates.TOP_LIMIT=100; entries,_=base.candidate_source.candidates.build_bridge_candidates(Path(repo))
 finally: base.candidate_source.candidates.TOP_LIMIT=old
 c=next((x for x in entries if x.rank==97),None)
 if c is None or (c.candidate_id,c.bridge_class,c.source_context_count,c.ready_to_reopen_domain,c.source_patch_authorized)!=('9453fad2974f','mapped-caller-callee-bridge',5,'no','no'): raise ValueError('ranked candidate drift')
 row=dict(story_id='RE-646',topic='ghidra-second-window-next-candidate-selection',upstream_handoff='RE-645',closed_candidate_id='7129784944ab',selected_rank='97',selected_candidate_id='9453fad2974f',selected_bridge_class='mapped-caller-callee-bridge',source_symbol_context_count='5',safe_context_status='filtered-metadata-only',ready_to_reopen_domain_count='0',source_patch_authorized_count='0',selected_domain='none',selected_pivot='none',next_ticket='RE-647',next_topic='ghidra-second-window-rank-97-narrow-export',metadata_work_readiness='ready',code_change_readiness='blocked',stop_condition='next ranked metadata candidate selected; production changes remain blocked');validate(row);return row
def validate(row):
 if tuple(row)!=FIELDS: raise ValueError('output schema drift')
 if any(x in '\n'.join(map(str,row.values())).lower() for x in BAD): raise ValueError('forbidden output fragment')
 if (row['code_change_readiness'],row['source_patch_authorized_count'],row['safe_context_status'])!=('blocked','0','filtered-metadata-only'): raise ValueError('output safety drift')
def write(row,repo):
 validate(row);repo=Path(repo);outs=[]
 for suffix in ('candidates','summary','handoff'):
  p=repo/'docs/reverse/generated'/f'{PREFIX}-{suffix}.csv';p.parent.mkdir(parents=True,exist_ok=True)
  with p.open('w',encoding='utf-8',newline='') as h: w=csv.DictWriter(h,fieldnames=FIELDS,lineterminator='\n');w.writeheader();w.writerow(row)
  outs.append(p)
 docs={repo/'docs/reverse/functions/re646-ghidra-second-window-next-candidate-selection.md':'# RE-646 selection\n\nFiltered metadata-only decision; production and code work remain blocked.\n',repo/'docs/stories/RE-646-ghidra-second-window-next-candidate-selection.md':'# RE-646 selection\n\n## Progress tracker\n\n- [x] RE-645 handoff validated.\n- [x] Rank-97 candidate selected from the fixed safe ranking.\n- [x] Filtered metadata-only safety retained.\n- [x] Production and code work remain blocked.\n- [x] RE-647 selected; not executed.\n'}
 for p,t in docs.items(): p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t,encoding='utf-8');outs.append(p)
 for p in outs:
  if any(x in p.read_text(encoding='utf-8').lower() for x in BAD): raise ValueError('forbidden written fragment')
 return outs
if __name__=='__main__':write(build(ROOT),ROOT)
