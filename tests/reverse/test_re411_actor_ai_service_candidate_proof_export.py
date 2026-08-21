from pathlib import Path
from scripts.reverse.re411_actor_ai_service_candidate_proof_export import build,write
def test_re411_exports_actor_context():
 b=build(Path(__file__).resolve().parents[2]);assert b['selected_candidate_id']=='bcfb623df366';assert b['next_ticket']=='RE-412'
