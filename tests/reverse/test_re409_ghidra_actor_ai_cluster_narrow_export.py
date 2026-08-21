from pathlib import Path
from scripts.reverse.re409_ghidra_actor_ai_cluster_narrow_export import build,write
def test_re409_selects_actor_ai():
 b=build(Path(__file__).resolve().parents[2]);assert b['selected_candidate_id']=='bcfb623df366';assert b['next_ticket']=='RE-410'
