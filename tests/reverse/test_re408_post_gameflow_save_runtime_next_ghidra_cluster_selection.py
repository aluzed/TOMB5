from pathlib import Path
from scripts.reverse.re408_post_gameflow_save_runtime_next_ghidra_cluster_selection import build,write
def test_re408_selects_actor_ai():
 b=build(Path(__file__).resolve().parents[2]);assert b['selected_followup_cluster']=='actor-ai-cluster';assert b['next_ticket']=='RE-409'
