"""Produce the fail-closed, metadata-only RE-588 readiness gate."""
import csv
from pathlib import Path

BAD = (
    '0x', 'fun_', 'sub_', 'word_le_hex', 'payload_offset', 'opcode',
    'machine word', 'raw dump', 'raw evidence', 'raw_evidence',
    'call_address', 'branch target', 'call target', 'ghidra_entry',
    'ghidra_name', 'source_line_text', 'code.wad', 'gamewad.obj', 'secret',
    'private key', 'credential', 'asset', 'raw binary', 'source patch',
    'address', 'symbol evidence', 'copyright',
)
UPSTREAM = 'docs/reverse/generated/re587-ghidra-second-window-rank-77-narrow-export-handoff.csv'
PREFIX = 're588-mapped-caller-callee-bridge-readiness-gate'
UPFIELDS = (
    'story_id', 'topic', 'upstream_handoff', 'selected_candidate_id',
    'selected_rank', 'selected_subcluster', 'source_symbol_context_count',
    'bridge_class', 'safe_context_status', 'candidate_level_proof_count',
    'ready_to_reopen_domain_count', 'source_patch_authorized_count',
    'selected_domain', 'selected_pivot', 'next_ticket', 'next_topic',
    'metadata_work_readiness', 'code_change_readiness', 'stop_condition',
)
FIELDS = (
    'story_id', 'topic', 'upstream_handoff', 'selected_candidate_id',
    'selected_rank', 'selected_subcluster', 'source_symbol_context_count',
    'bridge_class', 'safe_context_status', 'source_backed_callsite_count',
    'candidate_level_proof_count', 'repository_symbol_direct_proof_count',
    'ready_to_reopen_domain_count', 'source_patch_authorized_count',
    'selected_domain', 'selected_pivot', 'next_ticket', 'next_topic',
    'metadata_work_readiness', 'code_change_readiness', 'stop_condition',
)
EXPECTED = {
    'story_id': 'RE-587',
    'topic': 'ghidra-second-window-rank-77-narrow-export',
    'upstream_handoff': 'RE-586',
    'selected_candidate_id': '0e8763dda0df',
    'selected_rank': '77',
    'selected_subcluster': 'mapped-caller-callee-bridge-readiness-gate',
    'source_symbol_context_count': '4',
    'bridge_class': 'mapped-caller-callee-bridge',
    'safe_context_status': 'filtered-metadata-only',
    'candidate_level_proof_count': '0',
    'ready_to_reopen_domain_count': '0',
    'source_patch_authorized_count': '0',
    'selected_domain': 'none',
    'selected_pivot': 'none',
    'next_ticket': 'RE-588',
    'next_topic': 'mapped-caller-callee-bridge-readiness-gate',
    'metadata_work_readiness': 'ready',
    'code_change_readiness': 'blocked',
    'stop_condition': 'narrow rank-77 export requires readiness gate before proof-domain selection',
}


def build(repo):
    with (Path(repo) / UPSTREAM).open(encoding='utf-8', newline='') as handle:
        reader = csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != UPFIELDS:
            raise ValueError('handoff schema drift')
        rows = list(reader)
    if len(rows) != 1 or any(rows[0].get(key) != value for key, value in EXPECTED.items()):
        raise ValueError('handoff drift')
    row = dict(
        story_id='RE-588',
        topic='mapped-caller-callee-bridge-readiness-gate',
        upstream_handoff='RE-587',
        selected_candidate_id='0e8763dda0df',
        selected_rank='77',
        selected_subcluster='mapped-caller-callee-bridge-readiness-gate',
        source_symbol_context_count='4',
        bridge_class='mapped-caller-callee-bridge',
        safe_context_status='filtered-metadata-only',
        source_backed_callsite_count='0',
        candidate_level_proof_count='0',
        repository_symbol_direct_proof_count='0',
        ready_to_reopen_domain_count='0',
        source_patch_authorized_count='0',
        selected_domain='none',
        selected_pivot='none',
        next_ticket='RE-589',
        next_topic='ghidra-second-window-next-candidate-selection',
        metadata_work_readiness='ready',
        code_change_readiness='blocked',
        stop_condition='metadata-only safety gate denies proof-domain selection and production changes',
    )
    validate(row)
    return row


def validate(row):
    if tuple(row) != FIELDS:
        raise ValueError('output schema drift')
    text = '\n'.join(map(str, row.values())).lower()
    if any(fragment in text for fragment in BAD):
        raise ValueError('forbidden output fragment')
    if (row['code_change_readiness'], row['source_patch_authorized_count'],
            row['safe_context_status']) != ('blocked', '0', 'filtered-metadata-only'):
        raise ValueError('output safety drift')


def write(row, repo):
    validate(row)
    repo = Path(repo)
    outputs = []
    for suffix in ('gate', 'summary', 'handoff'):
        path = repo / 'docs/reverse/generated' / f'{PREFIX}-{suffix}.csv'
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('w', encoding='utf-8', newline='') as handle:
            writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator='\n')
            writer.writeheader()
            writer.writerow(row)
        outputs.append(path)
    documents = {
        repo / 'docs/reverse/functions/re588-mapped-caller-callee-bridge-readiness-gate.md': (
            '# RE-588 readiness gate\n\n'
            'Filtered metadata-only decision; production and code work remain blocked.\n'
        ),
        repo / 'docs/stories/RE-588-mapped-caller-callee-bridge-readiness-gate.md': (
            '# RE-588 readiness gate\n\n## Progress tracker\n\n'
            '- [x] RE-587 handoff validated.\n'
            '- [x] Filtered metadata decision recorded.\n'
            '- [x] Safety guard retained.\n'
            '- [x] Production and code work remain blocked.\n'
            '- [x] RE-589 selected; not executed.\n'
        ),
    }
    for path, text in documents.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')
        outputs.append(path)
    for path in outputs:
        text = path.read_text(encoding='utf-8').lower()
        if any(fragment in text for fragment in BAD):
            raise ValueError('forbidden written fragment')
    return outputs


if __name__ == '__main__':
    ROOT = Path(__file__).resolve().parents[2]
    write(build(ROOT), ROOT)
