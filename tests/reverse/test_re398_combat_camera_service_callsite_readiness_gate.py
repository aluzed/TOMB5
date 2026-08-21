from pathlib import Path
from scripts.reverse.re398_combat_camera_service_callsite_readiness_gate import build_combat_camera_service_callsite_readiness_gate,write_all_artifacts
def test_re398_keeps_readiness_blocked():
 b=build_combat_camera_service_callsite_readiness_gate(Path(__file__).resolve().parents[2]); assert b.summary.story_id=='RE-398';assert b.summary.candidate_level_proof_count==0;assert b.summary.next_ticket=='TBD';assert b.summary.code_change_readiness=='blocked'
def test_re398_writes(tmp_path):
 assert write_all_artifacts(build_combat_camera_service_callsite_readiness_gate(Path(__file__).resolve().parents[2]),tmp_path)
