"""RE898 public-only safety/schema/inverse contract; no ignored proof imports."""
import hashlib, importlib.util, json
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[2]
def api():
 p=ROOT/'scripts/reverse/re898_publication.py'
 assert p.exists(), 'RED: RE898 metadata publication generator absent'
 s=importlib.util.spec_from_file_location('re898',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def test_contract():
 m=api();d=m.metadata();assert m.validate(d)==d
 assert d['schema']=='re898-private-proof-publication-v1'
 assert d['publication_review']=='PENDING_INDEPENDENT_EXACT_HASH_REVIEW'
 assert d['integration'] is False and d['production_patch'] is False
 assert d['next_ticket']=='RE899'
 rows=d['archived_private_results'];assert [r['ticket'] for r in rows]==['RE895','RE896','RE897']
 assert [r['producer']['native'] for r in rows]==[24,18,60]
 assert [r['reviewer_accepted']['native'] for r in rows]==[24,6,60]
 assert rows[1]['reviewer_total']==dict(target=6,cpu=6,native=16)
 assert [r['fullraw_verdict'] for r in rows]==['PASS_FINITE','FAIL_FOUR_BYTES','PASS_FINITE']
 assert rows[0]['caller_returned'] is False and rows[0]['gte_commands']==0
 assert rows[2]['native_matrix']==dict(baseline_red=12,candidate_green=24,rollback_first=12,rollback_second=12)
 assert rows[2]['audit_additional']==dict(target=0,native=0)
 assert all(r['historical_failures'] for r in rows)
 assert 'not saturation' in d['limits']

@pytest.mark.parametrize('mutation',['unknown','boolint','intbool','count','hash','review','global','failure','frontier','audit'])
def test_schema_drift(mutation):
 m=api();d=m.metadata();r=d['archived_private_results'][0]
 if mutation=='unknown':d['extra']='x'
 if mutation=='boolint':d['integration']=0
 if mutation=='intbool':r['producer']['target']=True
 if mutation=='count':r['reviewer_accepted']['native']=60
 if mutation=='hash':r['review_verdict_sha256']='0'*64
 if mutation=='review':d['publication_review']='PASS'
 if mutation=='global':d['global_scope']='PASS'
 if mutation=='failure':d['archived_private_results'][1]['fullraw_verdict']='PASS'
 if mutation=='frontier':d['next_ticket']='RE898'
 if mutation=='audit':d['archived_private_results'][2]['audit_additional']['native']=60
 with pytest.raises(ValueError):m.validate(d)

def test_render_public_fixtures_and_inverse():
 m=api();before=(ROOT/m.PRIOR_DASHBOARD).read_bytes();out=m.render(before)
 assert out==m.render(before) and set(out)==set(m.OUTPUT_PATHS)
 assert m.preceding_dashboard(out[m.DASHBOARD])==before
 for p,b in out.items():assert (m.read_maintained() if p==m.MAINTAINED else (ROOT/p).read_bytes())==b;m.guard_output(p,b)
 assert json.loads(out[m.JSON_PATH])==m.metadata()
 maintained=m.read_maintained();assert m.preceding_maintained(maintained)==m.maintained_before()
 m.check()

@pytest.mark.parametrize('change',['history','missing','duplicate','altered','trailing','unknown'])
def test_exact_dashboard_inverse(change):
 m=api();s=m.SECTION.encode();data=m.render((ROOT/m.PRIOR_DASHBOARD).read_bytes())[m.DASHBOARD]
 if change=='history':data=b'foreign'+data
 if change=='missing':data=data.replace(b'<!-- RE898 PUBLICATION END -->',b'')
 if change=='duplicate':data=data[:-7]+s+b'</html>'
 if change=='altered':data=data.replace(s,s.replace(b'ARCHIVED',b'FRESH'))
 if change=='trailing':data+=b'foreign'
 if change=='unknown':data=data[:-7]+b'<!-- unknown -->'+b'</html>'
 with pytest.raises(ValueError):m.preceding_dashboard(data)

@pytest.mark.parametrize('bad',[b'0x80012345',b'FUN_80012345',b'word_le_hex',b'raw_opcode',b'payload_offset',b'data:image/png;base64,',b'-----BEGIN '+b'PRIVATE KEY-----',b'ghp_'+b'a'*30,b'```mips\n',b'\0',b'raw_pc=123',b'register_values=[1]',b'target_address=123',b'a'*100001])
def test_guard_with_benign_control(bad):
 m=api();m.guard_added(m.STORY,b'safe symbolic metadata')
 with pytest.raises(ValueError):m.guard_added(m.STORY,bad)

@pytest.mark.parametrize('p',['SPEC_PSXPC_N/MATHS.C','build/reverse/proof.bin','assets/new.png','docs/reverse/proof.exe','../escape.md','/tmp/x'])
def test_path_guard(p):
 with pytest.raises(ValueError):api().guard_added(p,b'safe metadata')

def test_documents():
 m=api();out=m.render((ROOT/m.PRIOR_DASHBOARD).read_bytes())
 for p in (m.STORY,m.REPORT):
  for phrase in ['## Progression','## Evidence','## Blockers','## Acceptance','- [x]','- [ ]','RE899','PENDING_INDEPENDENT_EXACT_HASH_REVIEW','integration=false','FULLRAW FAIL','BLOCKED-001/002']:
   assert phrase in out[p].decode()


def test_historical_guard_adapter_exact_delta():
 m=api();text=(ROOT/'tests/reverse/test_re830_table_provenance_publication.py').read_text()
 assert m.original_test830(text)
 for bad in [text+'# foreign\n',text.replace(m.ADAPTER,''),text.replace(m.ADAPTER,m.ADAPTER*2)]:
  with pytest.raises(ValueError):m.original_test830(bad)

@pytest.mark.parametrize('change',['history','missing','duplicate','altered','trailing','unknown'])
def test_maintained_inverse_mutants(change):
 m=api();data=m.read_maintained();s=m.SECTION.encode()
 if change=='history':data=b'foreign'+data
 if change=='missing':data=data.replace(b'<!-- RE898 PUBLICATION END -->',b'')
 if change=='duplicate':data=data[:-7]+s+b'</html>'
 if change=='altered':data=data.replace(s,s.replace(b'ARCHIVED',b'FRESH'))
 if change=='trailing':data+=b'foreign'
 if change=='unknown':data=data[:-7]+b'<!-- unknown -->'+b'</html>'
 with pytest.raises(ValueError):m.preceding_maintained(data)
