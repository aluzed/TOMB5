import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))


def test_re563_rank_69_narrow_export_is_metadata_only(tmp_path):
    from scripts.reverse import re563_ghidra_second_window_rank_69_narrow_export as module

    row = module.build(REPO)
    assert (
        row['story_id'], row['selected_rank'], row['selected_candidate_id'],
        row['bridge_class'], row['next_ticket'], row['code_change_readiness'],
    ) == ('RE-563', '69', 'e5b9063e77db', 'mapped-caller-callee-bridge', 'RE-564', 'blocked')
    assert len(module.write(row, tmp_path)) == 5
