from pathlib import Path
from scripts.reverse.re406_gameflow_save_runtime_service_next_candidate_callsite_map import build,write
def test_re406_maps_deferred_candidate():
 b=build(Path(__file__).resolve().parents[2]);assert b['selected_candidate_id']=='64182b59acd1';assert b['next_ticket']=='RE-407'
