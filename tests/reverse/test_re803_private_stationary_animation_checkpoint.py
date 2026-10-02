"""Portable RE803 publication contracts; no ignored proof dependency."""
import hashlib, json, re
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[2]
META=ROOT/'docs/reverse/generated/re803-private-stationary-animation.json'
STORY=ROOT/'docs/stories/RE-803-private-stationary-animation-proof.md'
DASH=ROOT/'docs/reverse/reconstruction-progress.html'
BLOCKER=ROOT/'docs/stories/blocked/BLOCKED-004-door-production-prerequisites.md'
START=b'<!-- start re803-private-stationary-animation -->'
END=b'<!-- end re803-private-stationary-animation -->'
PRECEDING='beaaa9177c5e454b9d3a05f0c36a7603a4b979c1bba88b2d9356b1856989904a'
FROZEN={'GAME/CONTROL.C': '5a24abe8b574054875a1fd2e4d66499400cbbfa427d2b0a1f7aa3956000b4158', 'GAME/DOOR.C': 'a538fca3ca3bd0426570d60b7a1c8b3a44d4d96c66b59990a04e716ef4e295ff', 'docs/stories/RE-802-private-generic-door-prefix.md': '350c534d9fe52386cbc60089a8e0aa9a5b8947aa74848ee5b7636b1ea611a211', 'docs/stories/RE-801-private-door-control-lift-proof.md': '0e81d1e6ee8cb1d2bc001887cf43a83986af3665bedb4c76f10ac32823f47307', 'docs/reverse/generated/re801-private-door-control.json': 'e97d28e0582cde3ceb9751e65315737428ca8056b46c6531afeb1a88b3b2664e', 'docs/reverse/generated/re802-private-door-prefix.json': '389a532a6364c91611c4a4556c8cedb1d6aa31fb86e0bde6a8829e324b3a5bf2'}
def metadata():
    assert META.exists(),'RED: métadonnées RE803 absentes'
    return json.loads(META.read_text())
def dashboard_before_named_re803(b):
    assert b.count(START)==b.count(END)==1,'RED: section RE803 absente'
    a=b.index(START);assert END in b[a:]
    z=b.index(END,a)+len(END)
    before=b[:a]+b[z:]
    assert hashlib.sha256(before).hexdigest()==PRECEDING
    return before
def test_fail_closed_scope():
    d=metadata()
    assert d['schema']=='re803-private-stationary-animation-v1'
    assert d['approval_scope']=='private-bounded-fixtures-only'
    assert d['production_status']=={'DoorControl':'stub','AnimateItem':'stub','ProcessClosedDoors':'not-implemented'}
    for k in ('source_integrated','registration_activated','runtime_performed','fullbuild_performed','global_green','general_stationary_proven','self_loop_proven','getchange_authentic_exercised'):
        assert d[k] is False,k
    assert d['candidate_sha256']=='d60ca859dc9e12bfef8f2e0c47ce05bbffd488fbfed19e646839a1d32488f896'
    assert d['review_sha256']=='db511cd1da0a5a1272c709053b6d7747952b3ccf738e7d8b604f115e6d3124f4'
def test_exact_observed_behavior():
    d=metadata()
    assert d['direct']=={'cases':16,'advances':8,'jumps':8,'advance_frames':[3,4],'jump_animations':[0,1],'jump_frames':[8,2],'target_visits':1716,'buffer_bytes':224,'return_proven':True}
    assert d['composition']=={'cases':4,'target_visits':642,'real_services':['TriggerActive','AnimateItem'],'return_proven':True,'synthetic_only':True,'jumps':0}
    assert d['native']['modes']==['normal','ASan','UBSan','ASan+UBSan']
    assert d['native']['baseline']=={'build_exit':0,'run_exit':1,'direct_failures':16,'composition_failures':4}
    assert d['native']['candidate']=={'build_exit':0,'run_exit':0,'direct_pass':16,'composition_pass':4}
    assert d['sensitivity']=={'kind':'code-mutants','mode':'normal-only','failures':{'frame':16,'jump':8,'touch':16}}
    assert d['independent_review']=={'passed':True,'fresh_native_builds':19,'fresh_native_runs':19,'original_hashes_verified':271,'fresh_target_replay':True}
    assert d['next_story']=='RE-804'
    assert d['next_frontier']['status']=='planned-not-proven'
    assert 'GetChange' in d['next_frontier']['smallest_real_proof']
    assert d['next_frontier']['repeat_closed_fixtures'] is d['next_frontier']['registration_allowed'] is False
    assert len(d['limits'])>=10 and len(d['failed_attempts'])>=3
def test_story_blocker_and_explicit_limits():
    assert STORY.exists(),'RED: story RE803 absente'
    for t in (STORY.read_text(),BLOCKER.read_text()):
        for word in ('RE-803','RE-804','GetChange','AnimateItem','TriggerActive','1716','642','stub','pas de GREEN global','02:20','02:40','02:50','03:00'):
            assert word in t,word
    t=STORY.read_text()
    for word in ('## Tracker','- [x]','- [ ]','synthétique','required_state','NDEBUG','LP64','Unicorn','sans saut','frame7'):
        assert word in t,word
    assert '## État actuel — frontière RE-803' in BLOCKER.read_text()
def test_named_append_and_mutation_rejection():
    b=DASH.read_bytes();dashboard_before_named_re803(b)
    assert metadata()['preceding_dashboard_sha256']==PRECEDING
    assert b.count(b'</body>')==b.count(b'</html>')==1
    for m in (b+b'foreign',b.replace(b'RE-802',b'RE-xxx',1),b+START+END,b.replace(END,b'',1),b.replace(START,b'<!-- start re804 -->',1),b.replace(START,END,1)):
        with pytest.raises(AssertionError):dashboard_before_named_re803(m)
def test_public_bytes_safe():
    metadata();assert STORY.exists();b=DASH.read_bytes();assert START in b and END in b
    section=b.split(START,1)[1].split(END,1)[0].decode()
    for t in (META.read_text(),STORY.read_text(),BLOCKER.read_text(),section):
        assert not re.search(r'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}|word_le_hex|payload_offset|data:image|item_raw|floor_raw|```(?:asm|mips|cpp|c)\b',t)
def test_frozen_sources_history_and_report():
    for p,h in FROZEN.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
