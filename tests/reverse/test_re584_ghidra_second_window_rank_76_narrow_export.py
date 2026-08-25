import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))


def test_re584_rank_76_narrow_export_is_metadata_only(tmp_path):
    from scripts.reverse import re584_ghidra_second_window_rank_76_narrow_export as module

    row = module.build(REPO)
    assert (row['story_id'], row['selected_rank'], row['selected_candidate_id'], row['candidate_level_proof_count'], row['next_ticket'], row['code_change_readiness']) == ('RE-584', '76', '8f7269b61897', '0', 'RE-585', 'blocked')
    assert len(module.write(row, tmp_path)) == 5
