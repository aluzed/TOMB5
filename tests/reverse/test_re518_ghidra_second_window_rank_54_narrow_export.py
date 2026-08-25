import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))


def test_re518_rank_54_metadata_only_export(tmp_path):
    from scripts.reverse import re518_ghidra_second_window_rank_54_narrow_export as m

    row = m.build(REPO)
    assert (row['story_id'], row['selected_candidate_id'], row['selected_rank'], row['bridge_class'], row['next_ticket'], row['code_change_readiness']) == ('RE-518', '65e0849a91c0', '54', 'mapped-caller-bridge', 'RE-519', 'blocked')
    assert len(m.write(row, tmp_path)) == 5
