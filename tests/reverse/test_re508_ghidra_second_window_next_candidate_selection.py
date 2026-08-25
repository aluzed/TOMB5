import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))


def test_re508_selects_rank_51_metadata_only(tmp_path):
    from scripts.reverse import re508_ghidra_second_window_next_candidate_selection as m

    row = m.build(REPO)
    assert (row['story_id'], row['selected_rank'], row['selected_candidate_id'], row['selected_bridge_class'], row['next_ticket'], row['code_change_readiness']) == ('RE-508', '51', '27952a832b99', 'mapped-caller-callee-bridge', 'RE-509', 'blocked')
    assert len(m.write(row, tmp_path)) == 5
