import sys
from pathlib import Path
import pytest
REPO=Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:sys.path.insert(0,str(REPO))
def test_re496_selects_rank_47_metadata_only(tmp_path):
 from scripts.reverse import re496_ghidra_second_window_next_candidate_selection as m
 r=m.build(REPO)
 assert (r['story_id'],r['selected_rank'],r['selected_candidate_id'],r['selected_bridge_class'],r['next_ticket'],r['code_change_readiness'])==('RE-496','47','afcb272bc095','mapped-caller-callee-bridge','RE-497','blocked')
 assert len(m.write(r,tmp_path))==5
