import sys
from pathlib import Path
REPO=Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:sys.path.insert(0,str(REPO))
def test_re506_metadata_only_export(tmp_path):
 from scripts.reverse import re506_ghidra_second_window_rank_50_narrow_export as m
 row=m.build(REPO)
 assert (row['story_id'],row['selected_candidate_id'],row['selected_rank'],row['bridge_class'],row['next_ticket'],row['code_change_readiness'])==('RE-506','bdb92ce23200','50','mapped-caller-callee-bridge','RE-507','blocked')
 assert len(m.write(row,tmp_path))==5
