from pathlib import Path
from scripts.reverse.re423_matrix_render_runtime_bridge_service_candidate_proof_export import build,write
def test_re423_exports_metadata_only_context():
 b=build(Path(__file__).resolve().parents[2]);assert b['selected_candidate_id']=='c2ed98ffa484';assert b['next_ticket']=='RE-424';assert b['candidate_level_proof_count']=='0'
