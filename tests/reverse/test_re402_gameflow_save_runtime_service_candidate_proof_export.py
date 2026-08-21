from pathlib import Path
from scripts.reverse.re402_gameflow_save_runtime_service_candidate_proof_export import build,write
def test_re402_exports_blocked_context():
 b=build(Path(__file__).resolve().parents[2]);assert b['story_id']=='RE-402';assert b['selected_candidate_id']=='f7335a494e49';assert b['next_ticket']=='RE-403'
