from pathlib import Path
from scripts.reverse.re417_collision_runtime_bridge_service_candidate_proof_export import build,write
def test_re417_exports_metadata_only_context():
 b=build(Path(__file__).resolve().parents[2]);assert b['selected_candidate_id']=='9d570ef9a5a7';assert b['next_ticket']=='RE-418';assert b['candidate_level_proof_count']=='0'
