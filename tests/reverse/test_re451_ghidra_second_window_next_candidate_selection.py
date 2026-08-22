import csv
import shutil
from pathlib import Path

import pytest

from scripts.reverse.re451_ghidra_second_window_next_candidate_selection import (
    FORBIDDEN_OUTPUT_FRAGMENTS,
    UPSTREAM,
    build,
    write,
)

REPO = Path(__file__).resolve().parents[2]


def test_re451_selects_rank_32_metadata_only_candidate(tmp_path):
    result = build(REPO)
    assert result == {
        'story_id': 'RE-451',
        'topic': 'ghidra-second-window-next-candidate-selection',
        'upstream_handoff': 'RE-450',
        'closed_candidate_id': '9faee15c7d52',
        'selected_rank': '32',
        'selected_candidate_id': '0afc7c889086',
        'selected_bridge_class': 'mapped-callee-bridge',
        'source_symbol_context_count': '9',
        'safe_context_status': 'filtered-metadata-only',
        'ready_to_reopen_domain_count': '0',
        'source_patch_authorized_count': '0',
        'selected_domain': 'none',
        'selected_pivot': 'none',
        'next_ticket': 'RE-452',
        'next_topic': 'ghidra-second-window-rank-32-narrow-export',
        'metadata_work_readiness': 'ready',
        'code_change_readiness': 'blocked',
        'stop_condition': 'rank 32 selected; source and code work remain blocked pending a narrow metadata gate',
    }
    outputs = write(result, tmp_path)
    assert {path.name for path in outputs} == {
        're451-ghidra-second-window-next-candidate-selection-candidates.csv',
        're451-ghidra-second-window-next-candidate-selection-summary.csv',
        're451-ghidra-second-window-next-candidate-selection-handoff.csv',
        're451-ghidra-second-window-next-candidate-selection.md',
        'RE-451-ghidra-second-window-next-candidate-selection.md',
    }
    for path in outputs:
        assert not any(fragment in path.read_text(encoding='utf-8').lower()
                       for fragment in FORBIDDEN_OUTPUT_FRAGMENTS)


def test_re451_rejects_upstream_and_output_drift(tmp_path):
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
