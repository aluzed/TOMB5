#!/usr/bin/env python3
"""Select the next safe second-window bridge candidate as metadata only."""

import csv
import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from scripts.reverse import re309_ghidra_unmapped_bridge_candidates as r309

UPSTREAM = 'docs/reverse/generated/re437-runtime-bridge-service-callsite-readiness-gate-handoff.csv'
PREFIX = 're438-ghidra-second-window-next-candidate-selection'
FORBIDDEN_OUTPUT_FRAGMENTS = (
    '0x', 'fun_', 'sub_', 'word_le_hex', 'payload_offset', 'opcode',
    'machine word', 'raw dump', 'raw_evidence', 'call_address',
    'branch target', 'call target', 'ghidra_entry', 'ghidra_name',
    'source_line_text', 'code.wad', 'gamewad.obj', 'secret',
)


def one_row(path):
    with path.open(encoding='utf-8', newline='') as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 1:
        raise ValueError('handoff row-count drift')
    return rows[0]


def ranked_candidate(repo, rank):
    old_limit = r309.TOP_LIMIT
    try:
        r309.TOP_LIMIT = 50
        rows, _ = r309.build_bridge_candidates(repo)
    finally:
        r309.TOP_LIMIT = old_limit
    return next((row for row in rows if row.rank == rank), None)


def build(repo):
    """Validate closure of rank 29 and select rank 30 without source evidence."""
    repo = Path(repo)
    handoff = one_row(repo / UPSTREAM)
    expected = {
        'story_id': 'RE-437',
        'next_ticket': 'RE-438',
        'next_topic': 'ghidra-second-window-next-candidate-selection',
        'selected_candidate_id': '763c9cd0e3f7',
        'selected_rank': '29',
        'selected_subcluster': 'runtime-bridge-service',
        'source_context_function_count': '10',
        'source_backed_callsite_count': '0',
        'candidate_level_proof_count': '0',
        'repository_symbol_direct_proof_count': '0',
        'ready_to_reopen_domain_count': '0',
        'source_patch_authorized_count': '0',
        'selected_domain': 'none',
        'selected_pivot': 'none',
        'metadata_work_readiness': 'ready',
        'code_change_readiness': 'blocked',
    }
    for field, value in expected.items():
        if handoff.get(field) != value:
            raise ValueError(f'handoff drift: {field}')
    candidate = ranked_candidate(repo, 30)
    if candidate is None:
        raise ValueError('rank 30 unavailable')
    if (candidate.candidate_id, candidate.bridge_class, candidate.source_context_count) != (
        '0947c90b8674', 'mapped-caller-heavy', 8,
    ):
        raise ValueError('rank 30 candidate drift')
    if candidate.ready_to_reopen_domain != 'no' or candidate.source_patch_authorized != 'no':
        raise ValueError('rank 30 readiness drift')
    return {
        'story_id': 'RE-438',
        'topic': 'ghidra-second-window-next-candidate-selection',
        'upstream_handoff': 'RE-437',
        'closed_candidate_id': handoff['selected_candidate_id'],
        'selected_rank': str(candidate.rank),
        'selected_candidate_id': candidate.candidate_id,
        'selected_bridge_class': candidate.bridge_class,
        'source_symbol_context_count': str(candidate.source_context_count),
        'safe_context_status': 'filtered-metadata-only',
        'ready_to_reopen_domain_count': '0',
        'source_patch_authorized_count': '0',
        'selected_domain': 'none',
        'selected_pivot': 'none',
        'next_ticket': 'RE-439',
        'next_topic': 'ghidra-second-window-rank-30-narrow-export',
        'metadata_work_readiness': 'ready',
        'code_change_readiness': 'blocked',
        'stop_condition': 'rank 30 selected; source and code work remain blocked pending a narrow metadata gate',
    }


def validate_output(result):
    expected_fields = (
        'story_id', 'topic', 'upstream_handoff', 'closed_candidate_id',
        'selected_rank', 'selected_candidate_id', 'selected_bridge_class',
        'source_symbol_context_count', 'safe_context_status',
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
        'story_id': 'RE-438',
        'topic': 'ghidra-second-window-next-candidate-selection',
        'upstream_handoff': 'RE-437',
        'closed_candidate_id': '763c9cd0e3f7',
        'selected_rank': '30',
        'selected_candidate_id': '0947c90b8674',
        'next_ticket': 'RE-439',
        'next_topic': 'ghidra-second-window-rank-30-narrow-export',
        'metadata_work_readiness': 'ready',
    }
    if any(result.get(field) != value for field, value in identity.items()):
        raise ValueError('output identity drift')
    safety = {
        'safe_context_status': 'filtered-metadata-only',
        'ready_to_reopen_domain_count': '0',
        'source_patch_authorized_count': '0',
        'selected_domain': 'none',
        'selected_pivot': 'none',
        'code_change_readiness': 'blocked',
    }
    if any(result.get(field) != value for field, value in safety.items()):
        raise ValueError('output safety drift')


def write(result, repo):
    """Write the selection, handoff, and explicit progress tracker."""
    validate_output(result)
    repo = Path(repo)
    outputs = []
    for suffix in ('candidates', 'summary', 'handoff'):
        path = repo / f'docs/reverse/generated/{PREFIX}-{suffix}.csv'
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('w', newline='', encoding='utf-8') as handle:
            writer = csv.DictWriter(handle, fieldnames=result.keys(), lineterminator='\n')
            writer.writeheader()
            writer.writerow(result)
        outputs.append(path)
    documents = {
        'docs/reverse/functions/re438-ghidra-second-window-next-candidate-selection.md': (
            '# RE-438 second-window next candidate selection\n\n'
            'Rank 30 is retained as a metadata-only candidate; source and code work remain blocked.\n'
        ),
        'docs/stories/RE-438-ghidra-second-window-next-candidate-selection.md': (
            '# RE-438 second-window next candidate selection\n\n'
            '## Progress tracker\n\n'
            '- [x] RE-437 handoff validated.\n'
            '- [x] Rank 29 closure retained.\n'
            '- [x] Rank 30 metadata candidate selected.\n'
            '- [x] Source and code work remain blocked.\n'
            '- [x] RE-439 selected.\n'
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
