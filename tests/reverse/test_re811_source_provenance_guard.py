import hashlib,runpy
from pathlib import Path
import pytest
R=Path(__file__).resolve().parents[2]
G=runpy.run_path(str(R/'scripts/reverse/re811_provenance.py'))
def test_exact_inverse_and_all_unrelated_bytes():
 b=(R/'GAME/ITEMS.C').read_bytes()
 assert hashlib.sha256(G['baseline_from_approved_source'](b)).hexdigest()==G['BASELINE']
 for m in (b+b'\n',b.replace(b'#else',b'#else\n',1),b.replace(b'#endif',b'',1)):
  with pytest.raises(AssertionError):G['baseline_from_approved_source'](m)
def test_named_dashboard_successor_failclosed():
 b=(R/'docs/reverse/reconstruction-progress.html').read_bytes()
 assert hashlib.sha256(G['dashboard_before_re811'](b)).hexdigest()==G['PRECEDING']
 for m in (b+b'foreign',b.replace(b'RE-809',b'RE-xxx',1),b+b'<!-- start re811-removeactiveitem-integration --><!-- end re811-removeactiveitem-integration -->'):
  with pytest.raises(AssertionError):G['dashboard_before_re811'](m)
