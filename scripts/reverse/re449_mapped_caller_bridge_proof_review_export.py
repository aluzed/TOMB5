#!/usr/bin/env python3
"""Emit the fail-closed RE-449 mapped-caller proof-review export."""

import csv
from pathlib import Path

UPSTREAM = 'docs/reverse/generated/re448-mapped-caller-bridge-proof-readiness-review-handoff.csv'
PREFIX = 're449-mapped-caller-bridge-proof-review-export'
FORBIDDEN_OUTPUT_FRAGMENTS = (
    '0x', 'fun_', 'sub_', 'word_le_hex', 'payload_offset', 'opcode',
    'machine word', 'raw dump', 'raw_evidence', 'call_address',
    'branch target', 'call target', 'ghidra_entry', 'ghidra_name',
    'source_line_text', 'code.wad', 'gamewad.obj', 'secret', 'asset',
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


def one_row(path):
    with path.open(encoding='utf-8', newline='') as handle:
        reader = csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != FIELDS:
            raise ValueError('handoff schema drift')
        rows = list(reader)
    if len(rows) != 1:
        raise ValueError('handoff row-count drift')
    return rows[0]


def build(repo):
    """Validate RE-448 and retain its metadata-only, fail-closed state."""
    handoff = one_row(Path(repo) / UPSTREAM)
    expected = {
        'story_id': 'RE-448',
        'topic': 'mapped-caller-bridge-proof-readiness-review',
        'upstream_handoff': 'RE-447',
        'selected_candidate_id': '9faee15c7d52',
        'selected_rank': '31',
        'selected_subcluster': 'mapped-caller-bridge-readiness-gate',
        'source_symbol_context_count': '9',
        'bridge_class': 'mapped-caller-bridge',
        'safe_context_status': 'filtered-metadata-only',
        'next_ticket': 'RE-449',
        'next_topic': 'mapped-caller-bridge-proof-review-export',
        'metadata_work_readiness': 'ready',
        'code_change_readiness': 'blocked',
    }
    for field, value in expected.items():
        if handoff.get(field) != value:
            raise ValueError(f'handoff drift: {field}')
    safety_fields = (
        'source_backed_callsite_count', 'candidate_level_proof_count',
        'repository_symbol_direct_proof_count', 'ready_to_reopen_domain_count',
        'source_patch_authorized_count',
    )
    if any(handoff.get(field) != '0' for field in safety_fields):
        raise ValueError('safety-count drift')
    return {
        'story_id': 'RE-449',
        'topic': 'mapped-caller-bridge-proof-review-export',
        'upstream_handoff': 'RE-448',
        'selected_candidate_id': handoff['selected_candidate_id'],
        'selected_rank': handoff['selected_rank'],
        'selected_subcluster': handoff['selected_subcluster'],
        'source_symbol_context_count': handoff['source_symbol_context_count'],
        'bridge_class': handoff['bridge_class'],
        'safe_context_status': handoff['safe_context_status'],
        'source_backed_callsite_count': '0',
        'candidate_level_proof_count': '0',
        'repository_symbol_direct_proof_count': '0',
        'ready_to_reopen_domain_count': '0',
        'source_patch_authorized_count': '0',
        'selected_domain': 'none',
        'selected_pivot': 'none',
        'next_ticket': 'RE-450',
        'next_topic': 'mapped-caller-bridge-proof-review-readiness-gate',
        'metadata_work_readiness': 'ready',
        'code_change_readiness': 'blocked',
        'stop_condition': 'mapped caller bridge candidate has no safe source-backed proof context',
    }


def validate_output(result):
    if tuple(result) != FIELDS:
        raise ValueError('output schema drift')
    text = '\n'.join(str(value).lower() for value in result.values())
    if any(fragment in text for fragment in FORBIDDEN_OUTPUT_FRAGMENTS):
        raise ValueError('forbidden output fragment')
    identity = {
        'story_id': 'RE-449',
        'topic': 'mapped-caller-bridge-proof-review-export',
        'upstream_handoff': 'RE-448',
        'bridge_class': 'mapped-caller-bridge',
        'safe_context_status': 'filtered-metadata-only',
        'next_ticket': 'RE-450',
        'next_topic': 'mapped-caller-bridge-proof-review-readiness-gate',
        'metadata_work_readiness': 'ready',
    }
    if any(result.get(field) != value for field, value in identity.items()):
        raise ValueError('output identity drift')
    safety = {
        'source_backed_callsite_count': '0',
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
    """Write deterministic, sanitized proof-review artifacts."""
    validate_output(result)
    repo = Path(repo)
    outputs = []
    for suffix in ('proof', 'summary', 'handoff'):
        path = repo / f'docs/reverse/generated/{PREFIX}-{suffix}.csv'
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('w', newline='', encoding='utf-8') as handle:
            writer = csv.DictWriter(handle, fieldnames=result.keys(), lineterminator='\n')
            writer.writeheader()
            writer.writerow(result)
        outputs.append(path)
    documents = {
        'docs/reverse/functions/re449-mapped-caller-bridge-proof-review-export.md': (
            '# RE-449 mapped caller bridge proof review export\n\n'
            'No safe source-backed proof context is available; source and code work remain blocked.\n'
        ),
        'docs/stories/RE-449-mapped-caller-bridge-proof-review-export.md': (
            '# RE-449 mapped caller bridge proof review export\n\n'
            '## Progress tracker\n\n'
            '- [x] RE-448 handoff validated.\n'
            '- [x] Candidate proof-context absence confirmed.\n'
            '- [x] Filtered metadata-only safety retained.\n'
            '- [x] Source and code work remain blocked.\n'
            '- [x] RE-450 selected; not executed.\n'
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
