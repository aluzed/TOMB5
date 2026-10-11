"""RE901 metadata-only discriminating schema, history and delivery contract."""
import importlib.util,json
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[2]
def api():
 p=ROOT/'scripts/reverse/re901_publication.py'
 assert p.exists(),'RED: RE901 public metadata generator absent'
 s=importlib.util.spec_from_file_location('re901',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def test_contract():
 m=api();d=m.metadata();assert m.validate(d)==d
 assert d['integration'] is False and d['production_patch'] is False
 assert d['publication_review']=='PENDING_INDEPENDENT_EXACT_HASH_REVIEW'
 assert d['fresh_target']==d['fresh_native']==0
 a,b=d['archived_private_results'];assert [a['ticket'],b['ticket']]==['RE899','RE900']
 assert a['historical_schema_accepted'] is False and a['fullraw_verdict']=='FAIL' and a['strict_verdict']=='FAIL'
 assert a['reviewer_debugger']==7 and a['producer']['native']==36
 assert b['producer']['native']==255 and b['reviewer_accepted']['native']==252
 assert b['candidate_matrix']==dict(attempts=36,returns=36,raw_available=36)
 assert b['producer_roots_total']==dict(target=27,native=585)
 assert b['width_annex']==dict(static_bodies=16,writer_checks=32,new_native=0)
 assert d['global_scope']=='FAIL' and d['procedure_scope']=='FAIL'
 assert 'natural' in d['limits'] and 'dual' in d['limits']

@pytest.mark.parametrize('change',['unknown','boolint','countbool','producer','reviewer','hash','approval','historical','matrix','annex','global','frontier'])
def test_schema_mutants(change):
 m=api();d=m.metadata();a,b=d['archived_private_results']
 if change=='unknown':b['unknown']=1
 if change=='boolint':d['integration']=0
 if change=='countbool':d['fresh_native']=False
 if change=='producer':b['producer']['native']=252
 if change=='reviewer':b['reviewer_accepted']['native']=255
 if change=='hash':b['candidate_sha256']='0'*64
 if change=='approval':d['publication_review']='PASS'
 if change=='historical':a['historical_schema_accepted']=True
 if change=='matrix':b['candidate_matrix']['returns']=24
 if change=='annex':b['width_annex']['new_native']=32
 if change=='global':d['global_scope']='PASS'
 if change=='frontier':d['next_ticket']='RE900'
 with pytest.raises(ValueError):m.validate(d)

def test_fixtures():
 m=api();out=m.render((ROOT/m.PRIOR_DASHBOARD).read_bytes());assert set(out)==set(m.OUTPUT_PATHS)
 assert out==m.render((ROOT/m.PRIOR_DASHBOARD).read_bytes())
 for p,b in out.items():assert (ROOT/p).read_bytes()==b;m.guard_output(p,b)
 assert m.preceding_dashboard(out[m.DASHBOARD])==(ROOT/m.PRIOR_DASHBOARD).read_bytes()
 assert m.preceding_maintained(out[m.MAINTAINED])==(ROOT/m.PRIOR_MAINTAINED).read_bytes()
 assert json.loads(out[m.JSON_PATH])==m.metadata();m.check()

@pytest.mark.parametrize('which',['dashboard','maintained'])
@pytest.mark.parametrize('change',['history','missing','duplicate','altered','trailing','unknown'])
def test_inverse_mutants(which,change):
 m=api();out=m.render((ROOT/m.PRIOR_DASHBOARD).read_bytes());data=out[m.DASHBOARD if which=='dashboard' else m.MAINTAINED];s=m.SECTION.encode()
 if change=='history':data=b'foreign'+data
 if change=='missing':data=data.replace(b'<!-- RE901 PUBLICATION END -->',b'')
 if change=='duplicate':data=data[:-7]+s+b'</html>'
 if change=='altered':data=data.replace(s,s.replace(b'ARCHIVED',b'FRESH'))
 if change=='trailing':data+=b'foreign'
 if change=='unknown':data=data[:-7]+b'<!-- unknown -->'+b'</html>'
 with pytest.raises(ValueError):(m.preceding_dashboard if which=='dashboard' else m.preceding_maintained)(data)

@pytest.mark.parametrize('bad',[b'0x80012345',b'FUN_80012345',b'word_le_hex',b'raw_opcode',b'payload_offset',b'data:image/png;base64,',b'-----BEGIN '+b'PRIVATE KEY-----',b'ghp_'+b'a'*30,b'```mips\n',b'\0',b'raw_pc=123',b'register_values=[1]',b'target_address=123',b'a'*100001])
def test_content_guard(bad):
 m=api();m.guard_added(m.STORY,b'safe symbolic metadata')
 with pytest.raises(ValueError):m.guard_added(m.STORY,bad)

@pytest.mark.parametrize('p',['SPEC_PSXPC_N/MATHS.C','build/reverse/proof.bin','assets/x.png','../escape.md','/tmp/x'])
def test_path_guard(p):
 with pytest.raises(ValueError):api().guard_added(p,b'safe metadata')

def test_documents():
 m=api();out=m.render((ROOT/m.PRIOR_DASHBOARD).read_bytes())
 for p in (m.STORY,m.REPORT):
  for phrase in ['## Progression','## Evidence','## Blockers','## Acceptance','PENDING_INDEPENDENT_EXACT_HASH_REVIEW','integration=false','RE899','RE900','RE902','historical','BLOCKED-001/002']:
   assert phrase in out[p].decode()

def test_compatibility_deltas():
 m=api();m.compatibility_pins()
