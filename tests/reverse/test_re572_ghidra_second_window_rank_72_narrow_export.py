import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))


def test_re572_rank_72_narrow_export_is_metadata_only(tmp_path):
    from scripts.reverse import re572_ghidra_second_window_rank_72_narrow_export as module

    row = module.build(REPO)
    assert (
        row['story_id'], row['selected_rank'], row['selected_candidate_id'],
        row['selected_subcluster'], row['next_ticket'], row['code_change_readiness'],
    ) == ('RE-572', '72', '572021621f90', 'mapped-caller-bridge-readiness-gate', 'RE-573', 'blocked')
    assert len(module.write(row, tmp_path)) == 5
