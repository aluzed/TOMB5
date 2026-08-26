"""Fail-closed metadata-only RE-605 rank-83 narrow export."""
import csv,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from scripts.reverse import re584_ghidra_second_window_rank_76_narrow_export as base
BAD,FIELDS=base.BAD,base.FIELDS
UPSTREAM='docs/reverse/generated/re604-ghidra-second-window-next-candidate-selection-handoff.csv';PREFIX='re605-ghidra-second-window-rank-83-narrow-export'
UPFIELDS=('story_id','topic','upstream_handoff','closed_candidate_id','selected_rank','selected_candidate_id','selected_bridge_class','source_symbol_context_count','safe_context_status','ready_to_reopen_domain_count','source_patch_authorized_count','selected_domain','selected_pivot','next_ticket','next_topic','metadata_work_readiness','code_change_readiness','stop_condition')
EXPECTED={'story_id':'RE-604','topic':'ghidra-second-window-next-candidate-selection','upstream_handoff':'RE-603','closed_candidate_id':'8d8c7aec748e','selected_rank':'83','selected_candidate_id':'586681647d77','selected_bridge_class':'mapped-caller-callee-bridge','source_symbol_context_count':'5','safe_context_status':'filtered-metadata-only','ready_to_reopen_domain_count':'0','source_patch_authorized_count':'0','selected_domain':'none','selected_pivot':'none','next_ticket':'RE-605','next_topic':'ghidra-second-window-rank-83-narrow-export','metadata_work_readiness':'ready','code_change_readiness':'blocked','stop_condition':'next ranked metadata candidate selected; production changes remain blocked'}
def build(repo):
 with (Path(repo)/UPSTREAM).open(encoding='utf-8',newline='') as h:
  reader=csv.DictReader(h)
  if tuple(reader.fieldnames or ())!=UPFIELDS:raise ValueError('handoff schema drift')
  rows=list(reader)
 if len(rows)!=1:raise ValueError('handoff row-count drift')
 for f,v in EXPECTED.items():
  if rows[0].get(f)!=v:raise ValueError(f'handoff drift: {f}')
 row=dict(story_id='RE-605',topic='ghidra-second-window-rank-83-narrow-export',upstream_handoff='RE-604',selected_candidate_id='586681647d77',selected_rank='83',selected_subcluster='mapped-caller-callee-bridge-readiness-gate',source_symbol_context_count='5',bridge_class='mapped-caller-callee-bridge',safe_context_status='filtered-metadata-only',candidate_level_proof_count='0',ready_to_reopen_domain_count='0',source_patch_authorized_count='0',selected_domain='none',selected_pivot='none',next_ticket='RE-606',next_topic='mapped-caller-callee-bridge-readiness-gate',metadata_work_readiness='ready',code_change_readiness='blocked',stop_condition='narrow rank-83 export requires readiness gate before proof-domain selection')
 validate(row);return row
def validate(row):
 if tuple(row)!=FIELDS:raise ValueError('output schema drift')
 if any(x in '\n'.join(map(str,row.values())).lower() for x in BAD):raise ValueError('forbidden output fragment')
 if (row['code_change_readiness'],row['source_patch_authorized_count'],row['safe_context_status'])!=('blocked','0','filtered-metadata-only'):raise ValueError('output safety drift')
def write(row,repo):
 validate(row);repo=Path(repo);outs=[]
 for suffix in ('contexts','summary','handoff'):
  p=repo/'docs/reverse/generated'/f'{PREFIX}-{suffix}.csv';p.parent.mkdir(parents=True,exist_ok=True)
  with p.open('w',encoding='utf-8',newline='') as h:w=csv.DictWriter(h,fieldnames=FIELDS,lineterminator='\n');w.writeheader();w.writerow(row)
  outs.append(p)
 docs={repo/'docs/reverse/functions/re605-ghidra-second-window-rank-83-narrow-export.md':'# RE-605 rank-83 narrow export\n\nThe selected candidate is filtered metadata only; production and code work remain blocked.\n',repo/'docs/stories/RE-605-ghidra-second-window-rank-83-narrow-export.md':'# RE-605 rank-83 narrow export\n\n## Progress tracker\n\n- [x] RE-604 handoff validated.\n- [x] Rank-83 context narrowed.\n- [x] Filtered metadata-only safety retained.\n- [x] Production and code work remain blocked.\n- [x] RE-606 selected; not executed.\n'}
 for p,t in docs.items():p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t,encoding='utf-8');outs.append(p)
 for p in outs:
  if any(x in p.read_text(encoding='utf-8').lower() for x in BAD):raise ValueError('forbidden written fragment')
 return outs
if __name__=='__main__':write(build(ROOT),ROOT)
