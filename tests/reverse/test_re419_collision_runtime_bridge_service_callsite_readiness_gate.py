from pathlib import Path
from scripts.reverse.re419_collision_runtime_bridge_service_callsite_readiness_gate import build,write
def test_re419_closes_candidate():
 b=build(Path(__file__).resolve().parents[2]);assert b['next_ticket']=='RE-420';assert b['code_change_readiness']=='blocked'
