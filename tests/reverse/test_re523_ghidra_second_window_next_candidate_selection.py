import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))


def test_re523_selects_rank_56_metadata_only_candidate(tmp_path):
    from scripts.reverse import re523_ghidra_second_window_next_candidate_selection as m

    row = m.build(REPO)
    assert (
        row['story_id'], row['closed_candidate_id'], row['selected_rank'],
        row['selected_candidate_id'], row['selected_bridge_class'], row['next_ticket'],
        row['code_change_readiness'],
    ) == ('RE-523', 'c126657cee24', '56', '9f1d49236ff5', 'mapped-callee-bridge', 'RE-524', 'blocked')
    assert len(m.write(row, tmp_path)) == 5
