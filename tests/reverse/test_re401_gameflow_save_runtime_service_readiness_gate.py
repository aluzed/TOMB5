from pathlib import Path
from scripts.reverse.re401_gameflow_save_runtime_service_readiness_gate import build
def test_re401_blocks_without_proof():
 assert build(Path(__file__).resolve().parents[2])['next_ticket']=='RE-402'
