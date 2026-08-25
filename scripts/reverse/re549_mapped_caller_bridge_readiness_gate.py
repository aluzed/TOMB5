"""Fail-closed metadata-only readiness gate for RE-549."""
import csv
from pathlib import Path

BAD=('0x','fun_','sub_','word_le_hex','payload_offset','opcode','machine word','raw dump','raw evidence','raw_evidence','call_address','branch target','call target','ghidra_entry','ghidra_name','source_line_text','code.wad','gamewad.obj','secret','private key','credential','asset','raw binary','source patch','address','symbol evidence','copyright')
UPSTREAM='docs/reverse/generated/re548-ghidra-second-window-rank-64-narrow-export-handoff.csv'
PREFIX='re549-mapped-caller-bridge-readiness-gate'
UPFIELDS=('story_id','topic','upstream_handoff','selected_candidate_id','selected_rank','selected_subcluster','source_symbol_context_count','bridge_class','safe_context_status','candidate_level_proof_count','ready_to_reopen_domain_count','source_patch_authorized_count','selected_domain','selected_pivot','next_ticket','next_topic','metadata_work_readiness','code_change_readiness','stop_condition')
FIELDS=('story_id','topic','upstream_handoff','selected_candidate_id','selected_rank','selected_subcluster','source_symbol_context_count','bridge_class','safe_context_status','source_backed_callsite_count','candidate_level_proof_count','repository_symbol_direct_proof_count','ready_to_reopen_domain_count','source_patch_authorized_count','selected_domain','selected_pivot','next_ticket','next_topic','metadata_work_readiness','code_change_readiness','stop_condition')

def build(repo):
    with (Path(repo)/UPSTREAM).open(encoding='utf-8',newline='') as h:
        reader=csv.DictReader(h)
        if tuple(reader.fieldnames or ())!=UPFIELDS: raise ValueError('handoff schema drift')
        rows=list(reader)
    if len(rows)!=1: raise ValueError('handoff row-count drift')
    expected={'story_id':'RE-548','topic':'ghidra-second-window-rank-64-narrow-export','upstream_handoff':'RE-547','selected_candidate_id':'47d4d3877c3a','selected_rank':'64','selected_subcluster':'mapped-caller-bridge-readiness-gate','source_symbol_context_count':'6','bridge_class':'mapped-caller-bridge','safe_context_status':'filtered-metadata-only','candidate_level_proof_count':'0','ready_to_reopen_domain_count':'0','source_patch_authorized_count':'0','selected_domain':'none','selected_pivot':'none','next_ticket':'RE-549','next_topic':'mapped-caller-bridge-readiness-gate','metadata_work_readiness':'ready','code_change_readiness':'blocked','stop_condition':'narrow rank-64 export requires readiness gate before proof-domain selection'}
    if any(rows[0].get(k)!=v for k,v in expected.items()): raise ValueError('handoff drift')
    row=dict(story_id='RE-549',topic='mapped-caller-bridge-readiness-gate',upstream_handoff='RE-548',selected_candidate_id='47d4d3877c3a',selected_rank='64',selected_subcluster='mapped-caller-bridge-readiness-gate',source_symbol_context_count='6',bridge_class='mapped-caller-bridge',safe_context_status='filtered-metadata-only',source_backed_callsite_count='0',candidate_level_proof_count='0',repository_symbol_direct_proof_count='0',ready_to_reopen_domain_count='0',source_patch_authorized_count='0',selected_domain='none',selected_pivot='none',next_ticket='RE-550',next_topic='ghidra-second-window-next-candidate-selection',metadata_work_readiness='ready',code_change_readiness='blocked',stop_condition='metadata-only safety gate denies proof-domain selection and source changes')
    validate(row);return row

def validate(row):
    if tuple(row)!=FIELDS: raise ValueError('output schema drift')
    if any(x in '\n'.join(map(str,row.values())).lower() for x in BAD): raise ValueError('forbidden output fragment')
    if (row['code_change_readiness'],row['source_patch_authorized_count'],row['safe_context_status'])!=('blocked','0','filtered-metadata-only'): raise ValueError('output safety drift')

def write(row,repo):
    validate(row);repo=Path(repo);out=[]
    for suffix in ('gate','summary','handoff'):
        p=repo/'docs/reverse/generated'/f'{PREFIX}-{suffix}.csv';p.parent.mkdir(parents=True,exist_ok=True)
        with p.open('w',encoding='utf-8',newline='') as h:
            w=csv.DictWriter(h,fieldnames=FIELDS,lineterminator='\n');w.writeheader();w.writerow(row)
        out.append(p)
    docs={repo/'docs/reverse/functions/re549-mapped-caller-bridge-readiness-gate.md':'# RE-549 readiness gate\n\nFiltered metadata-only decision; source and code work remain blocked.\n',repo/'docs/stories/RE-549-mapped-caller-bridge-readiness-gate.md':'# RE-549 readiness gate\n\n## Progress tracker\n\n- [x] RE-548 handoff validated.\n- [x] Filtered metadata decision recorded.\n- [x] Safety guard retained.\n- [x] Source and code work remain blocked.\n- [x] RE-550 selected; not executed.\n'}
    for p,t in docs.items(): p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t,encoding='utf-8');out.append(p)
    if any(x in p.read_text(encoding='utf-8').lower() for p in out for x in BAD): raise ValueError('forbidden written fragment')
    return out
if __name__=='__main__':
    ROOT=Path(__file__).resolve().parents[2];write(build(ROOT),ROOT)
