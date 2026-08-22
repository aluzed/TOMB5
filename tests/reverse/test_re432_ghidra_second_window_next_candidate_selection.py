from pathlib import Path
from scripts.reverse.re432_ghidra_second_window_next_candidate_selection import build,write
def test_re432_selects_rank_29():
 b=build(Path(__file__).resolve().parents[2]);assert b['selected_rank']=='29';assert b['selected_candidate_id']=='763c9cd0e3f7';assert b['next_ticket']=='RE-433'
