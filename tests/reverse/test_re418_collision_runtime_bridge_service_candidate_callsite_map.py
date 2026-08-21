from pathlib import Path
from scripts.reverse.re418_collision_runtime_bridge_service_candidate_callsite_map import build,write
def test_re418_preserves_fail_closed_readiness():
 b=build(Path(__file__).resolve().parents[2]);assert b['selected_candidate_id']=='9d570ef9a5a7';assert b['next_ticket']=='RE-419';assert b['candidate_level_proof_count']=='0'
