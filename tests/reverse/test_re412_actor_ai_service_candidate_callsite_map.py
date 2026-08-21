from pathlib import Path
from scripts.reverse.re412_actor_ai_service_candidate_callsite_map import build,write
def test_re412_maps_actor_ai():
 b=build(Path(__file__).resolve().parents[2]);assert b['next_ticket']=='RE-413';assert b['code_change_readiness']=='blocked'
