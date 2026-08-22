"""RE-467 metadata-only rank-37 narrow export."""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))
from scripts.reverse.re462_re467_metadata_handoff import FORBIDDEN_OUTPUT_FRAGMENTS, build as _build, write as _write
TICKET = 'RE-467'
def build(repo): return _build(TICKET, Path(repo))
def write(result, repo): return _write(TICKET, result, Path(repo))
if __name__ == '__main__': write(build(ROOT), ROOT)
