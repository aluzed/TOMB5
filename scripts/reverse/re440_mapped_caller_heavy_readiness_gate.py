#!/usr/bin/env python3
"""Emit the fail-closed RE-440 mapped-caller-heavy readiness decision."""

import csv
from pathlib import Path

UPSTREAM = 'docs/reverse/generated/re439-ghidra-second-window-rank-30-narrow-export-handoff.csv'
PREFIX = 're440-mapped-caller-heavy-readiness-gate'
FORBIDDEN_OUTPUT_FRAGMENTS = (
    '0x', 'fun_', 'sub_', 'word_le_hex', 'payload_offset', 'opcode',
    'machine word', 'raw dump', 'raw_evidence', 'call_address',
    'branch target', 'call target', 'ghidra_entry', 'ghidra_name',
    'source_line_text', 'code.wad', 'gamewad.obj', 'secret',
)


def build(repo):
    """Validate RE-439 and retain a metadata-only fail-closed decision."""
    repo = Path(repo)
    with (repo / UPSTREAM).open(encoding='utf-8', newline='') as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 1:
        raise ValueError('handoff row-count drift')
    handoff = rows[0]
    expected = {
        'story_id': 'RE-439',
        'next_ticket': 'RE-440',
        'next_topic': 'mapped-caller-heavy-readiness-gate',
        'selected_candidate_id': '0947c90b8674',
        'selected_rank': '30',
        'selected_subcluster': 'mapped-caller-heavy-readiness-gate',
        'source_symbol_context_count': '8',
        'bridge_class': 'mapped-caller-heavy',
        'safe_context_status': 'filtered-metadata-only',
        'metadata_work_readiness': 'ready',
        'code_change_readiness': 'blocked',
        'selected_domain': 'none',
        'selected_pivot': 'none',
    }
    for field, value in expected.items():
        if handoff.get(field) != value:
            raise ValueError(f'handoff drift: {field}')
    safety_fields = (
        'candidate_level_proof_count',
        'ready_to_reopen_domain_count',
        'source_patch_authorized_count',
    )
    if any(handoff.get(field) != '0' for field in safety_fields):
        raise ValueError('safety-count drift')
    return {
        'story_id': 'RE-440',
        'topic': 'mapped-caller-heavy-readiness-gate',
        'upstream_handoff': 'RE-439',
        'selected_candidate_id': handoff['selected_candidate_id'],
        'selected_rank': handoff['selected_rank'],
        'selected_subcluster': handoff['selected_subcluster'],
        'source_symbol_context_count': handoff['source_symbol_context_count'],
        'bridge_class': handoff['bridge_class'],
        'safe_context_status': handoff['safe_context_status'],
        'candidate_level_proof_count': '0',
        'ready_to_reopen_domain_count': '0',
        'source_patch_authorized_count': '0',
        'selected_domain': 'none',
        'selected_pivot': 'none',
        'next_ticket': 'RE-441',
        'next_topic': 'mapped-caller-heavy-candidate-proof-export',
        'metadata_work_readiness': 'ready',
        'code_change_readiness': 'blocked',
        'stop_condition': 'mapped caller-heavy context remains prioritization signal without candidate proof',
    }


def validate_output(result):
    """Reject raw, asset, secret, identity, schema, and readiness drift."""
    expected_fields = (
        'story_id', 'topic', 'upstream_handoff', 'selected_candidate_id',
        'selected_rank', 'selected_subcluster', 'source_symbol_context_count',
        'bridge_class', 'safe_context_status',
        'candidate_level_proof_count', 'ready_to_reopen_domain_count',
        'source_patch_authorized_count', 'selected_domain', 'selected_pivot',
        'next_ticket', 'next_topic', 'metadata_work_readiness',
        'code_change_readiness', 'stop_condition',
    )
    if tuple(result) != expected_fields:
        raise ValueError('output schema drift')
    text = '\n'.join(str(value).lower() for value in result.values())
    if any(fragment in text for fragment in FORBIDDEN_OUTPUT_FRAGMENTS):
        raise ValueError('forbidden output fragment')
    identity = {
        'story_id': 'RE-440',
        'topic': 'mapped-caller-heavy-readiness-gate',
        'upstream_handoff': 'RE-439',
        'next_ticket': 'RE-441',
        'next_topic': 'mapped-caller-heavy-candidate-proof-export',
        'metadata_work_readiness': 'ready',
        'bridge_class': 'mapped-caller-heavy',
        'safe_context_status': 'filtered-metadata-only',
    }
    if any(result.get(field) != value for field, value in identity.items()):
        raise ValueError('output identity drift')
    safety = {
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
    """Write metadata-only artifacts and an explicit progress tracker."""
    validate_output(result)
    repo = Path(repo)
    outputs = []
    for suffix in ('gate', 'summary', 'handoff'):
        path = repo / f'docs/reverse/generated/{PREFIX}-{suffix}.csv'
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('w', newline='', encoding='utf-8') as handle:
            writer = csv.DictWriter(handle, fieldnames=result.keys(), lineterminator='\n')
            writer.writeheader()
            writer.writerow(result)
        outputs.append(path)
    documents = {
        'docs/reverse/functions/re440-mapped-caller-heavy-readiness-gate.md': (
            '# RE-440 mapped caller-heavy readiness gate\n\n'
            'Candidate proof is absent; source changes remain blocked.\n'
        ),
        'docs/stories/RE-440-mapped-caller-heavy-readiness-gate.md': (
            '# RE-440 mapped caller-heavy readiness gate\n\n'
            '## Progress tracker\n\n'
            '- [x] RE-439 handoff validated.\n'
            '- [x] Candidate-proof absence confirmed.\n'
            '- [x] Domain and source changes remain blocked.\n'
            '- [x] RE-441 selected.\n'
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
