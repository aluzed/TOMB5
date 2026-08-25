import sys
from pathlib import Path
REPO = Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path: sys.path.insert(0, str(REPO))

def test_re537_metadata_only_gate(tmp_path):
    from scripts.reverse import re537_mapped_callee_bridge_readiness_gate as m
    row=m.build(REPO)
    assert (row['story_id'],row['selected_rank'],row['selected_candidate_id'],row['source_backed_callsite_count'],row['next_ticket'],row['code_change_readiness'])==('RE-537','60','7bf1750a8ac1','0','RE-538','blocked')
    assert len(m.write(row,tmp_path))==5
