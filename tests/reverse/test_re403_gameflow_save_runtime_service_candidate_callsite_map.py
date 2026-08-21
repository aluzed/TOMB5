from pathlib import Path
from scripts.reverse.re403_gameflow_save_runtime_service_candidate_callsite_map import build,write
def test_re403_blocks_patch():
 b=build(Path(__file__).resolve().parents[2]);assert b['story_id']=='RE-403';assert b['candidate_level_proof_count']=='0';assert b['next_ticket']=='RE-404'
