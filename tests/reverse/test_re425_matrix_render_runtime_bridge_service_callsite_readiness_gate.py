from pathlib import Path
from scripts.reverse.re425_matrix_render_runtime_bridge_service_callsite_readiness_gate import build,write
def test_re425_closes_rank_27():
 b=build(Path(__file__).resolve().parents[2]);assert b['next_ticket']=='RE-426';assert b['code_change_readiness']=='blocked'
