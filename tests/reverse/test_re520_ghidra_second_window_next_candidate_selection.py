import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))


def test_re520_selects_rank_55_metadata_only_candidate(tmp_path):
    from scripts.reverse import re520_ghidra_second_window_next_candidate_selection as m

    row = m.build(REPO)
    assert (
        row['story_id'], row['closed_candidate_id'], row['selected_rank'],
        row['selected_candidate_id'], row['selected_bridge_class'], row['next_ticket'],
        row['code_change_readiness'],
    ) == ('RE-520', '65e0849a91c0', '55', 'c126657cee24', 'mapped-callee-bridge', 'RE-521', 'blocked')
    assert len(m.write(row, tmp_path)) == 5
