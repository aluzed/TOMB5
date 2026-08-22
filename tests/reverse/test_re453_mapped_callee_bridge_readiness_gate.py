import csv
import shutil
from pathlib import Path

import pytest

from scripts.reverse.re453_mapped_callee_bridge_readiness_gate import (
    FORBIDDEN_OUTPUT_FRAGMENTS,
    UPSTREAM,
    build,
    write,
)

REPO = Path(__file__).resolve().parents[2]


def test_re453_preserves_fail_closed_mapped_callee_readiness_gate(tmp_path):
    result = build(REPO)
    assert result == {
        'story_id': 'RE-453',
        'topic': 'mapped-callee-bridge-readiness-gate',
        'upstream_handoff': 'RE-452',
        'selected_candidate_id': '0afc7c889086',
        'selected_rank': '32',
        'selected_subcluster': 'mapped-callee-bridge-readiness-gate',
        'source_symbol_context_count': '9',
        'bridge_class': 'mapped-callee-bridge',
        'safe_context_status': 'filtered-metadata-only',
        'source_backed_callsite_count': '0',
        'candidate_level_proof_count': '0',
        'repository_symbol_direct_proof_count': '0',
        'ready_to_reopen_domain_count': '0',
        'source_patch_authorized_count': '0',
        'selected_domain': 'none',
        'selected_pivot': 'none',
        'next_ticket': 'RE-454',
        'next_topic': 'ghidra-second-window-next-candidate-selection',
        'metadata_work_readiness': 'ready',
        'code_change_readiness': 'blocked',
        'stop_condition': 'mapped callee bridge candidate has no safe source-backed proof context',
    }
    outputs = write(result, tmp_path)
    assert {path.name for path in outputs} == {
        're453-mapped-callee-bridge-readiness-gate-gate.csv',
        're453-mapped-callee-bridge-readiness-gate-summary.csv',
        're453-mapped-callee-bridge-readiness-gate-handoff.csv',
        're453-mapped-callee-bridge-readiness-gate.md',
        'RE-453-mapped-callee-bridge-readiness-gate.md',
    }
    for path in outputs:
        assert not any(fragment in path.read_text(encoding='utf-8').lower()
                       for fragment in FORBIDDEN_OUTPUT_FRAGMENTS)


def test_re453_rejects_upstream_schema_and_row_count_drift(tmp_path):
    upstream = tmp_path / UPSTREAM
    upstream.parent.mkdir(parents=True)
    upstream.write_text('unexpected\nvalue\n', encoding='utf-8')
    with pytest.raises(ValueError, match='handoff schema drift'):
        build(tmp_path)

    shutil.copy2(REPO / UPSTREAM, upstream)
    with upstream.open('a', encoding='utf-8') as handle:
        handle.write((REPO / UPSTREAM).read_text(encoding='utf-8').splitlines()[1] + '\\n')
    with pytest.raises(ValueError, match='handoff row-count drift'):
        build(tmp_path)


def test_re453_rejects_unsafe_upstream_and_output_drift(tmp_path):
    upstream = tmp_path / UPSTREAM
    upstream.parent.mkdir(parents=True)
    shutil.copy2(REPO / UPSTREAM, upstream)
    with upstream.open(encoding='utf-8', newline='') as handle:
        row = next(csv.DictReader(handle))
        fields = tuple(row)
    row['source_patch_authorized_count'] = '1'
    with upstream.open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator='\n')
        writer.writeheader()
        writer.writerow(row)
    with pytest.raises(ValueError, match='safety-count drift'):
        build(tmp_path)

    result = build(REPO)
    with pytest.raises(ValueError, match='forbidden output fragment'):
        write(dict(result, stop_condition='unsafe opcode value'), tmp_path)
    with pytest.raises(ValueError, match='output safety drift'):
        write(dict(result, code_change_readiness='ready'), tmp_path)
    with pytest.raises(ValueError, match='output identity drift'):
        write(dict(result, next_ticket='RE-999'), tmp_path)
