import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))


def test_re547_next_candidate_selection_is_metadata_only(tmp_path):
    from scripts.reverse import re547_ghidra_second_window_next_candidate_selection as m
    row = m.build(REPO)
    assert (row['story_id'], row['closed_candidate_id'], row['selected_rank'], row['selected_candidate_id'], row['next_ticket'], row['code_change_readiness']) == ('RE-547', '0887abf727ec', '64', '47d4d3877c3a', 'RE-548', 'blocked')
    assert len(m.write(row, tmp_path)) == 5
