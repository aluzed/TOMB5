from pathlib import Path
from scripts.reverse.re431_audio_death_runtime_bridge_service_callsite_readiness_gate import build,write
def test_re431_keeps_source_blocked(tmp_path):
 b=build(Path(__file__).resolve().parents[2]);assert b['code_change_readiness']=='blocked';assert b['next_ticket']=='RE-432';assert write(b,tmp_path)
