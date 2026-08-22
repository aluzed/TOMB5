#!/usr/bin/env python3
"""Produce the safe, metadata-only RE-439 rank-30 narrow export."""

import csv
from pathlib import Path

UPSTREAM = 'docs/reverse/generated/re438-ghidra-second-window-next-candidate-selection-handoff.csv'
PREFIX = 're439-ghidra-second-window-rank-30-narrow-export'
FORBIDDEN_OUTPUT_FRAGMENTS = (
    '0x', 'fun_', 'sub_', 'word_le_hex', 'payload_offset', 'opcode',
    'machine word', 'raw dump', 'raw_evidence', 'call_address',
    'branch target', 'call target', 'ghidra_entry', 'ghidra_name',
    'source_line_text', 'code.wad', 'gamewad.obj', 'secret', 'asset',
)


def one_row(path):
    with path.open(encoding='utf-8', newline='') as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 1:
        raise ValueError('handoff row-count drift')
    return rows[0]


def build(repo):
    """Validate RE-438 and retain rank 30 for its mandatory readiness gate."""
    handoff = one_row(Path(repo) / UPSTREAM)
    expected = {
        'story_id': 'RE-438',
        'topic': 'ghidra-second-window-next-candidate-selection',
        'upstream_handoff': 'RE-437',
        'closed_candidate_id': '763c9cd0e3f7',
        'selected_rank': '30',
        'selected_candidate_id': '0947c90b8674',
        'selected_bridge_class': 'mapped-caller-heavy',
        'source_symbol_context_count': '8',
        'safe_context_status': 'filtered-metadata-only',
        'ready_to_reopen_domain_count': '0',
        'source_patch_authorized_count': '0',
        'selected_domain': 'none',
        'selected_pivot': 'none',
        'next_ticket': 'RE-439',
        'next_topic': 'ghidra-second-window-rank-30-narrow-export',
        'metadata_work_readiness': 'ready',
        'code_change_readiness': 'blocked',
    }
    for field, value in expected.items():
        if handoff.get(field) != value:
            raise ValueError(f'handoff drift: {field}')
    return {
        'story_id': 'RE-439',
        'topic': 'ghidra-second-window-rank-30-narrow-export',
        'upstream_handoff': 'RE-438',
        'selected_candidate_id': handoff['selected_candidate_id'],
        'selected_rank': handoff['selected_rank'],
        'selected_subcluster': 'mapped-caller-heavy-readiness-gate',
        'source_symbol_context_count': handoff['source_symbol_context_count'],
        'bridge_class': handoff['selected_bridge_class'],
        'safe_context_status': handoff['safe_context_status'],
        'candidate_level_proof_count': '0',
        'ready_to_reopen_domain_count': '0',
        'source_patch_authorized_count': '0',
        'selected_domain': 'none',
        'selected_pivot': 'none',
        'next_ticket': 'RE-440',
        'next_topic': 'mapped-caller-heavy-readiness-gate',
        'metadata_work_readiness': 'ready',
        'code_change_readiness': 'blocked',
        'stop_condition': 'narrow rank-30 export requires readiness gate before proof-domain selection',
    }


def validate_output(result):
    expected_fields = (
        'story_id', 'topic', 'upstream_handoff', 'selected_candidate_id',
        'selected_rank', 'selected_subcluster', 'source_symbol_context_count',
        'bridge_class', 'safe_context_status', 'candidate_level_proof_count',
        'ready_to_reopen_domain_count', 'source_patch_authorized_count',
        'selected_domain', 'selected_pivot', 'next_ticket', 'next_topic',
        'metadata_work_readiness', 'code_change_readiness', 'stop_condition',
    )
    if tuple(result) != expected_fields:
        raise ValueError('output schema drift')
    text = '\n'.join(str(value).lower() for value in result.values())
    if any(fragment in text for fragment in FORBIDDEN_OUTPUT_FRAGMENTS):
        raise ValueError('forbidden output fragment')
    identity = {
        'story_id': 'RE-439',
        'topic': 'ghidra-second-window-rank-30-narrow-export',
        'upstream_handoff': 'RE-438',
        'selected_candidate_id': '0947c90b8674',
        'selected_rank': '30',
        'selected_subcluster': 'mapped-caller-heavy-readiness-gate',
        'next_ticket': 'RE-440',
        'next_topic': 'mapped-caller-heavy-readiness-gate',
        'metadata_work_readiness': 'ready',
    }
    if any(result.get(field) != value for field, value in identity.items()):
        raise ValueError('output identity drift')
    safety = {
        'safe_context_status': 'filtered-metadata-only',
        'candidate_level_proof_count': '0',
        'ready_to_reopen_domain_count': '0',
        'source_patch_authorized_count': '0',
        'selected_domain': 'none',
        'selected_pivot': 'none',
        'code_change_readiness': 'blocked',
    }
    if any(result.get(field) != value for field, value in safety.items()):
        raise ValueError('output safety drift')


def write(result, repo):
    """Write deterministic metadata-only CSV artifacts and a progress tracker."""
    validate_output(result)
    repo = Path(repo)
    outputs = []
    for suffix in ('contexts', 'summary', 'handoff'):
        path = repo / f'docs/reverse/generated/{PREFIX}-{suffix}.csv'
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('w', newline='', encoding='utf-8') as handle:
            writer = csv.DictWriter(handle, fieldnames=result.keys(), lineterminator='\n')
            writer.writeheader()
            writer.writerow(result)
        outputs.append(path)
    documents = {
        'docs/reverse/functions/re439-ghidra-second-window-rank-30-narrow-export.md': (
            '# RE-439 rank-30 narrow export\n\n'
            'The selected candidate is retained as filtered metadata only; source and code work remain blocked.\n'
        ),
        'docs/stories/RE-439-ghidra-second-window-rank-30-narrow-export.md': (
            '# RE-439 rank-30 narrow export\n\n'
            '## Progress tracker\n\n'
            '- [x] RE-438 handoff validated.\n'
            '- [x] Rank-30 context narrowed.\n'
            '- [x] Filtered metadata-only safety retained.\n'
            '- [x] Source and code work remain blocked.\n'
            '- [x] RE-440 selected.\n'
        ),
    }
    for relative, text in documents.items():
        path = repo / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')
        outputs.append(path)
    for path in outputs:
        text = path.read_text(encoding='utf-8').lower()
        if any(fragment in text for fragment in FORBIDDEN_OUTPUT_FRAGMENTS):
            raise ValueError('forbidden written fragment')
    return outputs


if __name__ == '__main__':
    repository = Path(__file__).resolve().parents[2]
    write(build(repository), repository)
