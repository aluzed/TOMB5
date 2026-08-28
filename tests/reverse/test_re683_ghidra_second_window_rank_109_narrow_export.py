import csv
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))


def test_re683_narrow_export_is_metadata_only(tmp_path):
    from scripts.reverse import re683_ghidra_second_window_rank_109_narrow_export as module
    row = module.build(REPO)
    assert (row['story_id'], row['selected_rank'], row['selected_candidate_id'], row['bridge_class'], row['next_ticket'], row['code_change_readiness']) == ('RE-683', '109', '08963c88efc1', 'mapped-caller-bridge', 'RE-684', 'blocked')
    assert len(module.write(row, tmp_path)) == 5


def test_re683_rejects_each_upstream_field_and_output_drift(tmp_path):
    from scripts.reverse import re683_ghidra_second_window_rank_109_narrow_export as module
    with (REPO / module.UPSTREAM).open(encoding='utf-8', newline='') as handle:
        reader = csv.DictReader(handle); original, fields = next(reader), tuple(reader.fieldnames or ())
    assert set(module.EXPECTED) == set(fields)
    for field in module.EXPECTED:
        changed = dict(original); changed[field] = 'drift'
        target = tmp_path / module.UPSTREAM; target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('w', encoding='utf-8', newline='') as handle:
            writer = csv.DictWriter(handle, fieldnames=fields, lineterminator='\n'); writer.writeheader(); writer.writerow(changed)
        with pytest.raises(ValueError, match=rf'handoff drift: {field}'):
            module.build(tmp_path)
    for field in module.OUTPUT:
        changed = module.build(REPO); changed[field] = 'drift'
        with pytest.raises(ValueError, match='output drift'):
            module.write(changed, tmp_path)


def test_re683_rejects_schema_and_row_count_drift(tmp_path):
    from scripts.reverse import re683_ghidra_second_window_rank_109_narrow_export as module
    target = tmp_path / module.UPSTREAM; target.parent.mkdir(parents=True)
    target.write_text('bad\nvalue\n', encoding='utf-8')
    with pytest.raises(ValueError, match='handoff schema drift'): module.build(tmp_path)
    valid = (REPO / module.UPSTREAM).read_text(encoding='utf-8')
    target.write_text(valid + valid.splitlines()[1] + '\n', encoding='utf-8')
    with pytest.raises(ValueError, match='handoff row-count drift'): module.build(tmp_path)
