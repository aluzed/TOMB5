import sys
from pathlib import Path
REPO=Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:sys.path.insert(0,str(REPO))
def test_re501_metadata_only_gate(tmp_path):
 from scripts.reverse import re501_mapped_callee_bridge_readiness_gate as m
 r=m.build(REPO)
 assert (r['story_id'],r['selected_candidate_id'],r['selected_rank'],r['bridge_class'],r['next_ticket'],r['code_change_readiness'])==('RE-501','76692514f5b0','48','mapped-callee-bridge','RE-502','blocked')
 assert len(m.write(r,tmp_path))==5
