"""Self-contained actual-TU regression: no skips or private target inputs."""
import runpy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def test_removeactiveitem_independent_full_buffer_oracle():
 out,rows=runpy.run_path(str(ROOT/'scripts/reverse/re811_removeactiveitem.py'))['run_contract']()
 for row in rows:
  assert row['exit']==0, str(out)+': '+row['stdout']+row['stderr']
  assert 'SUMMARY cases=106 failures=0' in row['stdout']
  assert row['stderr']==''
