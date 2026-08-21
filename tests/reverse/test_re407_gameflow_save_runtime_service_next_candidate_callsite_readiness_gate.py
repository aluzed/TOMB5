from pathlib import Path
from scripts.reverse.re407_gameflow_save_runtime_service_next_candidate_callsite_readiness_gate import build,write
def test_re407_closes_queue():
 b=build(Path(__file__).resolve().parents[2]);assert b['next_ticket']=='RE-408';assert b['code_change_readiness']=='blocked'
