import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))


def test_re546_mapped_caller_callee_bridge_readiness_gate_is_metadata_only(tmp_path):
    from scripts.reverse import re546_mapped_caller_callee_bridge_readiness_gate as m
    row = m.build(REPO)
    assert (row['story_id'], row['selected_rank'], row['selected_candidate_id'], row['source_backed_callsite_count'], row['next_ticket'], row['code_change_readiness']) == ('RE-546', '63', '0887abf727ec', '0', 'RE-547', 'blocked')
    assert len(m.write(row, tmp_path)) == 5
