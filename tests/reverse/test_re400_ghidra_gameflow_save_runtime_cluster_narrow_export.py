from pathlib import Path
from scripts.reverse.re400_ghidra_gameflow_save_runtime_cluster_narrow_export import build,write
def test_re400_selects_first_candidate():
 b=build(Path(__file__).resolve().parents[2]);assert b['story_id']=='RE-400';assert b['selected_candidate_id']=='f7335a494e49';assert b['next_ticket']=='RE-401'
