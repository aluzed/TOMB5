import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))


def test_re529_rank_58_metadata_only_selection(tmp_path):
    from scripts.reverse import re529_ghidra_second_window_next_candidate_selection as m

    row = m.build(REPO)
    assert (
        row['story_id'], row['closed_candidate_id'], row['selected_rank'],
        row['selected_candidate_id'], row['selected_bridge_class'], row['next_ticket'],
        row['code_change_readiness'],
    ) == ('RE-529', '326ddce9c64d', '58', '8671e20f3685', 'mapped-callee-bridge', 'RE-530', 'blocked')
    assert len(m.write(row, tmp_path)) == 5
