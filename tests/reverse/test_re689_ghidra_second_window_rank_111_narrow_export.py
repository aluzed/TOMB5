import csv
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))


def test_re689_narrow_export_is_metadata_only(tmp_path):
    from scripts.reverse import re689_ghidra_second_window_rank_111_narrow_export as module

    row = module.build(REPO)
    assert (row['story_id'], row['selected_rank'], row['selected_candidate_id'], row['bridge_class'], row['next_ticket'], row['code_change_readiness']) == ('RE-689', '111', '5fec2b3eae09', 'mapped-callee-bridge', 'RE-690', 'blocked')
    assert len(module.write(row, tmp_path)) == 5


def test_re689_rejects_every_upstream_field_drift(tmp_path):
    from scripts.reverse import re689_ghidra_second_window_rank_111_narrow_export as module

    with (REPO / module.UPSTREAM).open(encoding='utf-8', newline='') as handle:
        reader = csv.DictReader(handle)
        original, fields = next(reader), tuple(reader.fieldnames or ())
    assert set(module.EXPECTED) == set(fields)
    for field in module.EXPECTED:
        row = dict(original)
        row[field] = 'drift'
        target = tmp_path / module.UPSTREAM
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('w', encoding='utf-8', newline='') as handle:
            writer = csv.DictWriter(handle, fieldnames=fields, lineterminator='\n')
            writer.writeheader()
            writer.writerow(row)
        with pytest.raises(ValueError, match=rf'handoff drift: {field}'):
            module.build(tmp_path)


def test_re689_rejects_schema_row_count_and_output_drift(tmp_path):
    from scripts.reverse import re689_ghidra_second_window_rank_111_narrow_export as module

    target = tmp_path / module.UPSTREAM
    target.parent.mkdir(parents=True)
    target.write_text('bad\nvalue\n', encoding='utf-8')
    with pytest.raises(ValueError, match='handoff schema drift'):
        module.build(tmp_path)
    valid = (REPO / module.UPSTREAM).read_text(encoding='utf-8')
    target.write_text(valid + valid.splitlines()[1] + '\n', encoding='utf-8')
    with pytest.raises(ValueError, match='handoff row-count drift'):
        module.build(tmp_path)
    row = module.build(REPO)
    for field in module.OUTPUT:
        changed = dict(row)
        changed[field] = 'drift'
        with pytest.raises(ValueError, match='output drift'):
            module.write(changed, tmp_path)
