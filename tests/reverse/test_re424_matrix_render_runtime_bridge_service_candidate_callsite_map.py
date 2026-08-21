from pathlib import Path
from scripts.reverse.re424_matrix_render_runtime_bridge_service_candidate_callsite_map import build,write
def test_re424_preserves_fail_closed_state():
 b=build(Path(__file__).resolve().parents[2]);assert b['next_ticket']=='RE-425';assert b['candidate_level_proof_count']=='0'
