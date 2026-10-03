"""RE804 portable, metadata-only publication; private proof is not production approval."""
import hashlib,json,re,runpy
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[2]
META=ROOT/"docs/reverse/generated/re804-private-animation-change.json"
STORY=ROOT/"docs/stories/RE-804-private-animation-change-proof.md"
DASH=ROOT/"docs/reverse/reconstruction-progress.html"
BLOCKER=ROOT/"docs/stories/blocked/BLOCKED-004-door-production-prerequisites.md"
START=b"<!-- start re804-private-animation-change -->"
END=b"<!-- end re804-private-animation-change -->"
PRECEDING="cad5dd5a83eb8cddf932a476c70a14f0f829d88fe16ed90526f35b7ae3201fce"
FROZEN={'GAME/CONTROL.C': '5a24abe8b574054875a1fd2e4d66499400cbbfa427d2b0a1f7aa3956000b4158', 'SPEC_PSXPC_N/CONTROL_S.C': 'a1f7e696b08476bdcd3f616cef569e2ac99c6a1764b9c9086ee0304f1dd6545c', 'GAME/DOOR.C': 'a538fca3ca3bd0426570d60b7a1c8b3a44d4d96c66b59990a04e716ef4e295ff', 'docs/stories/RE-803-private-stationary-animation-proof.md': 'a9b3797fef565a2cf1cc4b54049535db285c7caeb70aee95855647f33a9467fc', 'docs/stories/RE-802-private-generic-door-prefix.md': '350c534d9fe52386cbc60089a8e0aa9a5b8947aa74848ee5b7636b1ea611a211', 'docs/stories/RE-801-private-door-control-lift-proof.md': '0e81d1e6ee8cb1d2bc001887cf43a83986af3665bedb4c76f10ac32823f47307', 'docs/reverse/generated/re803-private-stationary-animation.json': '606352ae9c020c2a0e77e5ec1e8ec6ab651a5b3555407428e8900b83c6c8f9e7', 'docs/reverse/generated/re801-private-door-control.json': 'e97d28e0582cde3ceb9751e65315737428ca8056b46c6531afeb1a88b3b2664e', 'docs/reverse/generated/re802-private-door-prefix.json': '389a532a6364c91611c4a4556c8cedb1d6aa31fb86e0bde6a8829e324b3a5bf2'}
def metadata():
    assert META.exists(),"RED: métadonnées RE804 absentes"
    return json.loads(META.read_text())
def test_private_scope_not_production_ready():
    d=metadata()
    assert d['schema']=='re804-private-animation-change-v1'
    assert d['approval_scope']=='private-bounded-fixtures-only'
    assert d['production_status']=={'DoorControl':'stub','AnimateItem':'stub','ProcessClosedDoors':'not-implemented','GetChange':'reset-defect-unpatched'}
    for k in ('source_integrated','registration_activated','runtime_performed','fullbuild_performed','global_green','production_ready','public_actual_tu_regression','exact_integration_review','general_stationary_proven'):
        assert d[k] is False,k
    assert d['review_sha256']=='9d2e382e77c4fcd14bcc2e9b94b6debe3458343fa6be90779780c8a669b6c3c1'
    assert d['candidate_sha256']=='42e54b4cd1f0f6a4cc064a80a6a4d64dc9ebb3df45e093d45e7e2f3f0520d2df'
    assert d['helper_candidate_sha256']=='e9d9ff631da7902105c6556844ef94faac210433f69fe3d1a4ea20bcfea33f34'
def test_exact_counts_and_baseline_attribution():
    d=metadata()
    assert d['target']=={'distinct_cases':24,'direct_GetChange':12,'AnimateItem_composition':12,'composition_helper_calls':11,'helper_entries_per_repetition':23,'visits_per_repetition':2090,'reviewer_fresh_replays':2,'buffer_bytes':268}
    assert d['native']['modes']==['normal','strict-ASan-UBSan']
    assert d['native']['baseline']=={'build_exit':0,'run_exit':1,'helper_direct_failures':1,'AnimateItem_stub_failures':12,'total_failures':13}
    assert d['native']['candidate']=={'build_exit':0,'run_exit':0,'pass_per_mode':24}
    assert d['sensitivity']=={'kind':'code-mutants','mode':'normal-only','failures':{'no_reset':2,'exclusive_start':8,'wrong_link_frame':12,'missing_current_refresh':6}}
    assert d['independent_review']=={'passed':True,'blocking_concerns':0,'actual_tu_builds':10,'actual_tu_runs':10,'additional_abi_builds':1,'original_manifest_entries_verified':313,'original_files_unchanged':314,'predecessor_files_verified':643}
    assert len(d['limits'])>=10 and len(d['failed_attempts'])>=2
    assert d['next_story']=='RE-805' and d['next_frontier']['status']=='planned-not-proven'
    assert d['next_frontier']['registration_allowed'] is False
    for term in ('actual-TU','GetChange','revue exacte'):
        assert term in d['next_frontier']['smallest_real_proof']
def test_story_and_current_blocker():
    assert STORY.exists(),'RED: story RE804 absente'
    for t in (STORY.read_text(),BLOCKER.read_text()):
        for term in ('RE-804','RE-805','GetChange','AnimateItem','24','12','11','2090','13','2/8/12/6','actual-TU','revue exacte','stub','pas de GREEN global','02:20','02:40','02:50','03:00'):
            assert term in t,term
    assert '## État actuel — frontière RE-804' in BLOCKER.read_text()
    assert '## Checkpoint historique — frontière RE-803' in BLOCKER.read_text()
    for term in ('## Tracker','- [x]','- [ ]','synthétiques','10→8','commentaire','LP64','NDEBUG','Unicorn','transitoires'):
        assert term in STORY.read_text(),term
def test_named_append_preservation_and_rejections():
    g=runpy.run_path(str(ROOT/'tests/reverse/test_re803_private_stationary_animation_checkpoint.py'))
    assert 'dashboard_before_named_re804' in g,'RED: garde RE804 absente'
    check=g['dashboard_before_named_re804']; b=DASH.read_bytes()
    assert b.count(START)==b.count(END)==1,'RED: section RE804 absente'
    before=check(b)
    assert hashlib.sha256(before).hexdigest()==PRECEDING
    assert check(before)==before
    assert metadata()['preceding_dashboard_sha256']==PRECEDING
    assert b.count(b'</body>')==b.count(b'</html>')==1
    for m in (b+b'foreign',b.replace(b'RE-803',b'RE-xxx',1),b+START+END,b.replace(END,b'',1),b.replace(START,b'<!-- start re805 -->',1),b.replace(START,END,1)):
        with pytest.raises(AssertionError):check(m)
    old=g['dashboard_before_named_re803']
    assert old(before)==old(b)
    for m in (b.replace(b'1716',b'1717',1),b.replace(b'RE-802',b'RE-xxx',1)):
        with pytest.raises(AssertionError):old(m)
def test_public_bytes_safe():
    metadata();assert STORY.exists();b=DASH.read_bytes();assert START in b and END in b
    section=b.split(START,1)[1].split(END,1)[0].decode()
    forbidden=r'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}|word_le_hex|payload_offset|data:image|item_raw|floor_raw|```(?:asm|mips|cpp|c)\b'
    for t in (META.read_text(),STORY.read_text(),BLOCKER.read_text(),section):
        assert not re.search(forbidden,t)
def test_frozen_predecessors_and_production():
    for p,h in FROZEN.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
