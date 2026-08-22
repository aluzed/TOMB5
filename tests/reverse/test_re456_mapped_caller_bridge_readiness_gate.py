import csv
import shutil
from pathlib import Path

import pytest

from scripts.reverse.re456_mapped_caller_bridge_readiness_gate import (
    FORBIDDEN_OUTPUT_FRAGMENTS,
    UPSTREAM,
    build,
    write,
)

REPO = Path(__file__).resolve().parents[2]


def test_re456_preserves_fail_closed_mapped_caller_readiness_gate(tmp_path):
    result = build(REPO)
    assert result == {
        'story_id': 'RE-456',
        'topic': 'mapped-caller-bridge-readiness-gate',
        'upstream_handoff': 'RE-455',
        'selected_candidate_id': '8beda0f5763e',
        'selected_rank': '33',
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
        'next_ticket': 'RE-457',
        'next_topic': 'ghidra-second-window-next-candidate-selection',
        'metadata_work_readiness': 'ready',
        'code_change_readiness': 'blocked',
        'stop_condition': 'mapped caller bridge candidate has no safe source-backed proof context',
    }
    outputs = write(result, tmp_path)
    assert {path.name for path in outputs} == {
        're456-mapped-caller-bridge-readiness-gate-gate.csv',
        're456-mapped-caller-bridge-readiness-gate-summary.csv',
        're456-mapped-caller-bridge-readiness-gate-handoff.csv',
        're456-mapped-caller-bridge-readiness-gate.md',
        'RE-456-mapped-caller-bridge-readiness-gate.md',
    }
    for path in outputs:
        assert not any(fragment in path.read_text(encoding='utf-8').lower()
                       for fragment in FORBIDDEN_OUTPUT_FRAGMENTS)


def test_re456_rejects_upstream_schema_and_row_count_drift(tmp_path):
    upstream = tmp_path / UPSTREAM
    upstream.parent.mkdir(parents=True)
    upstream.write_text('unexpected\nvalue\n', encoding='utf-8')
    with pytest.raises(ValueError, match='handoff schema drift'):
        build(tmp_path)

    shutil.copy2(REPO / UPSTREAM, upstream)
    with upstream.open('a', encoding='utf-8') as handle:
        handle.write((REPO / UPSTREAM).read_text(encoding='utf-8').splitlines()[1] + '\n')
    with pytest.raises(ValueError, match='handoff row-count drift'):
        build(tmp_path)


def test_re456_rejects_unsafe_upstream_and_output_drift(tmp_path):
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
    for unsafe_text in ('unsafe opcode value', 'unsafe address trace',
                        'unsafe raw binary evidence', 'unsafe secret value'):
        with pytest.raises(ValueError, match='forbidden output fragment'):
            write(dict(result, stop_condition=unsafe_text), tmp_path)
    with pytest.raises(ValueError, match='output safety drift'):
        write(dict(result, code_change_readiness='ready'), tmp_path)
    with pytest.raises(ValueError, match='output identity drift'):
        write(dict(result, next_ticket='RE-999'), tmp_path)
    with pytest.raises(ValueError, match='output identity drift'):
        write(dict(result, selected_candidate_id='metadata-drift'), tmp_path)
    with pytest.raises(ValueError, match='output identity drift'):
        write(dict(result, stop_condition='metadata decision drift'), tmp_path)
