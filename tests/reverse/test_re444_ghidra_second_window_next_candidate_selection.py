import csv
import shutil
from pathlib import Path

import pytest

from scripts.reverse.re444_ghidra_second_window_next_candidate_selection import (
    FORBIDDEN_OUTPUT_FRAGMENTS,
    UPSTREAM,
    build,
    write,
)

REPO = Path(__file__).resolve().parents[2]


def test_re444_selects_rank_31_metadata_only_candidate(tmp_path):
    result = build(REPO)
    assert result == {
        'story_id': 'RE-444',
        'topic': 'ghidra-second-window-next-candidate-selection',
        'upstream_handoff': 'RE-443',
        'closed_candidate_id': '0947c90b8674',
        'selected_rank': '31',
        'selected_candidate_id': '9faee15c7d52',
        'selected_bridge_class': 'mapped-caller-bridge',
        'source_symbol_context_count': '9',
        'safe_context_status': 'filtered-metadata-only',
        'ready_to_reopen_domain_count': '0',
        'source_patch_authorized_count': '0',
        'selected_domain': 'none',
        'selected_pivot': 'none',
        'next_ticket': 'RE-445',
        'next_topic': 'ghidra-second-window-rank-31-narrow-export',
        'metadata_work_readiness': 'ready',
        'code_change_readiness': 'blocked',
        'stop_condition': 'rank 31 selected; source and code work remain blocked pending a narrow metadata gate',
    }
    outputs = write(result, tmp_path)
    assert {path.name for path in outputs} == {
        're444-ghidra-second-window-next-candidate-selection-candidates.csv',
        're444-ghidra-second-window-next-candidate-selection-summary.csv',
        're444-ghidra-second-window-next-candidate-selection-handoff.csv',
        're444-ghidra-second-window-next-candidate-selection.md',
        'RE-444-ghidra-second-window-next-candidate-selection.md',
    }
    for path in outputs:
        text = path.read_text(encoding='utf-8').lower()
        assert not any(fragment in text for fragment in FORBIDDEN_OUTPUT_FRAGMENTS)


def test_re444_rejects_upstream_and_output_drift(tmp_path):
    upstream = tmp_path / UPSTREAM
    upstream.parent.mkdir(parents=True)
    shutil.copy2(REPO / UPSTREAM, upstream)
    with upstream.open(encoding='utf-8', newline='') as handle:
        row = next(csv.DictReader(handle))
        fields = tuple(row)
    row['code_change_readiness'] = 'ready'
    with upstream.open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator='\n')
        writer.writeheader()
        writer.writerow(row)
    with pytest.raises(ValueError, match='handoff drift: code_change_readiness'):
        build(tmp_path)

    result = build(REPO)
    with pytest.raises(ValueError, match='forbidden output fragment'):
        write(dict(result, stop_condition='unsafe 0x value'), tmp_path)
    with pytest.raises(ValueError, match='output safety drift'):
        write(dict(result, code_change_readiness='ready'), tmp_path)
    with pytest.raises(ValueError, match='output safety drift'):
        write(dict(result, safe_context_status='unfiltered'), tmp_path)
    with pytest.raises(ValueError, match='output schema drift'):
        write(dict(result, extra='no'), tmp_path)
    with pytest.raises(ValueError, match='output identity drift'):
        write(dict(result, next_ticket='RE-999'), tmp_path)
