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
RE830_TEST819_DELTAS = [('def test_append_only_dashboard_blocker_and_exact_inverse_code():\n', "def blocker_before_re830(data):\n # Only the exact authenticated RE830 successor is reversible; no generic append.\n if b'## RE830' in data:\n  contract=runpy.run_path(str(R/'tests/reverse/test_re830_table_provenance_publication.py'))\n  before=contract['preceding_blocker'](data)\n  assert H(before)=='a9c5a04d69c030a8e8c47915a345223e44a32eecadaa5c6cd5f7d20e8bbb4a59'\n  return before\n assert H(data)=='a9c5a04d69c030a8e8c47915a345223e44a32eecadaa5c6cd5f7d20e8bbb4a59', 'RE830 successor malformed or history altered'\n return data\ndef test_append_only_dashboard_blocker_and_exact_inverse_code():\n"), (" c=(R/g['BLOCKER_PATH']).read_bytes();append=g['BLOCKER_APPEND'].encode()\n", " c=blocker_before_re830((R/g['BLOCKER_PATH']).read_bytes());append=g['BLOCKER_APPEND'].encode()\n"), ('', "\n@pytest.mark.parametrize('mutation', ['foreign', 'duplicate', 'altered', 'missing', 'history', 'unknown'])\ndef test_re830_blocker_successor_fail_closed(mutation):\n contract=runpy.run_path(str(R/'tests/reverse/test_re830_table_provenance_publication.py'))\n data=(R/contract['BLOCKER']).read_bytes(); addition=contract['APPEND'].encode()\n assert blocker_before_re830(data)==contract['preceding_blocker'](data)\n mutants={'foreign':data+b'foreign','duplicate':data+addition,'altered':data.replace(addition,addition.replace(b'620',b'621')),'missing':data.replace(b'## RE830',b'## RE83X'),'history':b'foreign'+data,'unknown':data+b'\\n## RE831\\nunknown\\n'}\n with pytest.raises(AssertionError):blocker_before_re830(mutants[mutation])\n")]

def original_test819_before_re830(text):
 # Reverse ONLY the approved successor adaptation; original RE820 hash stays pinned.
 for old,new in reversed(RE830_TEST819_DELTAS):
  assert text.count(new)==1, 'RE830 test819 delta absent, duplicated or altered'
  text=text.replace(new,old,1)
 return text

def test_exact_append_inverse_and_mutants():
 g=api();b=(R/'docs/reverse/reconstruction-progress.html').read_bytes()
 assert H(g['dashboard_before_re820'](b))==g['PRECEDING']
 for m in [b+b'foreign',b+g['SECTION'].encode(),b.replace(b'RE-820',b'RE-xxx'),b.replace(b'RE-809',b'RE-xxx')]:
  with pytest.raises(AssertionError):g['dashboard_before_re820'](m)
 for p,h in g['OLD'].items():
  text=(R/p).read_text()
  if p=='tests/reverse/test_re819_publication.py':text=original_test819_before_re830(text)
  assert H(g['inverse_code'](text,p).encode())==h
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
