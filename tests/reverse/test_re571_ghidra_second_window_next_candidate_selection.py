import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))


def test_re571_candidate_selection_is_metadata_only(tmp_path):
    from scripts.reverse import re571_ghidra_second_window_next_candidate_selection as module

    row = module.build(REPO)
    assert (
        row['story_id'], row['selected_rank'], row['selected_candidate_id'],
        row['selected_bridge_class'], row['next_ticket'], row['code_change_readiness'],
    ) == ('RE-571', '72', '572021621f90', 'mapped-caller-bridge', 'RE-572', 'blocked')
    assert len(module.write(row, tmp_path)) == 5
