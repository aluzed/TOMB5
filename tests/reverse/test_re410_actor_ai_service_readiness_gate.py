from pathlib import Path
from scripts.reverse.re410_actor_ai_service_readiness_gate import build,write
def test_re410_blocks_actor_ai():
 b=build(Path(__file__).resolve().parents[2]);assert b['next_ticket']=='RE-411';assert b['code_change_readiness']=='blocked'
