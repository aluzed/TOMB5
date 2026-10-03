"""RE820 portable metadata publication; never target execution."""
import csv,hashlib,io,json,re,runpy
from pathlib import Path
import pytest
R=Path(__file__).resolve().parents[2]
H=lambda b:hashlib.sha256(b).hexdigest()
def api():
 p=R/'scripts/reverse/re820_publication.py'
 assert p.exists(),'RED: RE820 metadata generator absent'
 return runpy.run_path(str(p))
def test_finite_domain_and_denied_approval():
 g=api();d=g['metadata']()
 assert d['angles']==[0,-32768,16384,-16384,1]
 assert d['selected_cells']==[11,13,7,17,17]
 assert d['native_cases']==10 and d['target_cases']==5
 assert d['private_review']=='PENDING_INDEPENDENT_REVIEW'
 assert d['portal_present'] is False and d['flip_present'] is False
 assert d['caller']=='direct private initializer; not InitialiseItem composition'
 for k in ['integration_approved','production_patch','new_caller_proven','natural_startup_proven','gameplay_proven','general_domain_proven','publication_review_approved']:
  assert d[k] is False
 for k,v in d.items():
  with pytest.raises(ValueError):g['validate']({**d,k:None})
 with pytest.raises(ValueError):g['validate']({**d,'raw':'forbidden'})
def test_real_behavioral_red_is_not_sigill():
 d=api()['metadata']()
 assert d['domain_refusal_exit']==-4 and d['behavioral_mutant_contract_exit']==1
 assert d['behavioral_mutant_execution_exit']==0
 assert d['mutant_different_bytes']==[11,11]
 assert d['projection_bytes']==2980 and d['whole_native_buffer_bytes']==1088324
 assert d['events']==['allocation','GetDoor','GetDoor','ShutThatDoor','ShutThatDoor']
def test_generated_metadata_and_safety():
 g=api()
 for p,k in g['OUTPUTS'].items():
  text=(R/p).read_text();assert text==g[k]
  assert not re.search(r'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}|payload_offset|word_le_hex|data:image|```(?:asm|mips|cpp|c)\b',text)
 assert json.loads(g['PROOF_JSON'])==g['metadata']()
 assert len(list(csv.DictReader(io.StringIO(g['CSV_TEXT']))))==1
 assert '- [x]' in g['STORY'] and '- [ ]' in g['STORY']
 assert 'pending independent review' in g['STORY']
def test_exact_append_inverse_and_mutants():
 g=api();b=(R/'docs/reverse/reconstruction-progress.html').read_bytes()
 assert H(g['dashboard_before_re820'](b))==g['PRECEDING']
 for m in [b+b'foreign',b+g['SECTION'].encode(),b.replace(b'RE-820',b'RE-xxx'),b.replace(b'RE-809',b'RE-xxx')]:
  with pytest.raises(AssertionError):g['dashboard_before_re820'](m)
 for p,h in g['OLD'].items():assert H(g['inverse_code']((R/p).read_text(),p).encode())==h
 for p in g['OLD']:
  if p.startswith('scripts/'):
   old=runpy.run_path(str(R/p));fn=old['dashboard_before_'+Path(p).name[:5]]
   assert H(fn(b))==old['PRECEDING']
   with pytest.raises(AssertionError):fn(b+b'foreign')
def test_private_pins_and_forgery_rejection(tmp_path):
 g=api();fn=g['consume_producer'];fn.__globals__['ROOT']=tmp_path
 p=tmp_path/'build/reverse/autonomy-20261003/re820-sensitive-domain';p.mkdir(parents=True)
 for n in g['PRIVATE_PINS']:(p/n).write_text('{}\n')
 with pytest.raises(AssertionError):fn()
