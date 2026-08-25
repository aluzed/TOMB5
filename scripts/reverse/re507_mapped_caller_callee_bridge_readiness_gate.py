"""Fail-closed metadata-only readiness gate for RE-507."""
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
FIELDS = (
    'story_id', 'topic', 'upstream_handoff', 'selected_candidate_id',
    'selected_rank', 'selected_subcluster', 'source_symbol_context_count',
    'bridge_class', 'safe_context_status', 'source_backed_callsite_count',
    'candidate_level_proof_count', 'repository_symbol_direct_proof_count',
    'ready_to_reopen_domain_count', 'source_patch_authorized_count',
    'selected_domain', 'selected_pivot', 'next_ticket', 'next_topic',
    'metadata_work_readiness', 'code_change_readiness', 'stop_condition',
)
UPFIELDS = (
    'story_id', 'topic', 'upstream_handoff', 'selected_candidate_id',
    'selected_rank', 'selected_subcluster', 'source_symbol_context_count',
    'bridge_class', 'safe_context_status', 'candidate_level_proof_count',
    'ready_to_reopen_domain_count', 'source_patch_authorized_count',
    'selected_domain', 'selected_pivot', 'next_ticket', 'next_topic',
    'metadata_work_readiness', 'code_change_readiness', 'stop_condition',
)
TICKET = 'RE-507'
TOPIC = 'mapped-caller-callee-bridge-readiness-gate'
UPSTREAM = 'RE-506'
CANDIDATE = 'bdb92ce23200'
RANK = '50'
CONTEXTS = '7'
BRIDGE = 'mapped-caller-callee-bridge'
NEXT = 'RE-508'
NEXT_TOPIC = 'ghidra-second-window-next-candidate-selection'
STOP = 'metadata-only safety gate denies proof-domain selection and source changes'
UPSTREAM_PATH = 'docs/reverse/generated/re506-ghidra-second-window-rank-50-narrow-export-handoff.csv'


def read_upstream(repo):
    with (Path(repo) / UPSTREAM_PATH).open(encoding='utf-8', newline='') as handle:
        reader = csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != UPFIELDS:
            raise ValueError('handoff schema drift')
        rows = list(reader)
    if len(rows) != 1:
        raise ValueError('handoff row-count drift')
    row = rows[0]
    expected = {
        'story_id': UPSTREAM,
        'topic': 'ghidra-second-window-rank-50-narrow-export',
        'upstream_handoff': 'RE-505',
        'selected_candidate_id': CANDIDATE,
        'selected_rank': RANK,
        'selected_subcluster': TOPIC,
        'source_symbol_context_count': CONTEXTS,
        'bridge_class': BRIDGE,
        'safe_context_status': 'filtered-metadata-only',
        'candidate_level_proof_count': '0',
        'ready_to_reopen_domain_count': '0',
        'source_patch_authorized_count': '0',
        'selected_domain': 'none',
        'selected_pivot': 'none',
        'next_ticket': TICKET,
        'next_topic': TOPIC,
        'metadata_work_readiness': 'ready',
        'code_change_readiness': 'blocked',
        'stop_condition': 'narrow rank-50 export requires readiness gate before proof-domain selection',
    }
    for key, value in expected.items():
        if row.get(key) != value:
            raise ValueError(f'handoff drift: {key}')
    return row


def build(repo):
    read_upstream(repo)
    row = dict(
        story_id=TICKET, topic=TOPIC, upstream_handoff=UPSTREAM,
        selected_candidate_id=CANDIDATE, selected_rank=RANK,
        selected_subcluster=TOPIC, source_symbol_context_count=CONTEXTS,
        bridge_class=BRIDGE, safe_context_status='filtered-metadata-only',
        source_backed_callsite_count='0', candidate_level_proof_count='0',
        repository_symbol_direct_proof_count='0', ready_to_reopen_domain_count='0',
        source_patch_authorized_count='0', selected_domain='none',
        selected_pivot='none', next_ticket=NEXT, next_topic=NEXT_TOPIC,
        metadata_work_readiness='ready', code_change_readiness='blocked',
        stop_condition=STOP,
    )
    validate(row)
    return row


def validate(row):
    if tuple(row) != FIELDS:
        raise ValueError('output schema drift')
    if any(fragment in '\n'.join(map(str, row.values())).lower() for fragment in BAD):
        raise ValueError('forbidden output fragment')
    expected = {
        'story_id': TICKET, 'topic': TOPIC, 'upstream_handoff': UPSTREAM,
        'selected_candidate_id': CANDIDATE, 'selected_rank': RANK,
        'selected_subcluster': TOPIC, 'source_symbol_context_count': CONTEXTS,
        'bridge_class': BRIDGE, 'safe_context_status': 'filtered-metadata-only',
        'source_backed_callsite_count': '0', 'candidate_level_proof_count': '0',
        'repository_symbol_direct_proof_count': '0', 'ready_to_reopen_domain_count': '0',
        'source_patch_authorized_count': '0', 'selected_domain': 'none',
        'selected_pivot': 'none', 'next_ticket': NEXT, 'next_topic': NEXT_TOPIC,
        'metadata_work_readiness': 'ready', 'code_change_readiness': 'blocked',
        'stop_condition': STOP,
    }
    for key, value in expected.items():
        if row.get(key) != value:
            raise ValueError(f'output safety drift: {key}')


def write(row, repo):
    validate(row)
    repo = Path(repo)
    outputs = []
    prefix = 're507-mapped-caller-callee-bridge-readiness-gate'
    for suffix in ('gate', 'summary', 'handoff'):
        path = repo / 'docs/reverse/generated' / f'{prefix}-{suffix}.csv'
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('w', encoding='utf-8', newline='') as handle:
            writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator='\n')
            writer.writeheader()
            writer.writerow(row)
        outputs.append(path)
    documents = {
        repo / 'docs/reverse/functions/re507-mapped-caller-callee-bridge-readiness-gate.md': (
            '# RE-507 readiness gate\n\n'
            'Filtered metadata-only decision; source and code work remain blocked.\n'
        ),
        repo / 'docs/stories/RE-507-mapped-caller-callee-bridge-readiness-gate.md': (
            '# RE-507 readiness gate\n\n## Progress tracker\n\n'
            '- [x] RE-506 handoff validated.\n'
            '- [x] Filtered metadata decision recorded.\n'
            '- [x] Safety guard retained.\n'
            '- [x] Source and code work remain blocked.\n'
            '- [x] RE-508 selected; not executed.\n'
        ),
    }
    for path, text in documents.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')
        outputs.append(path)
    for path in outputs:
        if any(fragment in path.read_text(encoding='utf-8').lower() for fragment in BAD):
            raise ValueError('forbidden written fragment')
    return outputs


if __name__ == '__main__':
    ROOT = Path(__file__).resolve().parents[2]
    write(build(ROOT), ROOT)
