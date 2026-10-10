from pathlib import Path
import hashlib
import pytest
R=Path(__file__).resolve().parents[2]
BEGIN=b'<!-- start re866-mroty-integration -->'
END=b'<!-- end re866-mroty-integration -->'
PIN='0088371094e5421e3f1365caa52df2c1e3059a0f9efe3da7639307ed3a6df4f1'
def historical(data):
 assert data.count(BEGIN)==data.count(END)==1
 first=data.index(BEGIN);last=data.index(END)+len(END)
 return data[:first]+data[last:]
def verify(data):
 assert hashlib.sha256(historical(data)).hexdigest()==PIN
@pytest.mark.parametrize('mutation',[b'drift',b'<!-- unknown successor -->'])
def test_unknown_delta_rejected(mutation):
 data=(R/'docs/reverse/reconstruction-progress.html').read_bytes()
 with pytest.raises(AssertionError):verify(data+mutation)
def test_story_and_dashboard():
 verify((R/'docs/reverse/reconstruction-progress.html').read_bytes())
 story=(R/'docs/stories/RE-866-mroty-integration.md').read_text()
 for text in ['36','608','ELF32','ELF64','RED','GREEN','rawGTE FAIL','integrationGetSpheres=false','D9','count<=0','independent finalreview pending','fpermissive']:
  assert text in story
 assert hashlib.sha256((R/'SPEC_PSXPC_N/MATHS.C').read_bytes()).hexdigest()=='59e70b260ae67d613e5fa74486c728a63bd3bb7ae4727537e293d4c057d9b7fa'
 assert hashlib.sha256((R/'SPEC_PSXPC_N/SPHERES.C').read_bytes()).hexdigest()=='b4bb87d16ab90d21b967781ccac31f6205951dfb58cac42023aac4617e9368c0'
 assert hashlib.sha256((R/'EMULATOR/LIBGTE.C').read_bytes()).hexdigest()=='dcd178e302e902e96588749afaf1460c708f4389adaf6b892e563677fb226419'
def test_historical_pins_retained():
 assert '0af3e5af6447f96207c619493f6c7c47139c18bac550e4567ccc631eaa7bd61f' in (R/'tests/reverse/test_re859_documentation.py').read_text()
 assert 'df360d7af4f4c5eb4f6382354e5afdfb2d581786263a24a09b29f50d17f96259' in (R/'tests/reverse/test_re862_documentation.py').read_text()
