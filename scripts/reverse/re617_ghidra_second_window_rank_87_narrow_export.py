"""Fail-closed metadata-only RE-617 rank-87 narrow export."""
import csv,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from scripts.reverse import re614_ghidra_second_window_rank_86_narrow_export as base
BAD,FIELDS=base.BAD,base.FIELDS
UPSTREAM='docs/reverse/generated/re616-ghidra-second-window-next-candidate-selection-handoff.csv';PREFIX='re617-ghidra-second-window-rank-87-narrow-export'
UPFIELDS=('story_id','topic','upstream_handoff','closed_candidate_id','selected_rank','selected_candidate_id','selected_bridge_class','source_symbol_context_count','safe_context_status','ready_to_reopen_domain_count','source_patch_authorized_count','selected_domain','selected_pivot','next_ticket','next_topic','metadata_work_readiness','code_change_readiness','stop_condition')
EXPECTED={'story_id':'RE-616','topic':'ghidra-second-window-next-candidate-selection','upstream_handoff':'RE-615','closed_candidate_id':'4fc5988c65ba','selected_rank':'87','selected_candidate_id':'b90186552003','selected_bridge_class':'mapped-caller-bridge','source_symbol_context_count':'5','safe_context_status':'filtered-metadata-only','ready_to_reopen_domain_count':'0','source_patch_authorized_count':'0','selected_domain':'none','selected_pivot':'none','next_ticket':'RE-617','next_topic':'ghidra-second-window-rank-87-narrow-export','metadata_work_readiness':'ready','code_change_readiness':'blocked','stop_condition':'next ranked metadata candidate selected; production changes remain blocked'}
def build(repo):
 with (Path(repo)/UPSTREAM).open(encoding='utf-8',newline='') as h:
  reader=csv.DictReader(h)
  if tuple(reader.fieldnames or ())!=UPFIELDS:raise ValueError('handoff schema drift')
  rows=list(reader)
 if len(rows)!=1:raise ValueError('handoff row-count drift')
 for field,value in EXPECTED.items():
  if rows[0].get(field)!=value:raise ValueError(f'handoff drift: {field}')
 row=dict(story_id='RE-617',topic='ghidra-second-window-rank-87-narrow-export',upstream_handoff='RE-616',selected_candidate_id='b90186552003',selected_rank='87',selected_subcluster='mapped-caller-bridge-readiness-gate',source_symbol_context_count='5',bridge_class='mapped-caller-bridge',safe_context_status='filtered-metadata-only',candidate_level_proof_count='0',ready_to_reopen_domain_count='0',source_patch_authorized_count='0',selected_domain='none',selected_pivot='none',next_ticket='RE-618',next_topic='mapped-caller-bridge-readiness-gate',metadata_work_readiness='ready',code_change_readiness='blocked',stop_condition='narrow rank-87 export requires readiness gate before proof-domain selection')
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
 docs={repo/'docs/reverse/functions/re617-ghidra-second-window-rank-87-narrow-export.md':'# RE-617 rank-87 narrow export\n\nThe selected candidate is filtered metadata only; production and code work remain blocked.\n',repo/'docs/stories/RE-617-ghidra-second-window-rank-87-narrow-export.md':'# RE-617 rank-87 narrow export\n\n## Progress tracker\n\n- [x] RE-616 handoff validated.\n- [x] Rank-87 context narrowed.\n- [x] Filtered metadata-only safety retained.\n- [x] Production and code work remain blocked.\n- [x] RE-618 selected; not executed.\n'}
 for p,t in docs.items():p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t,encoding='utf-8');outs.append(p)
 for p in outs:
  if any(x in p.read_text(encoding='utf-8').lower() for x in BAD):raise ValueError('forbidden written fragment')
 return outs
if __name__=='__main__':write(build(ROOT),ROOT)
