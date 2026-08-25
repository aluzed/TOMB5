"""Fail-closed metadata-only readiness gate for RE-579."""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))
from scripts.reverse import re573_mapped_caller_bridge_readiness_gate as base
BAD, UPFIELDS, FIELDS = base.BAD, base.UPFIELDS, base.FIELDS
UPSTREAM = 'docs/reverse/generated/re578-ghidra-second-window-rank-74-narrow-export-handoff.csv'
PREFIX = 're579-mapped-caller-bridge-readiness-gate'

def build(repo):
    with (Path(repo)/UPSTREAM).open(encoding='utf-8',newline='') as h:
        reader=csv.DictReader(h)
        if tuple(reader.fieldnames or ()) != UPFIELDS: raise ValueError('handoff schema drift')
        rows=list(reader)
    expected={'story_id':'RE-578','topic':'ghidra-second-window-rank-74-narrow-export','upstream_handoff':'RE-577','selected_candidate_id':'9ded6d1f164d','selected_rank':'74','selected_subcluster':'mapped-caller-bridge-readiness-gate','source_symbol_context_count':'6','bridge_class':'mapped-caller-bridge','safe_context_status':'filtered-metadata-only','candidate_level_proof_count':'0','ready_to_reopen_domain_count':'0','source_patch_authorized_count':'0','selected_domain':'none','selected_pivot':'none','next_ticket':'RE-579','next_topic':'mapped-caller-bridge-readiness-gate','metadata_work_readiness':'ready','code_change_readiness':'blocked','stop_condition':'narrow rank-74 export requires readiness gate before proof-domain selection'}
    if len(rows)!=1 or any(rows[0].get(k)!=v for k,v in expected.items()): raise ValueError('handoff drift')
    row=dict(story_id='RE-579',topic='mapped-caller-bridge-readiness-gate',upstream_handoff='RE-578',selected_candidate_id='9ded6d1f164d',selected_rank='74',selected_subcluster='mapped-caller-bridge-readiness-gate',source_symbol_context_count='6',bridge_class='mapped-caller-bridge',safe_context_status='filtered-metadata-only',source_backed_callsite_count='0',candidate_level_proof_count='0',repository_symbol_direct_proof_count='0',ready_to_reopen_domain_count='0',source_patch_authorized_count='0',selected_domain='none',selected_pivot='none',next_ticket='RE-580',next_topic='ghidra-second-window-next-candidate-selection',metadata_work_readiness='ready',code_change_readiness='blocked',stop_condition='metadata-only safety gate denies proof-domain selection and source changes')
    validate(row);return row

def validate(row):
    if tuple(row)!=FIELDS: raise ValueError('output schema drift')
    if any(x in '\n'.join(map(str,row.values())).lower() for x in BAD): raise ValueError('forbidden output fragment')
    if (row['code_change_readiness'],row['source_patch_authorized_count'],row['safe_context_status'])!=('blocked','0','filtered-metadata-only'): raise ValueError('output safety drift')

def write(row,repo):
    validate(row);repo=Path(repo);outputs=[]
    for suffix in ('gate','summary','handoff'):
        p=repo/'docs/reverse/generated'/f'{PREFIX}-{suffix}.csv';p.parent.mkdir(parents=True,exist_ok=True)
        with p.open('w',encoding='utf-8',newline='') as h:
            w=csv.DictWriter(h,fieldnames=FIELDS,lineterminator='\n');w.writeheader();w.writerow(row)
        outputs.append(p)
    documents={repo/'docs/reverse/functions/re579-mapped-caller-bridge-readiness-gate.md':'# RE-579 readiness gate\n\nFiltered metadata-only decision; source and code work remain blocked.\n',repo/'docs/stories/RE-579-mapped-caller-bridge-readiness-gate.md':'# RE-579 readiness gate\n\n## Progress tracker\n\n- [x] RE-578 handoff validated.\n- [x] Filtered metadata decision recorded.\n- [x] Safety guard retained.\n- [x] Source and code work remain blocked.\n- [x] RE-580 selected; not executed.\n'}
    for p,text in documents.items(): p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8');outputs.append(p)
    if any(x in p.read_text(encoding='utf-8').lower() for p in outputs for x in BAD): raise ValueError('forbidden written fragment')
    return outputs
if __name__=='__main__': write(build(ROOT),ROOT)
