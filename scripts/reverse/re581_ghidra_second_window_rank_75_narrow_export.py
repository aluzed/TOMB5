"""Produce the fail-closed, metadata-only RE-581 rank-75 narrow export."""
import csv
from pathlib import Path

BAD = ('0x', 'fun_', 'sub_', 'word_le_hex', 'payload_offset', 'opcode', 'machine word', 'raw dump', 'raw evidence', 'raw_evidence', 'call_address', 'branch target', 'call target', 'ghidra_entry', 'ghidra_name', 'source_line_text', 'code.wad', 'gamewad.obj', 'secret', 'private key', 'credential', 'asset', 'raw binary', 'source patch', 'address', 'symbol evidence', 'copyright')
UPSTREAM = 'docs/reverse/generated/re580-ghidra-second-window-next-candidate-selection-handoff.csv'
PREFIX = 're581-ghidra-second-window-rank-75-narrow-export'
UPFIELDS = ('story_id', 'topic', 'upstream_handoff', 'closed_candidate_id', 'selected_rank', 'selected_candidate_id', 'selected_bridge_class', 'source_symbol_context_count', 'safe_context_status', 'ready_to_reopen_domain_count', 'source_patch_authorized_count', 'selected_domain', 'selected_pivot', 'next_ticket', 'next_topic', 'metadata_work_readiness', 'code_change_readiness', 'stop_condition')
FIELDS = ('story_id', 'topic', 'upstream_handoff', 'selected_candidate_id', 'selected_rank', 'selected_subcluster', 'source_symbol_context_count', 'bridge_class', 'safe_context_status', 'candidate_level_proof_count', 'ready_to_reopen_domain_count', 'source_patch_authorized_count', 'selected_domain', 'selected_pivot', 'next_ticket', 'next_topic', 'metadata_work_readiness', 'code_change_readiness', 'stop_condition')


def build(repo):
    with (Path(repo) / UPSTREAM).open(encoding='utf-8', newline='') as handle:
        reader = csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != UPFIELDS:
            raise ValueError('handoff schema drift')
        rows = list(reader)
    expected = {'story_id': 'RE-580', 'topic': 'ghidra-second-window-next-candidate-selection', 'upstream_handoff': 'RE-579', 'closed_candidate_id': '9ded6d1f164d', 'selected_rank': '75', 'selected_candidate_id': '792bbf9b7b74', 'selected_bridge_class': 'mapped-caller-bridge', 'source_symbol_context_count': '6', 'safe_context_status': 'filtered-metadata-only', 'ready_to_reopen_domain_count': '0', 'source_patch_authorized_count': '0', 'selected_domain': 'none', 'selected_pivot': 'none', 'next_ticket': 'RE-581', 'next_topic': 'ghidra-second-window-rank-75-narrow-export', 'metadata_work_readiness': 'ready', 'code_change_readiness': 'blocked', 'stop_condition': 'next ranked metadata candidate selected; source changes remain blocked'}
    if len(rows) != 1 or any(rows[0].get(key) != value for key, value in expected.items()):
        raise ValueError('handoff drift')
    row = dict(story_id='RE-581', topic='ghidra-second-window-rank-75-narrow-export', upstream_handoff='RE-580', selected_candidate_id='792bbf9b7b74', selected_rank='75', selected_subcluster='mapped-caller-bridge-readiness-gate', source_symbol_context_count='6', bridge_class='mapped-caller-bridge', safe_context_status='filtered-metadata-only', candidate_level_proof_count='0', ready_to_reopen_domain_count='0', source_patch_authorized_count='0', selected_domain='none', selected_pivot='none', next_ticket='RE-582', next_topic='mapped-caller-bridge-readiness-gate', metadata_work_readiness='ready', code_change_readiness='blocked', stop_condition='narrow rank-75 export requires readiness gate before proof-domain selection')
    validate(row)
    return row


def validate(row):
    if tuple(row) != FIELDS: raise ValueError('output schema drift')
    if any(x in '\n'.join(map(str,row.values())).lower() for x in BAD): raise ValueError('forbidden output fragment')
    if (row['code_change_readiness'],row['source_patch_authorized_count'],row['safe_context_status']) != ('blocked','0','filtered-metadata-only'): raise ValueError('output safety drift')


def write(row, repo):
    validate(row); repo=Path(repo); outputs=[]
    for suffix in ('contexts','summary','handoff'):
        p=repo/'docs/reverse/generated'/f'{PREFIX}-{suffix}.csv';p.parent.mkdir(parents=True,exist_ok=True)
        with p.open('w',encoding='utf-8',newline='') as h:
            w=csv.DictWriter(h,fieldnames=FIELDS,lineterminator='\n');w.writeheader();w.writerow(row)
        outputs.append(p)
    documents={repo/'docs/reverse/functions/re581-ghidra-second-window-rank-75-narrow-export.md':'# RE-581 rank-75 narrow export\n\nThe selected candidate is filtered metadata only; source and code work remain blocked.\n',repo/'docs/stories/RE-581-ghidra-second-window-rank-75-narrow-export.md':'# RE-581 rank-75 narrow export\n\n## Progress tracker\n\n- [x] RE-580 handoff validated.\n- [x] Rank-75 context narrowed.\n- [x] Filtered metadata-only safety retained.\n- [x] Source and code work remain blocked.\n- [x] RE-582 selected; not executed.\n'}
    for p,text in documents.items(): p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8');outputs.append(p)
    if any(x in p.read_text(encoding='utf-8').lower() for p in outputs for x in BAD): raise ValueError('forbidden written fragment')
    return outputs

if __name__ == '__main__':
    ROOT=Path(__file__).resolve().parents[2];write(build(ROOT),ROOT)
