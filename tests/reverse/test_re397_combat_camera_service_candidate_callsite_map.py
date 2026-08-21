from pathlib import Path
from scripts.reverse.re397_combat_camera_service_candidate_callsite_map import build_combat_camera_service_candidate_callsite_map, write_all_artifacts

def test_re397_maps_source_backed_callsites_without_authorizing_patch():
 b=build_combat_camera_service_candidate_callsite_map(Path(__file__).resolve().parents[2])
 assert b.summary.story_id=='RE-397'
 assert b.summary.selected_candidate_id=='0aaa76206517'
 assert b.summary.source_context_function_count==17
 assert b.summary.source_backed_callsite_count>0
 assert b.summary.candidate_level_proof_count==0
 assert b.summary.next_ticket=='RE-398'
 assert b.summary.code_change_readiness=='blocked'

def test_re397_writes_artifacts(tmp_path):
 b=build_combat_camera_service_candidate_callsite_map(Path(__file__).resolve().parents[2]); out=write_all_artifacts(b,tmp_path)
 assert {'functions_csv','callsites_csv','gate_csv','summary_csv','handoff_csv','md','story'}==set(out)
