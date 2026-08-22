import csv
import shutil
from pathlib import Path

import pytest

from scripts.reverse.re439_ghidra_second_window_rank_30_narrow_export import (
    FORBIDDEN_OUTPUT_FRAGMENTS,
    UPSTREAM,
    build,
    write,
)

REPO = Path(__file__).resolve().parents[2]


def test_re439_narrows_rank_30_as_metadata_only(tmp_path):
    result = build(REPO)
    assert result == {
        'story_id': 'RE-439',
        'topic': 'ghidra-second-window-rank-30-narrow-export',
        'upstream_handoff': 'RE-438',
        'selected_candidate_id': '0947c90b8674',
        'selected_rank': '30',
        'selected_subcluster': 'mapped-caller-heavy-readiness-gate',
        'source_symbol_context_count': '8',
        'bridge_class': 'mapped-caller-heavy',
        'safe_context_status': 'filtered-metadata-only',
        'candidate_level_proof_count': '0',
        'ready_to_reopen_domain_count': '0',
        'source_patch_authorized_count': '0',
        'selected_domain': 'none',
        'selected_pivot': 'none',
        'next_ticket': 'RE-440',
        'next_topic': 'mapped-caller-heavy-readiness-gate',
        'metadata_work_readiness': 'ready',
        'code_change_readiness': 'blocked',
        'stop_condition': 'narrow rank-30 export requires readiness gate before proof-domain selection',
    }
    outputs = write(result, tmp_path)
    assert {path.name for path in outputs} == {
        're439-ghidra-second-window-rank-30-narrow-export-contexts.csv',
        're439-ghidra-second-window-rank-30-narrow-export-summary.csv',
        're439-ghidra-second-window-rank-30-narrow-export-handoff.csv',
        're439-ghidra-second-window-rank-30-narrow-export.md',
        'RE-439-ghidra-second-window-rank-30-narrow-export.md',
    }
    for path in outputs:
        text = path.read_text(encoding='utf-8').lower()
        assert not any(fragment in text for fragment in FORBIDDEN_OUTPUT_FRAGMENTS)


def test_re439_rejects_upstream_and_output_drift(tmp_path):
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
    with pytest.raises(ValueError, match='output schema drift'):
        write(dict(result, extra='no'), tmp_path)
    with pytest.raises(ValueError, match='output identity drift'):
        write(dict(result, next_ticket='RE-999'), tmp_path)
