from pathlib import Path
from scripts.reverse.re413_actor_ai_service_callsite_readiness_gate import build,write
def test_re413_closes_actor_ai():
 b=build(Path(__file__).resolve().parents[2]);assert b['next_ticket']=='TBD';assert b['code_change_readiness']=='blocked'
