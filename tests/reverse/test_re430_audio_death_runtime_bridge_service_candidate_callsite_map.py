from pathlib import Path
from scripts.reverse.re430_audio_death_runtime_bridge_service_candidate_callsite_map import build,write
def test_re430_emits_blocked_callsite_map(tmp_path):
 b=build(Path(__file__).resolve().parents[2]);assert b['selected_candidate_id']=='61b63f61c1fd';assert b['source_backed_callsite_count']=='0';assert b['next_ticket']=='RE-431';assert write(b,tmp_path)
