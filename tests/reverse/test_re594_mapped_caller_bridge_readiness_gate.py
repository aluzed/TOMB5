import csv
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))


def test_re594_gate_is_metadata_only(tmp_path):
    from scripts.reverse import re594_mapped_caller_bridge_readiness_gate as module
    row = module.build(REPO)
    assert (row['story_id'], row['selected_rank'], row['selected_candidate_id'], row['candidate_level_proof_count'], row['next_ticket'], row['code_change_readiness']) == ('RE-594', '79', '6ba32f9cc1f5', '0', 'RE-595', 'blocked')
    assert len(module.write(row, tmp_path)) == 5


@pytest.mark.parametrize('field', tuple(__import__('scripts.reverse.re591_mapped_caller_bridge_readiness_gate', fromlist=['EXPECTED']).EXPECTED))
def test_re594_rejects_each_upstream_field_drift(tmp_path, field):
    from scripts.reverse import re594_mapped_caller_bridge_readiness_gate as module
    with (REPO / module.UPSTREAM).open(encoding='utf-8', newline='') as handle:
        reader = csv.DictReader(handle)
        rows, fields = list(reader), tuple(reader.fieldnames or ())
    rows[0][field] = 'drift'
    target = tmp_path / module.UPSTREAM
    target.parent.mkdir(parents=True)
    with target.open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator='\n')
        writer.writeheader(); writer.writerows(rows)
    with pytest.raises(ValueError, match='handoff drift'):
        module.build(tmp_path)


def test_re594_rejects_schema_drift(tmp_path):
    from scripts.reverse import re594_mapped_caller_bridge_readiness_gate as module
    target = tmp_path / module.UPSTREAM
    target.parent.mkdir(parents=True)
    target.write_text('bad_schema\nvalue\n', encoding='utf-8')
    with pytest.raises(ValueError, match='handoff schema drift'):
        module.build(tmp_path)
