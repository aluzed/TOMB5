from pathlib import Path
import pytest
from scripts.reverse.re460_ghidra_second_window_next_candidate_selection import FORBIDDEN_OUTPUT_FRAGMENTS, build, write
REPO=Path(__file__).resolve().parents[2]
def test_re460_selects_rank_35_metadata_only(tmp_path):
 r=build(REPO)
 assert r['story_id']=='RE-460' and r['closed_candidate_id']=='aaf42cb3b10b'
 assert r['selected_rank']=='35' and r['selected_candidate_id']=='ede72eed0265'
 assert r['selected_bridge_class']=='mapped-caller-bridge'
 assert r['next_ticket']=='RE-461' and r['next_topic']=='ghidra-second-window-rank-35-narrow-export'
 assert r['code_change_readiness']=='blocked'
 for p in write(r,tmp_path): assert not any(x in p.read_text(encoding='utf-8').lower() for x in FORBIDDEN_OUTPUT_FRAGMENTS)
def test_re460_rejects_forbidden_output(tmp_path):
 with pytest.raises(ValueError,match='forbidden output fragment'): write(dict(build(REPO),stop_condition='copyrighted asset'),tmp_path)
