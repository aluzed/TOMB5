import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))


def test_re541_rank_62_metadata_only_selection(tmp_path):
    from scripts.reverse import re541_ghidra_second_window_next_candidate_selection as m
    row = m.build(REPO)
    assert (row['story_id'], row['closed_candidate_id'], row['selected_rank'], row['selected_candidate_id'], row['selected_bridge_class'], row['next_ticket'], row['code_change_readiness']) == ('RE-541', '70f02d5b6c66', '62', '605d53c8fbfb', 'mapped-caller-callee-bridge', 'RE-542', 'blocked')
    assert len(m.write(row, tmp_path)) == 5
