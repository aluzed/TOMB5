#!/usr/bin/env python3
"""Produce the safe, metadata-only RE-458 rank-34 narrow export."""

import csv
from pathlib import Path

UPSTREAM = 'docs/reverse/generated/re457-ghidra-second-window-next-candidate-selection-handoff.csv'
PREFIX = 're458-ghidra-second-window-rank-34-narrow-export'
FORBIDDEN_OUTPUT_FRAGMENTS = (
    '0x', 'fun_', 'sub_', 'word_le_hex', 'payload_offset', 'opcode',
    'machine word', 'raw dump', 'raw_evidence', 'call_address',
    'branch target', 'call target', 'ghidra_entry', 'ghidra_name',
    'source_line_text', 'code.wad', 'gamewad.obj', 'secret', 'asset',
    'raw binary', 'address', 'symbol evidence', 'copyright',
)
UPSTREAM_FIELDS = (
    'story_id', 'topic', 'upstream_handoff', 'closed_candidate_id',
    'selected_rank', 'selected_candidate_id', 'selected_bridge_class',
    'source_symbol_context_count', 'safe_context_status',
    'ready_to_reopen_domain_count', 'source_patch_authorized_count',
    'selected_domain', 'selected_pivot', 'next_ticket', 'next_topic',
    'metadata_work_readiness', 'code_change_readiness', 'stop_condition',
)
FIELDS = (
    'story_id', 'topic', 'upstream_handoff', 'selected_candidate_id',
    'selected_rank', 'selected_subcluster', 'source_symbol_context_count',
    'bridge_class', 'safe_context_status', 'candidate_level_proof_count',
    'ready_to_reopen_domain_count', 'source_patch_authorized_count',
    'selected_domain', 'selected_pivot', 'next_ticket', 'next_topic',
    'metadata_work_readiness', 'code_change_readiness', 'stop_condition',
)


def one_row(path):
    with path.open(encoding='utf-8', newline='') as handle:
        reader = csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != UPSTREAM_FIELDS:
            raise ValueError('handoff schema drift')
        rows = list(reader)
    if len(rows) != 1:
        raise ValueError('handoff row-count drift')
    return rows[0]


def build(repo):
    """Validate RE-457 and retain rank 34 for its readiness gate."""
    handoff = one_row(Path(repo) / UPSTREAM)
    expected = {
        'story_id': 'RE-457', 'topic': 'ghidra-second-window-next-candidate-selection',
        'upstream_handoff': 'RE-456', 'closed_candidate_id': '8beda0f5763e',
        'selected_rank': '34', 'selected_candidate_id': 'aaf42cb3b10b',
        'selected_bridge_class': 'mapped-caller-bridge', 'source_symbol_context_count': '9',
        'safe_context_status': 'filtered-metadata-only',
        'ready_to_reopen_domain_count': '0', 'source_patch_authorized_count': '0',
        'selected_domain': 'none', 'selected_pivot': 'none', 'next_ticket': 'RE-458',
        'next_topic': 'ghidra-second-window-rank-34-narrow-export',
        'metadata_work_readiness': 'ready', 'code_change_readiness': 'blocked',
    }
    for field, value in expected.items():
        if handoff.get(field) != value:
            raise ValueError(f'handoff drift: {field}')
    return {
        'story_id': 'RE-458', 'topic': 'ghidra-second-window-rank-34-narrow-export',
        'upstream_handoff': 'RE-457', 'selected_candidate_id': handoff['selected_candidate_id'],
        'selected_rank': handoff['selected_rank'],
        'selected_subcluster': 'mapped-caller-bridge-readiness-gate',
        'source_symbol_context_count': handoff['source_symbol_context_count'],
        'bridge_class': handoff['selected_bridge_class'],
        'safe_context_status': handoff['safe_context_status'], 'candidate_level_proof_count': '0',
        'ready_to_reopen_domain_count': '0', 'source_patch_authorized_count': '0',
        'selected_domain': 'none', 'selected_pivot': 'none', 'next_ticket': 'RE-459',
        'next_topic': 'mapped-caller-bridge-readiness-gate', 'metadata_work_readiness': 'ready',
        'code_change_readiness': 'blocked',
        'stop_condition': 'narrow rank-34 export requires readiness gate before proof-domain selection',
    }


def validate_output(result):
    if tuple(result) != FIELDS:
        raise ValueError('output schema drift')
    text = '\n'.join(str(value).lower() for value in result.values())
    if any(fragment in text for fragment in FORBIDDEN_OUTPUT_FRAGMENTS):
        raise ValueError('forbidden output fragment')
    identity = {
        'story_id': 'RE-458', 'topic': 'ghidra-second-window-rank-34-narrow-export',
        'upstream_handoff': 'RE-457', 'selected_candidate_id': 'aaf42cb3b10b',
        'selected_rank': '34', 'selected_subcluster': 'mapped-caller-bridge-readiness-gate',
        'next_ticket': 'RE-459', 'next_topic': 'mapped-caller-bridge-readiness-gate',
        'metadata_work_readiness': 'ready',
    }
    if any(result.get(field) != value for field, value in identity.items()):
        raise ValueError('output identity drift')
    safety = {'safe_context_status': 'filtered-metadata-only', 'candidate_level_proof_count': '0',
              'ready_to_reopen_domain_count': '0', 'source_patch_authorized_count': '0',
              'selected_domain': 'none', 'selected_pivot': 'none', 'code_change_readiness': 'blocked'}
    if any(result.get(field) != value for field, value in safety.items()):
        raise ValueError('output safety drift')


def write(result, repo):
    validate_output(result)
    repo = Path(repo); outputs = []
    for suffix in ('contexts', 'summary', 'handoff'):
        path = repo / f'docs/reverse/generated/{PREFIX}-{suffix}.csv'; path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('w', newline='', encoding='utf-8') as handle:
            writer = csv.DictWriter(handle, fieldnames=result.keys(), lineterminator='\n'); writer.writeheader(); writer.writerow(result)
        outputs.append(path)
    documents = {
        'docs/reverse/functions/re458-ghidra-second-window-rank-34-narrow-export.md': '# RE-458 rank-34 narrow export\n\nThe selected candidate is filtered metadata only; source and code work remain blocked.\n',
        'docs/stories/RE-458-ghidra-second-window-rank-34-narrow-export.md': '# RE-458 rank-34 narrow export\n\n## Progress tracker\n\n- [x] RE-457 handoff validated.\n- [x] Rank-34 context narrowed.\n- [x] Filtered metadata-only safety retained.\n- [x] Source and code work remain blocked.\n- [x] RE-459 selected; not executed.\n',
    }
    for relative, text in documents.items():
        path = repo / relative; path.parent.mkdir(parents=True, exist_ok=True); path.write_text(text, encoding='utf-8'); outputs.append(path)
    for path in outputs:
        if any(fragment in path.read_text(encoding='utf-8').lower() for fragment in FORBIDDEN_OUTPUT_FRAGMENTS):
            raise ValueError('forbidden written fragment')
    return outputs


if __name__ == '__main__':
    repository = Path(__file__).resolve().parents[2]
    write(build(repository), repository)
