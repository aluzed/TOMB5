import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))


def test_re525_rank_56_metadata_only_readiness_gate(tmp_path):
    from scripts.reverse import re525_mapped_callee_bridge_readiness_gate as m

    row = m.build(REPO)
    assert (
        row['story_id'], row['selected_candidate_id'], row['selected_rank'],
        row['bridge_class'], row['next_ticket'], row['code_change_readiness'],
    ) == ('RE-525', '9f1d49236ff5', '56', 'mapped-callee-bridge', 'RE-526', 'blocked')
    assert len(m.write(row, tmp_path)) == 5
