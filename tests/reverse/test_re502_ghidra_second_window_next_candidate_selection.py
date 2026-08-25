import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))


def test_re502_selects_rank_49_metadata_only(tmp_path):
    from scripts.reverse import re502_ghidra_second_window_next_candidate_selection as module

    row = module.build(REPO)
    assert (
        row['story_id'], row['selected_rank'], row['selected_candidate_id'],
        row['selected_bridge_class'], row['next_ticket'], row['code_change_readiness'],
    ) == ('RE-502', '49', 'a6117c5f5023', 'mapped-callee-bridge', 'RE-503', 'blocked')
    assert len(module.write(row, tmp_path)) == 5
