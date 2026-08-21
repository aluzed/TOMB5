from pathlib import Path
from scripts.reverse.re422_matrix_render_runtime_bridge_service_readiness_gate import build,write
def test_re422_blocks_without_proof():
 b=build(Path(__file__).resolve().parents[2]);assert b['next_ticket']=='RE-423';assert b['code_change_readiness']=='blocked'
