import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))


def test_re553_next_candidate_selection_is_metadata_only(tmp_path):
    from scripts.reverse import re553_ghidra_second_window_next_candidate_selection as module

    row = module.build(REPO)
    assert (row['story_id'], row['closed_candidate_id'], row['selected_rank'], row['selected_candidate_id'], row['next_ticket'], row['code_change_readiness']) == ('RE-553', '75556f89b9cb', '66', '87acb47f89b8', 'RE-554', 'blocked')
    assert len(module.write(row, tmp_path)) == 5
