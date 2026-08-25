"""Produce the fail-closed, metadata-only RE-536 rank-60 narrow export."""
import csv
from pathlib import Path

BAD=('0x','fun_','sub_','word_le_hex','payload_offset','opcode','machine word','raw dump','raw evidence','raw_evidence','call_address','branch target','call target','ghidra_entry','ghidra_name','source_line_text','code.wad','gamewad.obj','secret','private key','credential','asset','raw binary','source patch','address','symbol evidence','copyright')
UPSTREAM='docs/reverse/generated/re535-ghidra-second-window-next-candidate-selection-handoff.csv'
PREFIX='re536-ghidra-second-window-rank-60-narrow-export'
UPFIELDS=('story_id','topic','upstream_handoff','closed_candidate_id','selected_rank','selected_candidate_id','selected_bridge_class','source_symbol_context_count','safe_context_status','ready_to_reopen_domain_count','source_patch_authorized_count','selected_domain','selected_pivot','next_ticket','next_topic','metadata_work_readiness','code_change_readiness','stop_condition')
FIELDS=('story_id','topic','upstream_handoff','selected_candidate_id','selected_rank','selected_subcluster','source_symbol_context_count','bridge_class','safe_context_status','candidate_level_proof_count','ready_to_reopen_domain_count','source_patch_authorized_count','selected_domain','selected_pivot','next_ticket','next_topic','metadata_work_readiness','code_change_readiness','stop_condition')

def build(repo):
    with (Path(repo)/UPSTREAM).open(encoding='utf-8',newline='') as handle:
        reader=csv.DictReader(handle)
        if tuple(reader.fieldnames or ())!=UPFIELDS: raise ValueError('handoff schema drift')
        rows=list(reader)
    if len(rows)!=1: raise ValueError('handoff row-count drift')
    expected={'story_id':'RE-535','topic':'ghidra-second-window-next-candidate-selection','upstream_handoff':'RE-534','closed_candidate_id':'b4bbe082dc9e','selected_rank':'60','selected_candidate_id':'7bf1750a8ac1','selected_bridge_class':'mapped-callee-bridge','source_symbol_context_count':'4','safe_context_status':'filtered-metadata-only','ready_to_reopen_domain_count':'0','source_patch_authorized_count':'0','selected_domain':'none','selected_pivot':'none','next_ticket':'RE-536','next_topic':'ghidra-second-window-rank-60-narrow-export','metadata_work_readiness':'ready','code_change_readiness':'blocked','stop_condition':'next ranked metadata candidate selected; source changes remain blocked'}
    if any(rows[0].get(k)!=v for k,v in expected.items()): raise ValueError('handoff drift')
    row=dict(story_id='RE-536',topic='ghidra-second-window-rank-60-narrow-export',upstream_handoff='RE-535',selected_candidate_id='7bf1750a8ac1',selected_rank='60',selected_subcluster='mapped-callee-bridge-readiness-gate',source_symbol_context_count='4',bridge_class='mapped-callee-bridge',safe_context_status='filtered-metadata-only',candidate_level_proof_count='0',ready_to_reopen_domain_count='0',source_patch_authorized_count='0',selected_domain='none',selected_pivot='none',next_ticket='RE-537',next_topic='mapped-callee-bridge-readiness-gate',metadata_work_readiness='ready',code_change_readiness='blocked',stop_condition='narrow rank-60 export requires readiness gate before proof-domain selection')
    validate(row); return row

def validate(row):
    if tuple(row)!=FIELDS: raise ValueError('output schema drift')
    if any(x in '\n'.join(map(str,row.values())).lower() for x in BAD): raise ValueError('forbidden output fragment')
    if (row['code_change_readiness'],row['source_patch_authorized_count'],row['safe_context_status'])!=('blocked','0','filtered-metadata-only'): raise ValueError('output safety drift')

def write(row,repo):
    validate(row); repo=Path(repo); outputs=[]
    for suffix in ('contexts','summary','handoff'):
        path=repo/'docs/reverse/generated'/f'{PREFIX}-{suffix}.csv';path.parent.mkdir(parents=True,exist_ok=True)
        with path.open('w',encoding='utf-8',newline='') as handle:
            writer=csv.DictWriter(handle,fieldnames=FIELDS,lineterminator='\n');writer.writeheader();writer.writerow(row)
        outputs.append(path)
    documents={repo/'docs/reverse/functions/re536-ghidra-second-window-rank-60-narrow-export.md':'# RE-536 rank-60 narrow export\n\nThe selected candidate is filtered metadata only; source and code work remain blocked.\n',repo/'docs/stories/RE-536-ghidra-second-window-rank-60-narrow-export.md':'# RE-536 rank-60 narrow export\n\n## Progress tracker\n\n- [x] RE-535 handoff validated.\n- [x] Rank-60 context narrowed.\n- [x] Filtered metadata-only safety retained.\n- [x] Source and code work remain blocked.\n- [x] RE-537 selected; not executed.\n'}
    for path,text in documents.items(): path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text,encoding='utf-8');outputs.append(path)
    if any(x in path.read_text(encoding='utf-8').lower() for path in outputs for x in BAD): raise ValueError('forbidden written fragment')
    return outputs

if __name__=='__main__':
    ROOT=Path(__file__).resolve().parents[2];write(build(ROOT),ROOT)
