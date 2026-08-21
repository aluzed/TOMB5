from pathlib import Path
from scripts.reverse.re414_ghidra_bridge_candidate_second_window_selection import build,write
def test_re414_selects_unprocessed_rank_26():
 b=build(Path(__file__).resolve().parents[2]);assert b['selected_rank']=='26';assert b['next_ticket']=='RE-415';assert b['selected_candidate_id']
