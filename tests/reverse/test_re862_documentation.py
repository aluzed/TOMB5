from pathlib import Path
import hashlib
import pytest
R=Path(__file__).resolve().parents[2]
PIN="df360d7af4f4c5eb4f6382354e5afdfb2d581786263a24a09b29f50d17f96259"
BEGIN=b'<!-- start re862-mrotz-mvmva-defined -->'
END=b'<!-- end re862-mrotz-mvmva-defined -->'
def historical(data):
 # Only named RE866 successor excluded; predecessor digest unchanged.
 nb=b'<!-- start re866-mroty-integration -->';ne=b'<!-- end re866-mroty-integration -->'
 if nb in data or ne in data:
  assert data.count(nb)==data.count(ne)==1
  data=data[:data.index(nb)]+data[data.index(ne)+len(ne):]
 assert data.count(BEGIN)==data.count(END)==1
 first=data.index(BEGIN);last=data.index(END)+len(END)
 return data[:first]+data[last:]
def verify(data):
 assert hashlib.sha256(historical(data)).hexdigest()==PIN
def test_append_only_and_story():
 verify((R/'docs/reverse/reconstruction-progress.html').read_bytes())
 story=(R/'docs/stories/RE-862-mrotz-mvmva-defined.md').read_text()
 for text in ['RE858 global FAIL','revue independante PASS scoped enregistree','synthetique','cv=2','mx=3','fpermissive','ELF32','ELF64','60','36','RED','GREEN']:
  assert text in story
@pytest.mark.parametrize('mutation',[b'<!-- unknown future section -->',b'drift'])
def test_no_future_or_drift_exception(mutation):
 data=(R/'docs/reverse/reconstruction-progress.html').read_bytes()
 with pytest.raises(AssertionError):verify(data+mutation)
def test_predecessor_pin_unchanged():
 s=(R/'tests/reverse/test_re859_documentation.py').read_text()
 assert '0af3e5af6447f96207c619493f6c7c47139c18bac550e4567ccc631eaa7bd61f' in s
 assert s.count('re862-mrotz-mvmva-defined')==2
