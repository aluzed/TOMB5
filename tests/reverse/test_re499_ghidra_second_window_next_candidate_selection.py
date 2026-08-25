import sys
from pathlib import Path
REPO=Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:sys.path.insert(0,str(REPO))
def test_re499_selects_rank_48_metadata_only(tmp_path):
 from scripts.reverse import re499_ghidra_second_window_next_candidate_selection as m
 r=m.build(REPO)
 assert (r['story_id'],r['selected_rank'],r['selected_candidate_id'],r['selected_bridge_class'],r['next_ticket'],r['code_change_readiness'])==('RE-499','48','76692514f5b0','mapped-callee-bridge','RE-500','blocked')
 assert len(m.write(r,tmp_path))==5
