from pathlib import Path
from scripts.reverse.re426_ghidra_second_window_next_candidate_selection import build,write
def test_re426_selects_rank_28_without_raw_context():
 b=build(Path(__file__).resolve().parents[2]);assert b['selected_rank']=='28';assert b['selected_candidate_id']=='61b63f61c1fd';assert b['next_ticket']=='RE-427'
