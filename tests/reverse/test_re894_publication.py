"""Portable publication contract, no target/native behavioral replay."""
import hashlib
import importlib.util
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[2]
def api():
    path=ROOT/'scripts/reverse/re894_publication.py'
    assert path.exists(), 'RED: RE894 generator absent'
    spec=importlib.util.spec_from_file_location('re894',path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def test_contract():
    m=api();d=m.metadata();assert m.validate(d)==d
    assert d['publication_review']=='PENDING_INDEPENDENT_EXACT_HASH_REVIEW'
    assert d['next_ticket']=='RE895' and d['integration'] is False
    rows=d['archived_private_results'];assert [r['ticket'] for r in rows]==['RE892','RE893']
    assert [r['reviewer_accepted']['native'] for r in rows]==[42,36]
    assert [r['producer_accepted']['native'] for r in rows]==[54,30]
    assert [r['caller_returned'] for r in rows]==[False,True]
    assert rows[0]['expression_scope']==dict(algebra_inspected=12,translation_sensitive=3,identity_rotation_zero_difference=9)
    assert rows[1]['positions']==[[26,-40,54],[34,-48,62],[43,-55,71]]
    assert rows[1]['reviewer_accepted']['uninstrumented_direct_return']==6
    assert [r['reviewer_accepted']['cpu_mutants'] for r in rows]==[3,2]
    assert rows[1]['reviewer_accepted']['initial_ram']==3
    for r in rows:
        assert r['fullraw_bytes']==2528
        assert r['candidate_sha256']=='9002cac7b27566f572a8b744cabddc36431b0b00fae9599d6342f156a523ba88'
        assert r['reviewer_accepted']['target']==r['reviewer_accepted']['cpu']==r['reviewer_accepted']['declarative']==3
    assert rows[0]['approved_verdict_sha256']=='7b03420c8563a49cd45c98e44d2f743b88843098a93d5c8624a8e6ed1024a9e0'
    assert rows[1]['approved_verdict_sha256']=='7d9ec09df201b7ec50067511dc37bacd55cf3932ada7ae1f7147bfe83051595f'
    assert rows[1]['completion_verdict_sha256']=='23bc5208ba55ba8c7f0440ca5d7fa101577da2b6daad4d403e1b88b9f9abeb2e'

@pytest.mark.parametrize('mutation',['unknown','boolint','intbool','nestedbool','count','hash','scope','return','review','positions','expression','initialram','completion'])
def test_recursive_schema_failclosed(mutation):
    m=api();d=m.metadata();r=d['archived_private_results'][0]
    if mutation=='unknown':r['unknown']=False
    if mutation=='boolint':d['integration']=0
    if mutation=='intbool':r['reviewer_accepted']['target']=True
    if mutation=='nestedbool':r['caller_returned']=0
    if mutation=='count':r['reviewer_accepted']['native']=54
    if mutation=='hash':r['approved_verdict_sha256']='0'*64
    if mutation=='scope':d['global_scope']='PASS'
    if mutation=='return':d['archived_private_results'][1]['caller_returned']=False
    if mutation=='review':d['publication_review']='PASS'
    if mutation=='positions':d['archived_private_results'][1]['positions'][0][0]+=1
    if mutation=='expression':r['expression_scope']['translation_sensitive']=12
    if mutation=='initialram':d['archived_private_results'][1]['reviewer_accepted']['initial_ram']=True
    if mutation=='completion':d['archived_private_results'][1]['completion_verdict_sha256']='0'*64
    with pytest.raises(ValueError):m.validate(d)

def test_deterministic_outputs_and_inverse():
    m=api();before=(ROOT/m.PRIOR_DASHBOARD).read_bytes();out=m.render(before)
    assert out==m.render(before) and set(out)==set(m.OUTPUT_PATHS)
    assert m.preceding_dashboard(out[m.DASHBOARD])==before
    for p,b in out.items():assert (ROOT/p).read_bytes()==b;m.guard_output(p,b)
    m.check()

@pytest.mark.parametrize('change',['history','missing','duplicate','altered','trailing','unknown'])
def test_dashboard_failclosed(change):
    m=api();data=m.render((ROOT/m.PRIOR_DASHBOARD).read_bytes())[m.DASHBOARD];s=m.SECTION.encode()
    if change=='history':data=b'foreign'+data
    if change=='missing':data=data.replace(b'<!-- RE894 PUBLICATION END -->',b'')
    if change=='duplicate':data=data[:-7]+s+b'</html>'
    if change=='altered':data=data.replace(s,s.replace(b'ARCHIVED',b'FRESH'))
    if change=='trailing':data+=b'foreign'
    if change=='unknown':data=data[:-7]+b'<!-- unknown section -->'+b'</html>'
    with pytest.raises(ValueError):m.preceding_dashboard(data)

@pytest.mark.parametrize('bad',[b'0x80012345',b'FUN_80012345',b'word_le_hex',b'raw_opcode',b'payload_offset',b'data:image/png;base64,',b'-----BEGIN '+b'PRIVATE KEY-----',b'ghp_'+b'a'*30,b'```mips\n',b'\0',b'raw_pc=123',b'register_values=[1]',b'target_address=123'])
def test_negative_guard_with_same_path_benign_control(bad):
    m=api();p=m.STORY;m.guard_added(p,b'safe symbolic metadata')
    with pytest.raises(ValueError):m.guard_added(p,bad)

@pytest.mark.parametrize('p',['SPEC_PSXPC_N/MATHS.C','build/reverse/proof.bin','assets/new.png','docs/reverse/proof.exe','../escape.md'])
def test_asset_scope(p):
    with pytest.raises(ValueError):api().guard_added(p,b'safe metadata')

def test_story_report_acceptance_and_source_preservation():
    m=api();o=m.render((ROOT/m.PRIOR_DASHBOARD).read_bytes())
    for p in [m.STORY,m.REPORT]:
        t=o[p].decode()
        for phrase in ['## Progression','## Evidence','## Blockers','## Acceptance','- [x]','- [ ]','integration=false','ARCHIVED','RE895','PENDING_INDEPENDENT_EXACT_HASH_REVIEW','BLOCKED-001/002','direct RET','ENOSPC']:assert phrase in t
    for p,h in m.PRESERVED.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h
