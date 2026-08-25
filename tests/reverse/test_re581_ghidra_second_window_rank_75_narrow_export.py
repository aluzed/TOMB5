import sys
from pathlib import Path
REPO = Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path: sys.path.insert(0, str(REPO))

def test_re581_rank_75_narrow_export_is_metadata_only(tmp_path):
    from scripts.reverse import re581_ghidra_second_window_rank_75_narrow_export as module
    row = module.build(REPO)
    assert (row['story_id'],row['selected_rank'],row['selected_candidate_id'],row['candidate_level_proof_count'],row['next_ticket'],row['code_change_readiness']) == ('RE-581','75','792bbf9b7b74','0','RE-582','blocked')
    assert len(module.write(row,tmp_path)) == 5
