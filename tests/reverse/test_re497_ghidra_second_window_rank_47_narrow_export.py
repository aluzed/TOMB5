import sys
from pathlib import Path
REPO=Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:sys.path.insert(0,str(REPO))
def test_re497_metadata_only_export(tmp_path):
 from scripts.reverse import re497_ghidra_second_window_rank_47_narrow_export as m
 r=m.build(REPO)
 assert (r['story_id'],r['selected_candidate_id'],r['selected_rank'],r['bridge_class'],r['next_ticket'],r['code_change_readiness'])==('RE-497','afcb272bc095','47','mapped-caller-callee-bridge','RE-498','blocked')
 assert len(m.write(r,tmp_path))==5
