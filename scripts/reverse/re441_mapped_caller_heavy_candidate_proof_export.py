#!/usr/bin/env python3
"""Emit fail-closed RE-441 metadata without inspecting game assets."""

import csv
from pathlib import Path

UPSTREAM = 'docs/reverse/generated/re440-mapped-caller-heavy-readiness-gate-handoff.csv'
PREFIX = 're441-mapped-caller-heavy-candidate-proof'
FORBIDDEN_OUTPUT_FRAGMENTS = (
    '0x', 'fun_', 'sub_', 'word_le_hex', 'payload_offset', 'opcode',
    'machine word', 'raw dump', 'raw_evidence', 'call_address',
    'branch target', 'call target', 'ghidra_entry', 'ghidra_name',
    'source_line_text', 'code.wad', 'gamewad.obj', 'secret',
)


def build(repo):
    """Validate RE-440 and retain its metadata-only fail-closed decision."""
    repo = Path(repo)
    with (repo / UPSTREAM).open(encoding='utf-8', newline='') as handle:
        reader = csv.DictReader(handle)
        expected_fields = (
            'story_id', 'topic', 'upstream_handoff', 'selected_candidate_id',
            'selected_rank', 'selected_subcluster', 'source_symbol_context_count',
            'bridge_class', 'safe_context_status',
            'candidate_level_proof_count', 'ready_to_reopen_domain_count',
            'source_patch_authorized_count', 'selected_domain', 'selected_pivot',
            'next_ticket', 'next_topic', 'metadata_work_readiness',
            'code_change_readiness', 'stop_condition',
        )
        if tuple(reader.fieldnames or ()) != expected_fields:
            raise ValueError('handoff schema drift')
        rows = list(reader)
    if len(rows) != 1:
        raise ValueError('handoff row-count drift')
    handoff = rows[0]
    expected = {
        'story_id': 'RE-440',
        'next_ticket': 'RE-441',
        'next_topic': 'mapped-caller-heavy-candidate-proof-export',
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
        'story_id': 'RE-441',
        'topic': 'mapped-caller-heavy-candidate-proof-export',
        'upstream_handoff': 'RE-440',
        'selected_candidate_id': handoff['selected_candidate_id'],
        'selected_rank': handoff['selected_rank'],
        'selected_subcluster': handoff['selected_subcluster'],
        'source_symbol_context_count': handoff['source_symbol_context_count'],
        'bridge_class': handoff['bridge_class'],
        'safe_context_status': handoff['safe_context_status'],
        'candidate_level_proof_count': '0',
        'repository_symbol_direct_proof_count': '0',
        'ready_to_reopen_domain_count': '0',
        'source_patch_authorized_count': '0',
        'selected_domain': 'none',
        'selected_pivot': 'none',
        'next_ticket': 'RE-442',
        'next_topic': 'mapped-caller-heavy-candidate-callsite-map',
        'metadata_work_readiness': 'ready',
        'code_change_readiness': 'blocked',
        'stop_condition': 'mapped caller-heavy context has no direct candidate proof',
    }


def validate_output(result):
    """Reject raw, asset, secret, schema, identity, and readiness drift."""
    expected_fields = (
        'story_id', 'topic', 'upstream_handoff', 'selected_candidate_id',
        'selected_rank', 'selected_subcluster', 'source_symbol_context_count',
        'bridge_class', 'safe_context_status', 'candidate_level_proof_count',
        'repository_symbol_direct_proof_count', 'ready_to_reopen_domain_count',
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
        'story_id': 'RE-441',
        'topic': 'mapped-caller-heavy-candidate-proof-export',
        'upstream_handoff': 'RE-440',
        'next_ticket': 'RE-442',
        'next_topic': 'mapped-caller-heavy-candidate-callsite-map',
        'metadata_work_readiness': 'ready',
        'bridge_class': 'mapped-caller-heavy',
        'safe_context_status': 'filtered-metadata-only',
    }
    if any(result.get(field) != value for field, value in identity.items()):
        raise ValueError('output identity drift')
    safety = {
        'candidate_level_proof_count': '0',
        'repository_symbol_direct_proof_count': '0',
        'ready_to_reopen_domain_count': '0',
        'source_patch_authorized_count': '0',
        'selected_domain': 'none',
        'selected_pivot': 'none',
        'code_change_readiness': 'blocked',
    }
    if any(result.get(field) != value for field, value in safety.items()):
        raise ValueError('output safety drift')


def write(result, repo):
    """Write metadata-only candidate-proof artifacts and progress tracking."""
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
        'docs/reverse/functions/re441-mapped-caller-heavy-candidate-proof-export.md': (
            '# RE-441 mapped caller-heavy candidate proof export\n\n'
            'No direct candidate proof is available; source changes remain blocked.\n'
        ),
        'docs/stories/RE-441-mapped-caller-heavy-candidate-proof-export.md': (
            '# RE-441 mapped caller-heavy candidate proof export\n\n'
            '## Progress tracker\n\n'
            '- [x] RE-440 handoff validated.\n'
            '- [x] Candidate-proof absence confirmed.\n'
            '- [x] Metadata-only export emitted.\n'
            '- [x] Domain and source changes remain blocked.\n'
            '- [x] RE-442 selected.\n'
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
