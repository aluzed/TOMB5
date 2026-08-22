import csv
import shutil
from pathlib import Path

import pytest

from scripts.reverse.re452_ghidra_second_window_rank_32_narrow_export import (
    FORBIDDEN_OUTPUT_FRAGMENTS,
    UPSTREAM,
    build,
    write,
)

REPO = Path(__file__).resolve().parents[2]


def test_re452_narrows_rank_32_as_metadata_only(tmp_path):
    result = build(REPO)
    assert result == {
        'story_id': 'RE-452',
        'topic': 'ghidra-second-window-rank-32-narrow-export',
        'upstream_handoff': 'RE-451',
        'selected_candidate_id': '0afc7c889086',
        'selected_rank': '32',
        'selected_subcluster': 'mapped-callee-bridge-readiness-gate',
        'source_symbol_context_count': '9',
        'bridge_class': 'mapped-callee-bridge',
        'safe_context_status': 'filtered-metadata-only',
        'candidate_level_proof_count': '0',
        'ready_to_reopen_domain_count': '0',
        'source_patch_authorized_count': '0',
        'selected_domain': 'none',
        'selected_pivot': 'none',
        'next_ticket': 'RE-453',
        'next_topic': 'mapped-callee-bridge-readiness-gate',
        'metadata_work_readiness': 'ready',
        'code_change_readiness': 'blocked',
        'stop_condition': 'narrow rank-32 export requires readiness gate before proof-domain selection',
    }
    outputs = write(result, tmp_path)
    assert {path.name for path in outputs} == {
        're452-ghidra-second-window-rank-32-narrow-export-contexts.csv',
        're452-ghidra-second-window-rank-32-narrow-export-summary.csv',
        're452-ghidra-second-window-rank-32-narrow-export-handoff.csv',
        're452-ghidra-second-window-rank-32-narrow-export.md',
        'RE-452-ghidra-second-window-rank-32-narrow-export.md',
    }
    for path in outputs:
        text = path.read_text(encoding='utf-8').lower()
        assert not any(fragment in text for fragment in FORBIDDEN_OUTPUT_FRAGMENTS)


def test_re452_rejects_upstream_and_output_drift(tmp_path):
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
