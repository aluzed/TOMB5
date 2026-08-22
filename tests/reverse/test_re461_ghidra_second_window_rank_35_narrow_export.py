from pathlib import Path
import pytest
from scripts.reverse.re461_ghidra_second_window_rank_35_narrow_export import FORBIDDEN_OUTPUT_FRAGMENTS, build, write
REPO=Path(__file__).resolve().parents[2]
def test_re461_narrows_rank_35_metadata_only(tmp_path):
 r=build(REPO)
 assert r['story_id']=='RE-461' and r['selected_candidate_id']=='ede72eed0265' and r['selected_rank']=='35'
 assert r['bridge_class']=='mapped-caller-bridge'
 assert r['next_ticket']=='RE-462' and r['next_topic']=='mapped-caller-bridge-readiness-gate'
 assert r['code_change_readiness']=='blocked' and r['source_patch_authorized_count']=='0'
 for p in write(r,tmp_path): assert not any(x in p.read_text(encoding='utf-8').lower() for x in FORBIDDEN_OUTPUT_FRAGMENTS)
def test_re461_rejects_forbidden_output(tmp_path):
 with pytest.raises(ValueError,match='forbidden output fragment'):write(dict(build(REPO),stop_condition='raw binary evidence'),tmp_path)
