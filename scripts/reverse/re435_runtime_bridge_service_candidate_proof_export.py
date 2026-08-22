#!/usr/bin/env python3
"""Emit fail-closed metadata for RE-435 without inspecting game assets."""

import csv
from pathlib import Path

UPSTREAM = 'docs/reverse/generated/re434-runtime-bridge-service-readiness-gate-handoff.csv'
PREFIX = 're435-runtime-bridge-service-candidate-proof'
FORBIDDEN_OUTPUT_FRAGMENTS = (
    '0x', 'fun_', 'sub_', 'word_le_hex', 'payload_offset', 'opcode',
    'machine word', 'raw dump', 'raw_evidence', 'call_address',
    'branch target', 'call target', 'ghidra_entry', 'ghidra_name',
    'source_line_text', 'code.wad', 'gamewad.obj', 'secret',
)


def build(repo):
    repo = Path(repo)
    with (repo / UPSTREAM).open(encoding='utf-8', newline='') as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 1:
        raise ValueError('handoff row-count drift')
    handoff = rows[0]
    expected = {
        'story_id': 'RE-434',
        'next_ticket': 'RE-435',
        'next_topic': 'runtime-bridge-service-candidate-proof-export',
        'selected_candidate_id': '763c9cd0e3f7',
        'selected_rank': '29',
        'selected_subcluster': 'runtime-bridge-service',
        'source_symbol_context_count': '10',
        'metadata_work_readiness': 'ready',
        'code_change_readiness': 'blocked',
        'selected_domain': 'none',
        'selected_pivot': 'none',
    }
    for field, value in expected.items():
        if handoff.get(field) != value:
            raise ValueError(f'handoff drift: {field}')
    safety_fields = (
        'candidate_level_proof_count', 'ready_to_reopen_domain_count',
        'source_patch_authorized_count',
    )
    if any(handoff.get(field) != '0' for field in safety_fields):
        raise ValueError('safety-count drift')
    return {
        'story_id': 'RE-435',
        'topic': 'runtime-bridge-service-candidate-proof-export',
        'upstream_handoff': 'RE-434',
        'selected_candidate_id': handoff['selected_candidate_id'],
        'selected_rank': handoff['selected_rank'],
        'selected_subcluster': handoff['selected_subcluster'],
        'source_symbol_context_count': handoff['source_symbol_context_count'],
        'candidate_level_proof_count': '0',
        'repository_symbol_direct_proof_count': '0',
        'ready_to_reopen_domain_count': '0',
        'source_patch_authorized_count': '0',
        'selected_domain': 'none',
        'selected_pivot': 'none',
        'next_ticket': 'RE-436',
        'next_topic': 'runtime-bridge-service-candidate-callsite-map',
        'metadata_work_readiness': 'ready',
        'code_change_readiness': 'blocked',
        'stop_condition': 'runtime bridge symbolic context has no direct candidate proof',
    }


def validate_output(result):
    text = '\n'.join(str(value).lower() for value in result.values())
    if any(fragment in text for fragment in FORBIDDEN_OUTPUT_FRAGMENTS):
        raise ValueError('forbidden output fragment')
    expected = {
        'candidate_level_proof_count': '0',
        'repository_symbol_direct_proof_count': '0',
        'ready_to_reopen_domain_count': '0',
        'source_patch_authorized_count': '0',
        'selected_domain': 'none',
        'selected_pivot': 'none',
        'code_change_readiness': 'blocked',
    }
    if any(result.get(field) != value for field, value in expected.items()):
        raise ValueError('output safety drift')


def write(result, repo):
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
        'docs/reverse/functions/re435-runtime-bridge-service-candidate-proof-export.md': (
            '# RE-435 runtime bridge service candidate proof export\n\n'
            'No direct candidate proof is available; source changes remain blocked.\n'
        ),
        'docs/stories/RE-435-runtime-bridge-service-candidate-proof-export.md': (
            '# RE-435 runtime bridge service candidate proof export\n\n'
            '## Progress tracker\n\n'
            '- [x] RE-434 handoff validated.\n'
            '- [x] Candidate-proof absence confirmed.\n'
            '- [x] Metadata-only export emitted.\n'
            '- [x] Source changes blocked.\n'
            '- [x] RE-436 selected.\n'
        ),
    }
    for relative, text in documents.items():
        path = repo / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')
        outputs.append(path)
    return outputs


if __name__ == '__main__':
    result = build(Path(__file__).resolve().parents[2])
    write(result, Path(__file__).resolve().parents[2])
