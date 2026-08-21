from pathlib import Path
from scripts.reverse.re404_gameflow_save_runtime_service_callsite_readiness_gate import build,write
def test_re404_closes_candidate_without_proof():
 b=build(Path(__file__).resolve().parents[2]);assert b['story_id']=='RE-404';assert b['next_ticket']=='RE-405';assert b['code_change_readiness']=='blocked'
