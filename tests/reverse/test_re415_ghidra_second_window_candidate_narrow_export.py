from pathlib import Path
from scripts.reverse.re415_ghidra_second_window_candidate_narrow_export import build,write
def test_re415_selects_collision_runtime_bridge():
 b=build(Path(__file__).resolve().parents[2]);assert b['selected_candidate_id']=='9d570ef9a5a7';assert b['selected_subcluster']=='collision-runtime-bridge-service';assert b['next_ticket']=='RE-416'
