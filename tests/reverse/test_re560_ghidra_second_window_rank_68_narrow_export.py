import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))


def test_re560_rank_68_narrow_export_is_metadata_only(tmp_path):
    from scripts.reverse import re560_ghidra_second_window_rank_68_narrow_export as module

    row = module.build(REPO)
    assert (
        row['story_id'], row['selected_rank'], row['selected_candidate_id'],
        row['bridge_class'], row['next_ticket'], row['code_change_readiness'],
    ) == ('RE-560', '68', 'b7ab26b5c07b', 'mapped-callee-bridge', 'RE-561', 'blocked')
    assert len(module.write(row, tmp_path)) == 5
