"""Fresh public-only metadata regression; no private proof dependencies."""
import hashlib
import importlib.util
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[2]
def api():
    script=ROOT/'scripts/reverse/re891_publication.py'
    assert script.exists(), 'RED: RE891 generator absent'
    spec=importlib.util.spec_from_file_location('re891',script)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def test_contract():
    m=api(); d=m.metadata(); assert m.validate(d)==d
    assert d['publication_review']=='PENDING_INDEPENDENT_EXACT_HASH_REVIEW'
    assert d['next_ticket']=='RE892' and d['integration'] is False
    rows=d['archived_private_results']; assert [r['ticket'] for r in rows]==['RE886','RE887','RE888','RE889','RE890']
    assert [r['reviewer_accepted']['native'] for r in rows]==[18,12,18,18,18]
    assert rows[0]['reviewer_accepted']['baseline_red']==6
    assert rows[1]['reviewer_cumulative']['native']==48
    assert rows[3]['reviewer_additional_declarative']==3
    assert rows[4]['corrected_review_rerun'] is False
    assert rows[4]['producer_attempt_totals']==dict(target=9,cpu=9,declarative=9,native=37)
    for r in rows:
        assert r['fullraw_bytes']==2528 and r['caller_returned'] is False
        assert r['reviewer_accepted']['target']==r['reviewer_accepted']['cpu']==r['reviewer_accepted']['declarative']==3
        assert r['candidate_sha256']=='a23d973e7f99876092411ffe8e4c159670318fd1c8e6f2d15a5c1811af9377cb'
    assert [r['approved_verdict_sha256'] for r in rows]==['d19a201e8c2a9fdde08439f223bfb311dc805dd51c709e34ca1c000e483b13cd','40951d551720e671ffc790d672f61dd41b14df00293414694406207b345d742d','25e152cffb4c0090218a8617c4dbfcaf86e87f1091cbb8c2d533f03266bb13cd','4451340ccbe61b959ce1210ae08641be886c4813bd2bf0f73efb31de735895e7','7f1f8f1ef622386f651091abf129b7091ae1113467d68c63fddf374eb33282bf']

@pytest.mark.parametrize('mutation',['unknown','boolint','intbool','nestedbool','count','hash','scope','return','review','rerun','attempt'])
def test_recursive_schema_failclosed(mutation):
    m=api();d=m.metadata();r=d['archived_private_results'][0]
    if mutation=='unknown':r['unknown']=False
    if mutation=='boolint':d['integration']=0
    if mutation=='intbool':r['reviewer_accepted']['target']=True
    if mutation=='nestedbool':r['caller_returned']=0
    if mutation=='count':r['reviewer_accepted']['native']=42
    if mutation=='hash':r['approved_verdict_sha256']='0'*64
    if mutation=='scope':d['global_scope']='PASS'
    if mutation=='return':r['caller_returned']=True
    if mutation=='review':d['publication_review']='PASS'
    if mutation=='rerun':d['archived_private_results'][4]['corrected_review_rerun']=True
    if mutation=='attempt':d['archived_private_results'][4]['producer_attempt_totals']['native']=18
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
    if change=='missing':data=data.replace(b'<!-- RE891 PUBLICATION END -->',b'')
    if change=='duplicate':data=data[:-7]+s+b'</html>'
    if change=='altered':data=data.replace(s,s.replace(b'ARCHIVED',b'FRESH'))
    if change=='trailing':data+=b'foreign'
    if change=='unknown':data=data[:-7]+b'<!-- unknown section -->'+b'</html>'
    with pytest.raises(ValueError):m.preceding_dashboard(data)

@pytest.mark.parametrize('bad',[b'0x80012345',b'FUN_80012345',b'word_le_hex',b'raw_opcode',b'payload_offset',b'data:image/png;base64,',b'-----BEGIN '+b'PRIVATE KEY-----',b'ghp_'+b'a'*30,b'```mips\n',b'\0'])
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
        for phrase in ['## Progression','## Evidence','## Blockers','## Acceptance','- [x]','- [ ]','integration=false','ARCHIVED','RE892','InterpolateMatrix','PENDING_INDEPENDENT_EXACT_HASH_REVIEW']:assert phrase in t
        assert 'caller never returned' in t
    for p,h in m.PRESERVED.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h
