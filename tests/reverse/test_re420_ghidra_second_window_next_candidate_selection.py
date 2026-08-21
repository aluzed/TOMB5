from pathlib import Path
from scripts.reverse.re420_ghidra_second_window_next_candidate_selection import build,write
def test_re420_selects_rank_27():
 b=build(Path(__file__).resolve().parents[2]);assert b['selected_rank']=='27';assert b['selected_candidate_id']=='c2ed98ffa484';assert b['next_ticket']=='RE-421'
