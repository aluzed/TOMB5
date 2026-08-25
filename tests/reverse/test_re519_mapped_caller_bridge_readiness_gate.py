import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))


def test_re519_rank_54_metadata_only_readiness_gate(tmp_path):
    from scripts.reverse import re519_mapped_caller_bridge_readiness_gate as m

    row = m.build(REPO)
    assert (
        row['story_id'], row['selected_candidate_id'], row['selected_rank'],
        row['bridge_class'], row['next_ticket'], row['code_change_readiness'],
    ) == ('RE-519', '65e0849a91c0', '54', 'mapped-caller-bridge', 'RE-520', 'blocked')
    assert len(m.write(row, tmp_path)) == 5
