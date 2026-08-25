"""Fail-closed metadata-only selection for RE-490."""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.reverse import re309_ghidra_unmapped_bridge_candidates as candidates

FORBIDDEN_OUTPUT_FRAGMENTS = ('0x', 'fun_', 'sub_', 'word_le_hex', 'payload_offset', 'opcode', 'machine word', 'raw dump', 'raw evidence', 'raw_evidence', 'call_address', 'branch target', 'call target', 'ghidra_entry', 'ghidra_name', 'source_line_text', 'code.wad', 'gamewad.obj', 'secret', 'private key', 'credential', 'asset', 'raw binary', 'source patch', 'address', 'symbol evidence', 'copyright')
FIELDS = ('story_id', 'topic', 'upstream_handoff', 'closed_candidate_id', 'selected_rank', 'selected_candidate_id', 'selected_bridge_class', 'source_symbol_context_count', 'safe_context_status', 'ready_to_reopen_domain_count', 'source_patch_authorized_count', 'selected_domain', 'selected_pivot', 'next_ticket', 'next_topic', 'metadata_work_readiness', 'code_change_readiness', 'stop_condition')
UPSTREAM_FIELDS = ('story_id', 'topic', 'upstream_handoff', 'selected_candidate_id', 'selected_rank', 'selected_subcluster', 'source_symbol_context_count', 'bridge_class', 'safe_context_status', 'source_backed_callsite_count', 'candidate_level_proof_count', 'repository_symbol_direct_proof_count', 'ready_to_reopen_domain_count', 'source_patch_authorized_count', 'selected_domain', 'selected_pivot', 'next_ticket', 'next_topic', 'metadata_work_readiness', 'code_change_readiness', 'stop_condition')
TICKET='RE-490'; TOPIC='ghidra-second-window-next-candidate-selection'; UPSTREAM='RE-489'; CLOSED='967dd5c009c5'; RANK='45'; CANDIDATE='3eb366db63dd'; BRIDGE='mapped-caller-bridge'; CONTEXTS='8'; NEXT='RE-491'; NEXT_TOPIC='ghidra-second-window-rank-45-narrow-export'
STOP='next ranked metadata candidate selected; source changes remain blocked'

def ranked_candidate(repo, rank):
    old=candidates.TOP_LIMIT
    try:
        candidates.TOP_LIMIT=55; rows,_=candidates.build_bridge_candidates(Path(repo))
    finally:
        candidates.TOP_LIMIT=old
    return next((row for row in rows if row.rank==int(rank)), None)

def read_upstream(repo):
    path=Path(repo)/'docs/reverse/generated/re489-mapped-caller-callee-bridge-readiness-gate-handoff.csv'
    with path.open(encoding='utf-8',newline='') as handle:
        reader=csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != UPSTREAM_FIELDS: raise ValueError('handoff schema drift')
        rows=list(reader)
    if len(rows)!=1: raise ValueError('handoff row-count drift')
    row=rows[0]
    expected={'story_id':UPSTREAM,'topic':'mapped-caller-callee-bridge-readiness-gate','upstream_handoff':'RE-488','selected_candidate_id':CLOSED,'selected_rank':'44','selected_subcluster':'mapped-caller-callee-bridge-readiness-gate','source_symbol_context_count':'8','bridge_class':'mapped-caller-callee-bridge','safe_context_status':'filtered-metadata-only','source_backed_callsite_count':'0','candidate_level_proof_count':'0','repository_symbol_direct_proof_count':'0','ready_to_reopen_domain_count':'0','source_patch_authorized_count':'0','selected_domain':'none','selected_pivot':'none','next_ticket':TICKET,'next_topic':TOPIC,'metadata_work_readiness':'ready','code_change_readiness':'blocked','stop_condition':'metadata-only safety gate denies proof-domain selection and source changes'}
    for field,value in expected.items():
        if row.get(field)!=value: raise ValueError(f'handoff drift: {field}')
    return row

def build(repo):
    row=read_upstream(repo); candidate=ranked_candidate(repo,RANK)
    if candidate is None or (candidate.candidate_id,candidate.bridge_class,candidate.source_context_count)!=(CANDIDATE,BRIDGE,int(CONTEXTS)): raise ValueError('ranked candidate drift')
    if candidate.ready_to_reopen_domain!='no' or candidate.source_patch_authorized!='no': raise ValueError('candidate readiness drift')
    result=dict(story_id=TICKET,topic=TOPIC,upstream_handoff=UPSTREAM,closed_candidate_id=row['selected_candidate_id'],selected_rank=RANK,selected_candidate_id=CANDIDATE,selected_bridge_class=BRIDGE,source_symbol_context_count=CONTEXTS,safe_context_status='filtered-metadata-only',ready_to_reopen_domain_count='0',source_patch_authorized_count='0',selected_domain='none',selected_pivot='none',next_ticket=NEXT,next_topic=NEXT_TOPIC,metadata_work_readiness='ready',code_change_readiness='blocked',stop_condition=STOP)
    validate_output(result); return result

def validate_output(result):
    if tuple(result)!=FIELDS: raise ValueError('output schema drift')
    expected={'story_id':TICKET,'topic':TOPIC,'upstream_handoff':UPSTREAM,'closed_candidate_id':CLOSED,'selected_rank':RANK,'selected_candidate_id':CANDIDATE,'selected_bridge_class':BRIDGE,'source_symbol_context_count':CONTEXTS,'safe_context_status':'filtered-metadata-only','ready_to_reopen_domain_count':'0','source_patch_authorized_count':'0','selected_domain':'none','selected_pivot':'none','next_ticket':NEXT,'next_topic':NEXT_TOPIC,'metadata_work_readiness':'ready','code_change_readiness':'blocked','stop_condition':STOP}
    for field,value in expected.items():
        if result.get(field)!=value: raise ValueError(f'output safety drift: {field}')
    if any(fragment in '\n'.join(map(str,result.values())).lower() for fragment in FORBIDDEN_OUTPUT_FRAGMENTS): raise ValueError('forbidden output fragment')

def write(result,repo):
    validate_output(result); repo=Path(repo); paths=[]; prefix='re490-ghidra-second-window-next-candidate-selection'
    for suffix in ('candidates','summary','handoff'):
        path=repo/'docs/reverse/generated'/f'{prefix}-{suffix}.csv'; path.parent.mkdir(parents=True,exist_ok=True)
        with path.open('w',encoding='utf-8',newline='') as handle:
            writer=csv.DictWriter(handle,fieldnames=FIELDS,lineterminator='\n'); writer.writeheader(); writer.writerow(result)
        paths.append(path)
    docs={repo/'docs/reverse/functions/re490-ghidra-second-window-next-candidate-selection.md':'# RE-490 ghidra-second-window-next-candidate-selection\n\nFiltered metadata-only decision; source and code work remain blocked.\n',repo/'docs/stories/RE-490-ghidra-second-window-next-candidate-selection.md':'# RE-490 ghidra-second-window-next-candidate-selection\n\n## Progress tracker\n\n- [x] RE-489 handoff validated.\n- [x] Filtered metadata decision recorded.\n- [x] Safety guard retained.\n- [x] Source and code work remain blocked.\n- [x] RE-491 selected; not executed.\n'}
    for path,text in docs.items(): path.parent.mkdir(parents=True,exist_ok=True); path.write_text(text,encoding='utf-8'); paths.append(path)
    for path in paths:
        if any(fragment in path.read_text(encoding='utf-8').lower() for fragment in FORBIDDEN_OUTPUT_FRAGMENTS): raise ValueError('forbidden written fragment')
    return paths

if __name__=='__main__':
    ROOT=Path(__file__).resolve().parents[2]; write(build(ROOT),ROOT)
