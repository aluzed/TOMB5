from pathlib import Path
from scripts.reverse.re416_collision_runtime_bridge_service_readiness_gate import build,write
def test_re416_blocks_without_candidate_proof():
 b=build(Path(__file__).resolve().parents[2]);assert b['selected_candidate_id']=='9d570ef9a5a7';assert b['next_ticket']=='RE-417';assert b['code_change_readiness']=='blocked'
