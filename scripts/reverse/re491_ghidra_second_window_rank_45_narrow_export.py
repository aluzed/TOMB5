"""Produce the fail-closed, metadata-only RE-491 rank-45 narrow export."""
import csv
from pathlib import Path

FORBIDDEN_OUTPUT_FRAGMENTS=('0x','fun_','sub_','word_le_hex','payload_offset','opcode','machine word','raw dump','raw evidence','raw_evidence','call_address','branch target','call target','ghidra_entry','ghidra_name','source_line_text','code.wad','gamewad.obj','secret','private key','credential','asset','raw binary','source patch','address','symbol evidence','copyright')
UPSTREAM='docs/reverse/generated/re490-ghidra-second-window-next-candidate-selection-handoff.csv'
PREFIX='re491-ghidra-second-window-rank-45-narrow-export'
UPSTREAM_FIELDS=('story_id','topic','upstream_handoff','closed_candidate_id','selected_rank','selected_candidate_id','selected_bridge_class','source_symbol_context_count','safe_context_status','ready_to_reopen_domain_count','source_patch_authorized_count','selected_domain','selected_pivot','next_ticket','next_topic','metadata_work_readiness','code_change_readiness','stop_condition')
FIELDS=('story_id','topic','upstream_handoff','selected_candidate_id','selected_rank','selected_subcluster','source_symbol_context_count','bridge_class','safe_context_status','candidate_level_proof_count','ready_to_reopen_domain_count','source_patch_authorized_count','selected_domain','selected_pivot','next_ticket','next_topic','metadata_work_readiness','code_change_readiness','stop_condition')
TICKET='RE-491';TOPIC='ghidra-second-window-rank-45-narrow-export';NEXT='RE-492';NEXT_TOPIC='mapped-caller-bridge-readiness-gate';CANDIDATE='3eb366db63dd';RANK='45';BRIDGE='mapped-caller-bridge';CONTEXTS='8';STOP='narrow rank-45 export requires readiness gate before proof-domain selection'

def read_upstream(repo):
    with (Path(repo)/UPSTREAM).open(encoding='utf-8',newline='') as handle:
        reader=csv.DictReader(handle)
        if tuple(reader.fieldnames or ())!=UPSTREAM_FIELDS:raise ValueError('handoff schema drift')
        rows=list(reader)
    if len(rows)!=1:raise ValueError('handoff row-count drift')
    row=rows[0]
    expected={'story_id':'RE-490','topic':'ghidra-second-window-next-candidate-selection','upstream_handoff':'RE-489','closed_candidate_id':'967dd5c009c5','selected_rank':RANK,'selected_candidate_id':CANDIDATE,'selected_bridge_class':BRIDGE,'source_symbol_context_count':CONTEXTS,'safe_context_status':'filtered-metadata-only','ready_to_reopen_domain_count':'0','source_patch_authorized_count':'0','selected_domain':'none','selected_pivot':'none','next_ticket':TICKET,'next_topic':TOPIC,'metadata_work_readiness':'ready','code_change_readiness':'blocked','stop_condition':'next ranked metadata candidate selected; source changes remain blocked'}
    for field,value in expected.items():
        if row.get(field)!=value:raise ValueError(f'handoff drift: {field}')
    return row

def build(repo):
    row=read_upstream(repo)
    result=dict(story_id=TICKET,topic=TOPIC,upstream_handoff='RE-490',selected_candidate_id=row['selected_candidate_id'],selected_rank=row['selected_rank'],selected_subcluster=NEXT_TOPIC,source_symbol_context_count=row['source_symbol_context_count'],bridge_class=row['selected_bridge_class'],safe_context_status='filtered-metadata-only',candidate_level_proof_count='0',ready_to_reopen_domain_count='0',source_patch_authorized_count='0',selected_domain='none',selected_pivot='none',next_ticket=NEXT,next_topic=NEXT_TOPIC,metadata_work_readiness='ready',code_change_readiness='blocked',stop_condition=STOP)
    validate_output(result);return result

def validate_output(result):
    if tuple(result)!=FIELDS:raise ValueError('output schema drift')
    expected={'story_id':TICKET,'topic':TOPIC,'upstream_handoff':'RE-490','selected_candidate_id':CANDIDATE,'selected_rank':RANK,'selected_subcluster':NEXT_TOPIC,'source_symbol_context_count':CONTEXTS,'bridge_class':BRIDGE,'safe_context_status':'filtered-metadata-only','candidate_level_proof_count':'0','ready_to_reopen_domain_count':'0','source_patch_authorized_count':'0','selected_domain':'none','selected_pivot':'none','next_ticket':NEXT,'next_topic':NEXT_TOPIC,'metadata_work_readiness':'ready','code_change_readiness':'blocked','stop_condition':STOP}
    for field,value in expected.items():
        if result.get(field)!=value:raise ValueError(f'output safety drift: {field}')
    if any(fragment in '\n'.join(map(str,result.values())).lower() for fragment in FORBIDDEN_OUTPUT_FRAGMENTS):raise ValueError('forbidden output fragment')

def write(result,repo):
    validate_output(result);repo=Path(repo);paths=[]
    for suffix in ('contexts','summary','handoff'):
        path=repo/'docs/reverse/generated'/f'{PREFIX}-{suffix}.csv';path.parent.mkdir(parents=True,exist_ok=True)
        with path.open('w',encoding='utf-8',newline='') as handle:writer=csv.DictWriter(handle,fieldnames=FIELDS,lineterminator='\n');writer.writeheader();writer.writerow(result)
        paths.append(path)
    docs={repo/'docs/reverse/functions/re491-ghidra-second-window-rank-45-narrow-export.md':'# RE-491 rank-45 narrow export\n\nThe selected candidate is filtered metadata only; source and code work remain blocked.\n',repo/'docs/stories/RE-491-ghidra-second-window-rank-45-narrow-export.md':'# RE-491 rank-45 narrow export\n\n## Progress tracker\n\n- [x] RE-490 handoff validated.\n- [x] Rank-45 context narrowed.\n- [x] Filtered metadata-only safety retained.\n- [x] Source and code work remain blocked.\n- [x] RE-492 selected; not executed.\n'}
    for path,text in docs.items():path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text,encoding='utf-8');paths.append(path)
    for path in paths:
        if any(fragment in path.read_text(encoding='utf-8').lower() for fragment in FORBIDDEN_OUTPUT_FRAGMENTS):raise ValueError('forbidden written fragment')
    return paths
if __name__=='__main__':
 ROOT=Path(__file__).resolve().parents[2];write(build(ROOT),ROOT)
