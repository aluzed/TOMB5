import csv
import shutil
from pathlib import Path

import pytest

from scripts.reverse.re447_mapped_caller_bridge_candidate_proof_export import (
    FORBIDDEN_OUTPUT_FRAGMENTS,
    UPSTREAM,
    build,
    write,
)

REPO = Path(__file__).resolve().parents[2]


def test_re447_preserves_fail_closed_candidate_proof_export(tmp_path):
    result = build(REPO)
    assert result == {
        'story_id': 'RE-447',
        'topic': 'mapped-caller-bridge-candidate-proof-export',
        'upstream_handoff': 'RE-446',
        'selected_candidate_id': '9faee15c7d52',
        'selected_rank': '31',
        'selected_subcluster': 'mapped-caller-bridge-readiness-gate',
        'source_symbol_context_count': '9',
        'bridge_class': 'mapped-caller-bridge',
        'safe_context_status': 'filtered-metadata-only',
        'source_backed_callsite_count': '0',
        'candidate_level_proof_count': '0',
        'repository_symbol_direct_proof_count': '0',
        'ready_to_reopen_domain_count': '0',
        'source_patch_authorized_count': '0',
        'selected_domain': 'none',
        'selected_pivot': 'none',
        'next_ticket': 'RE-448',
        'next_topic': 'mapped-caller-bridge-proof-readiness-review',
        'metadata_work_readiness': 'ready',
        'code_change_readiness': 'blocked',
        'stop_condition': 'mapped caller bridge candidate has no safe source-backed proof context',
    }
    outputs = write(result, tmp_path)
    assert {path.name for path in outputs} == {
        're447-mapped-caller-bridge-candidate-proof-export-proof.csv',
        're447-mapped-caller-bridge-candidate-proof-export-summary.csv',
        're447-mapped-caller-bridge-candidate-proof-export-handoff.csv',
        're447-mapped-caller-bridge-candidate-proof-export.md',
        'RE-447-mapped-caller-bridge-candidate-proof-export.md',
    }
    for path in outputs:
        text = path.read_text(encoding='utf-8').lower()
        assert not any(fragment in text for fragment in FORBIDDEN_OUTPUT_FRAGMENTS)


def test_re447_rejects_unsafe_upstream_or_output_drift(tmp_path):
    upstream = tmp_path / UPSTREAM
    upstream.parent.mkdir(parents=True)
    shutil.copy2(REPO / UPSTREAM, upstream)
    with upstream.open(encoding='utf-8', newline='') as handle:
        row = next(csv.DictReader(handle))
        fields = tuple(row)
    row['repository_symbol_direct_proof_count'] = '1'
    with upstream.open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator='\n')
        writer.writeheader()
        writer.writerow(row)
    with pytest.raises(ValueError, match='safety-count drift'):
        build(tmp_path)

    with (REPO / UPSTREAM).open(encoding='utf-8', newline='') as handle:
        safe_row = next(csv.DictReader(handle))
    with upstream.open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(
            handle, fieldnames=fields + ('unexpected',), lineterminator='\n'
        )
        writer.writeheader()
        writer.writerow(dict(safe_row, unexpected='no'))
    with pytest.raises(ValueError, match='handoff schema drift'):
        build(tmp_path)

    result = build(REPO)
    for forbidden in ('0x', 'opcode', 'fun_', 'asset', 'secret'):
        with pytest.raises(ValueError, match='forbidden output fragment'):
            write(dict(result, stop_condition=f'unsafe {forbidden} value'), tmp_path)
    with pytest.raises(ValueError, match='output safety drift'):
        write(dict(result, code_change_readiness='ready'), tmp_path)
    with pytest.raises(ValueError, match='output schema drift'):
        write(dict(result, extra='no'), tmp_path)
    with pytest.raises(ValueError, match='output identity drift'):
        write(dict(result, next_ticket='RE-999'), tmp_path)
