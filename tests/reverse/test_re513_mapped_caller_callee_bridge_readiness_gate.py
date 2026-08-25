import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))


def test_re513_metadata_only_gate(tmp_path):
    from scripts.reverse import re513_mapped_caller_callee_bridge_readiness_gate as m

    row = m.build(REPO)
    assert (row['story_id'], row['selected_candidate_id'], row['selected_rank'], row['bridge_class'], row['next_ticket'], row['code_change_readiness']) == ('RE-513', 'bee4d7de442c', '52', 'mapped-caller-callee-bridge', 'RE-514', 'blocked')
    assert len(m.write(row, tmp_path)) == 5
