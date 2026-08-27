import csv
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))


def test_re656_metadata_only_narrow_export(tmp_path):
    from scripts.reverse import re656_ghidra_second_window_rank_100_narrow_export as module
    row = module.build(REPO)
    assert (row['story_id'], row['selected_rank'], row['selected_candidate_id'], row['bridge_class'], row['next_ticket'], row['code_change_readiness']) == ('RE-656', '100', '3f3ca77b4b8e', 'mapped-caller-callee-bridge', 'RE-657', 'blocked')
    assert len(module.write(row, tmp_path)) == 5


@pytest.mark.parametrize('field', ('story_id', 'topic', 'upstream_handoff', 'closed_candidate_id', 'selected_rank', 'selected_candidate_id', 'selected_bridge_class', 'source_symbol_context_count', 'safe_context_status', 'ready_to_reopen_domain_count', 'source_patch_authorized_count', 'selected_domain', 'selected_pivot', 'next_ticket', 'next_topic', 'metadata_work_readiness', 'code_change_readiness', 'stop_condition'))
def test_re656_rejects_each_upstream_handoff_field_drift(tmp_path, field):
    from scripts.reverse import re656_ghidra_second_window_rank_100_narrow_export as module
    with (REPO / module.UPSTREAM).open(encoding='utf-8', newline='') as handle:
        reader = csv.DictReader(handle); rows, fields = list(reader), tuple(reader.fieldnames or ())
    rows[0][field] = 'drift'
    target = tmp_path / module.UPSTREAM; target.parent.mkdir(parents=True)
    with target.open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator='\n'); writer.writeheader(); writer.writerows(rows)
    with pytest.raises(ValueError, match=rf'handoff drift: {field}'):
        module.build(tmp_path)


def test_re656_rejects_upstream_schema_and_row_count_drift(tmp_path):
    from scripts.reverse import re656_ghidra_second_window_rank_100_narrow_export as module
    target = tmp_path / module.UPSTREAM; target.parent.mkdir(parents=True)
    target.write_text('bad_schema\nvalue\n', encoding='utf-8')
    with pytest.raises(ValueError, match='handoff schema drift'):
        module.build(tmp_path)
    valid = (REPO / module.UPSTREAM).read_text(encoding='utf-8')
    target.write_text(valid + valid.splitlines()[1] + '\n', encoding='utf-8')
    with pytest.raises(ValueError, match='handoff row-count drift'):
        module.build(tmp_path)
