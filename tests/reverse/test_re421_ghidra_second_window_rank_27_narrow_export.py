from pathlib import Path
from scripts.reverse.re421_ghidra_second_window_rank_27_narrow_export import build,write
def test_re421_selects_matrix_runtime_bridge():
 b=build(Path(__file__).resolve().parents[2]);assert b['selected_candidate_id']=='c2ed98ffa484';assert b['next_ticket']=='RE-422'
