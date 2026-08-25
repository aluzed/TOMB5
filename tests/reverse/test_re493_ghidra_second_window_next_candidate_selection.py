import sys
from pathlib import Path
import pytest
REPO=Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:sys.path.insert(0,str(REPO))
def test_re493_is_metadata_only_and_selects_rank_46(tmp_path):
 from scripts.reverse import re493_ghidra_second_window_next_candidate_selection as m
 r=m.build(REPO)
 assert (r['story_id'],r['selected_rank'],r['selected_candidate_id'],r['selected_bridge_class'],r['next_ticket'],r['code_change_readiness'])==('RE-493','46','8ac39f9a6a85','mapped-caller-callee-bridge','RE-494','blocked')
 for p in m.write(r,tmp_path):assert not any(x in p.read_text(encoding='utf-8').lower() for x in m.BAD)
def test_re493_rejects_candidate_drift(monkeypatch):
 from scripts.reverse import re493_ghidra_second_window_next_candidate_selection as m
 monkeypatch.setattr(m,'ranked',lambda _repo:None)
 with pytest.raises(ValueError,match='ranked candidate drift'):m.build(REPO)
