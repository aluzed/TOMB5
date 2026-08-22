from pathlib import Path
from scripts.reverse.re433_ghidra_second_window_rank_29_narrow_export import build,write
def test_re433_narrows_rank_29():
 b=build(Path(__file__).resolve().parents[2]);assert b['selected_candidate_id']=='763c9cd0e3f7';assert b['selected_rank']=='29';assert b['next_ticket']=='RE-434'
