from pathlib import Path
from scripts.reverse.re399_post_lara_combat_camera_next_ghidra_cluster_selection import build,write
def test_re399_selects_gameflow():
 b=build(Path(__file__).resolve().parents[2]);assert b['selected_followup_cluster']=='gameflow-save-runtime-cluster';assert b['next_ticket']=='RE-400';assert b['code_change_readiness']=='blocked'
