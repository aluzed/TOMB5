import importlib.util,json,copy
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[2]
def api():
 p=ROOT/'scripts/reverse/re904_publication.py';assert p.exists(),'RED: RE904 metadata generator absent'
 s=importlib.util.spec_from_file_location('re904',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def test_contract():
 m=api();d=m.metadata();assert m.validate(d)==d
 assert d['integration'] is False and d['global_scope']==d['procedure_scope']=='FAIL'
 assert d['fresh_target']==d['fresh_native']==0 and d['publication_review']=='PENDING_INDEPENDENT_EXACT_HASH_REVIEW'
 a,b=d['archived_private_results'];assert a['ticket']=='RE902' and b['ticket']=='RE903'
 assert a['native']==dict(attempts=36,returns=24,aborts=12,raw_mismatches=24,position_mismatches=0)
 assert b['producer_accepted']==dict(target=9,cpu=9,math=9,native_attempts=291,native_returns=253,native_aborts=38,probes=3)
 assert b['producer_roots_total']==dict(target=18,native_attempts=546,native_returns=482,native_aborts=64)
 assert b['reviewer']==dict(target=9,cpu=9,math=9,native_attempts=288,native_returns=252,native_aborts=36)
 assert b['static_annex']['new_native']==0
@pytest.mark.parametrize('change',['unknown','boolint','countbool','attempts','returns','aborts','total','review','candidate','global','static'])
def test_schema_mutants(change):
 m=api();d=m.metadata();b=d['archived_private_results'][1];before=copy.deepcopy(d)
 if change=='unknown':d['unknown']=1
 if change=='boolint':d['integration']=0
 if change=='countbool':d['fresh_native']=False
 if change in ('attempts','returns','aborts'):b['producer_accepted']['native_'+change]+=1
 if change=='total':b['producer_roots_total']['native_attempts']=291
 if change=='review':d['publication_review']='PASS'
 if change=='candidate':b['candidate_sha256']='0'*64
 if change=='global':d['global_scope']='PASS'
 if change=='static':b['static_annex']['new_native']=32
 assert repr(d)!=repr(before)
 with pytest.raises(ValueError):m.validate(d)
def test_fixtures():
 m=api();out=m.render();assert set(out)==set(m.OUTPUT_PATHS)
 for p,b in out.items():assert (ROOT/p).read_bytes()==b;m.guard_output(p,b)
 assert m.preceding_dashboard(out[m.DASHBOARD])==(ROOT/m.PRIOR_DASHBOARD).read_bytes()
 assert m.preceding_maintained(out[m.MAINTAINED])==(ROOT/m.PRIOR_MAINTAINED).read_bytes()
 m.check()
@pytest.mark.parametrize('which',['dashboard','maintained'])
@pytest.mark.parametrize('change',['history','missing','duplicate','altered','trailing','unknown'])
def test_inverse_mutants(which,change):
 m=api();data=m.render()[m.DASHBOARD if which=='dashboard' else m.MAINTAINED];original=data;s=m.SECTION.encode()
 if change=='history':data=b'foreign'+data
 if change=='missing':data=data.replace(b'<!-- RE904 PUBLICATION END -->',b'')
 if change=='duplicate':data=data[:-7]+s+b'</html>'
 if change=='altered':data=data.replace(s,s.replace(b'ARCHIVED',b'FRESH'))
 if change=='trailing':data+=b'foreign'
 if change=='unknown':data=data[:-7]+b'<!-- unknown successor -->'+b'</html>'
 assert data!=original
 with pytest.raises(ValueError):(m.preceding_dashboard if which=='dashboard' else m.preceding_maintained)(data)
@pytest.mark.parametrize('bad',[b'0x80012345',b'FUN_80012345',b'word_le_hex',b'raw_opcode',b'payload_offset',b'data:image/png;base64,',b'-----BEGIN '+b'PRIVATE KEY-----',b'ghp_'+b'a'*30,b'```mips\n',b'\0',b'raw_pc=123',b'register_values=[1]',b'target_address=123',b'a'*100001])
def test_content_guard(bad):
 m=api();m.guard_added(m.STORY,b'safe symbolic metadata')
 with pytest.raises(ValueError):m.guard_added(m.STORY,bad)
@pytest.mark.parametrize('p',['SPEC_PSXPC_N/MATHS.C','build/reverse/proof.bin','assets/x.png','../escape.md','/tmp/x'])
def test_path_guard(p):
 with pytest.raises(ValueError):api().guard_added(p,b'safe metadata')
def test_documents():
 m=api();out=m.render()
 for p in (m.STORY,m.REPORT):
  for phrase in ['## Progression','## Evidence','## Blockers','## Acceptance','PENDING_INDEPENDENT_EXACT_HASH_REVIEW','integration=false','RE902','RE903','firstFAIL','BLOCKED-001/002']:
   assert phrase in out[p].decode()
def test_compatibility():api().compatibility_pins()
