import csv
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))


def test_re585_readiness_gate_is_metadata_only(tmp_path):
    from scripts.reverse import re585_mapped_caller_callee_bridge_readiness_gate as module

    row = module.build(REPO)
    assert (
        row['story_id'], row['selected_rank'], row['selected_candidate_id'],
        row['source_backed_callsite_count'], row['next_ticket'], row['code_change_readiness'],
    ) == ('RE-585', '76', '8f7269b61897', '0', 'RE-586', 'blocked')
    outputs = module.write(row, tmp_path)
    assert len(outputs) == 5
    assert all('source patch' not in path.read_text(encoding='utf-8').lower() for path in outputs)


@pytest.mark.parametrize('field', (
    'story_id', 'topic', 'upstream_handoff', 'selected_candidate_id', 'selected_rank',
    'selected_subcluster', 'source_symbol_context_count', 'bridge_class',
    'safe_context_status', 'candidate_level_proof_count',
    'ready_to_reopen_domain_count', 'source_patch_authorized_count',
    'selected_domain', 'selected_pivot', 'next_ticket', 'next_topic',
    'metadata_work_readiness', 'code_change_readiness', 'stop_condition',
))
def test_re585_rejects_each_upstream_handoff_field_drift(tmp_path, field):
    from scripts.reverse import re585_mapped_caller_callee_bridge_readiness_gate as module

    upstream = REPO / module.UPSTREAM
    with upstream.open(encoding='utf-8', newline='') as handle:
        rows = list(csv.DictReader(handle))
        fields = tuple(csv.DictReader(upstream.open(encoding='utf-8', newline='')).fieldnames)
    rows[0][field] = 'drift'
    target = tmp_path / module.UPSTREAM
    target.parent.mkdir(parents=True)
    with target.open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
    with pytest.raises(ValueError, match='handoff drift'):
        module.build(tmp_path)


def test_re585_rejects_upstream_schema_and_row_count_drift(tmp_path):
    from scripts.reverse import re585_mapped_caller_callee_bridge_readiness_gate as module

    target = tmp_path / module.UPSTREAM
    target.parent.mkdir(parents=True)
    target.write_text('bad_schema\nvalue\n', encoding='utf-8')
    with pytest.raises(ValueError, match='handoff schema drift'):
        module.build(tmp_path)
