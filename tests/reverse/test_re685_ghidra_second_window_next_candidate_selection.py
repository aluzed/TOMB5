import csv
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))


def test_re685_selects_rank_110_as_metadata_only(tmp_path):
    from scripts.reverse import re685_ghidra_second_window_next_candidate_selection as module

    row = module.build(REPO)
    assert (
        row['story_id'], row['closed_candidate_id'], row['selected_rank'],
        row['selected_candidate_id'], row['selected_bridge_class'],
        row['next_ticket'], row['code_change_readiness'],
    ) == (
        'RE-685', '08963c88efc1', '110', '47dbffdb0518',
        'mapped-callee-bridge', 'RE-686', 'blocked',
    )
    assert len(module.write(row, tmp_path)) == 5


def test_re685_rejects_all_upstream_and_output_drift(tmp_path):
    from scripts.reverse import re685_ghidra_second_window_next_candidate_selection as module

    with (REPO / module.UPSTREAM).open(encoding='utf-8', newline='') as handle:
        reader = csv.DictReader(handle)
        original, fields = next(reader), tuple(reader.fieldnames or ())
    assert set(module.EXPECTED) == set(fields)
    for field in module.EXPECTED:
        drift = dict(original)
        drift[field] = 'drift'
        target = tmp_path / module.UPSTREAM
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('w', encoding='utf-8', newline='') as handle:
            writer = csv.DictWriter(handle, fieldnames=fields, lineterminator='\n')
            writer.writeheader()
            writer.writerow(drift)
        with pytest.raises(ValueError, match=rf'handoff drift: {field}'):
            module.build(tmp_path)
    row = module.build(REPO)
    for field in module.OUTPUT:
        drift = dict(row)
        drift[field] = 'drift'
        with pytest.raises(ValueError, match='output drift'):
            module.write(drift, tmp_path)


def test_re685_rejects_schema_row_count_and_ranked_candidate_drift(tmp_path, monkeypatch):
    from scripts.reverse import re685_ghidra_second_window_next_candidate_selection as module

    target = tmp_path / module.UPSTREAM
    target.parent.mkdir(parents=True)
    target.write_text('bad\nvalue\n', encoding='utf-8')
    with pytest.raises(ValueError, match='handoff schema drift'):
        module.build(tmp_path)
    valid = (REPO / module.UPSTREAM).read_text(encoding='utf-8')
    target.write_text(valid + valid.splitlines()[1] + '\n', encoding='utf-8')
    with pytest.raises(ValueError, match='handoff row-count drift'):
        module.build(tmp_path)
    monkeypatch.setattr(module.candidate_source.candidates, 'build_bridge_candidates', lambda repo: ([], None))
    with pytest.raises(ValueError, match='ranked candidate drift'):
        module.build(REPO)
