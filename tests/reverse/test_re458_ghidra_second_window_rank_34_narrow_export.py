import csv
import shutil
from pathlib import Path

import pytest

from scripts.reverse.re458_ghidra_second_window_rank_34_narrow_export import (
    FORBIDDEN_OUTPUT_FRAGMENTS, UPSTREAM, build, write,
)

REPO = Path(__file__).resolve().parents[2]


def test_re458_narrows_rank_34_as_metadata_only(tmp_path):
    result = build(REPO)
    assert result['story_id'] == 'RE-458'
    assert result['selected_candidate_id'] == 'aaf42cb3b10b'
    assert result['selected_rank'] == '34'
    assert result['bridge_class'] == 'mapped-caller-bridge'
    assert result['next_ticket'] == 'RE-459'
    assert result['next_topic'] == 'mapped-caller-bridge-readiness-gate'
    assert result['code_change_readiness'] == 'blocked'
    assert result['source_patch_authorized_count'] == '0'
    outputs = write(result, tmp_path)
    assert len(outputs) == 5
    for path in outputs:
        assert not any(fragment in path.read_text(encoding='utf-8').lower()
                       for fragment in FORBIDDEN_OUTPUT_FRAGMENTS)


def test_re458_rejects_upstream_and_output_drift(tmp_path):
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
        write(dict(result, stop_condition='unsafe opcode evidence'), tmp_path)
    with pytest.raises(ValueError, match='output safety drift'):
        write(dict(result, code_change_readiness='ready'), tmp_path)
