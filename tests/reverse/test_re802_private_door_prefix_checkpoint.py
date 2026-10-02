"""RE802 safe publication: portable tests, no ignored proof dependency."""
import hashlib, json, re, runpy
from pathlib import Path
import pytest
ROOT = Path(__file__).resolve().parents[2]
META = ROOT/'docs/reverse/generated/re802-private-door-prefix.json'
STORY = ROOT/'docs/stories/RE-802-private-generic-door-prefix.md'
DASH = ROOT/'docs/reverse/reconstruction-progress.html'
BLOCKER = ROOT/'docs/stories/blocked/BLOCKED-004-door-production-prerequisites.md'
START, END = b'<!-- start re802-private-door-prefix -->', b'<!-- end re802-private-door-prefix -->'
PRECEDING = '75203801505616180d3ed635c737e898f6dba9b219baa60660d9aeb4fcddf595'
def metadata():
    assert META.exists(), 'RED: métadonnées RE802 absentes'
    return json.loads(META.read_text())
def test_fail_closed_readiness():
    d=metadata()
    assert d['schema']=='re802-private-door-prefix-v1'
    assert d['approval_scope']=='private-prefix-proof-only'
    assert d['production_status']=={'DoorControl':'stub','AnimateItem':'stub','ProcessClosedDoors':'not-implemented'}
    for k in ('source_integrated','registration_activated','runtime_performed','fullbuild_performed','global_green','full_game_link','doorcontrol_return_proven','animateitem_body_executed'):
        assert d[k] is False,k
    assert d['candidate_sha256']=='bf1ed5dc4c15f1d02d72c7a98b639d3ad40079937cfa68c8030dfec43fe2d0a1'
    assert d['review_sha256']=='d975a3b7049dce5eaa94a7a1391e6960d76546a086398bcd094dab372b6657db'
def test_exact_counts_and_composition():
    d=metadata()
    assert d['target']=={'cases':40,'active':20,'inactive':20,'timer_changes':12,'hook_visits':2408,'ordered_events':120,'stop':'before-first-AnimateItem-instruction','fresh_independent_replay':True}
    assert d['native']['modes']==['normal','strict-ASan-UBSan']
    assert d['native']['cases_per_mode']==40
    assert d['native']['baseline']=={'build_exit':0,'run_exit':1,'event_failures':40,'state_failures':26,'input_failures':0}
    assert d['native']['candidate']=={'build_exit':0,'run_exit':0,'event_failures':0,'state_failures':0,'input_failures':0}
    assert d['native']['real_services']==['TriggerActive']
    assert d['native']['animateitem_observation']=='entry-exception-no-return'
    assert d['native']['detect_leaks'] is False
    assert d['sensitivity']=={'kind':'code-mutants','mode':'normal-only','failures':{'status':[20,0],'goal':[20,0],'polarity':[40,0],'no-trigger':[26,40],'no-animate':[0,40]},'count_order':['state','events']}
    assert d['projection']=={'regions':10,'target_bytes_per_case':2293,'native_bytes_per_case':2283,'removed_padding_bytes':10,'caller_stack_excluded_bytes':32,'pointer_fields_only_relocated':True,'full_target_ram_compared':True}
    assert d['independent_review']=={'kind':'fresh-target-and-native','passed':True,'blocking_concerns':0,'reviewed_hashes':1896,'native_builds':4,'abi_probe_separate':True}
    assert len(d['limits'])>=10 and len(d['failed_attempts'])>=5
    for term in ('transitoires','Unicorn','LP64','NDEBUG','goal','allocations','assertions','corrél','multi-frame'):
        assert term in ' '.join(d['limits']),term
    assert d['next_story']=='RE-803'
    assert d['next_frontier']['status']=='planned-not-proven'
    assert d['next_frontier']['repeat_closed_prefix_matrices'] is d['next_frontier']['registration_allowed'] is False
    assert 'AnimateItem' in d['next_frontier']['smallest_real_proof']
def test_story_blocker_and_limits():
    assert STORY.exists(),'RED: story RE802 absente'
    for text in (STORY.read_text(),BLOCKER.read_text()):
        for term in ('RE-802','RE-803','AnimateItem','TriggerActive','40','2408','120','stub','non-lift','pas de GREEN global','02:20','02:40','02:50','03:00'):
            assert term in text,term
    assert '## Tracker' in STORY.read_text() and '- [x]' in STORY.read_text() and '- [ ]' in STORY.read_text()
    assert '## État actuel — frontière RE-802' in BLOCKER.read_text()
def test_historical_bytes_and_named_section():
    b=DASH.read_bytes();assert b.count(START)==b.count(END)==1,'RED: section RE802 absente'
    a=b.index(START);z=b.index(END,a)+len(END)
    assert hashlib.sha256(b[:a]+b[z:]).hexdigest()==PRECEDING
    assert b.count(b'</body>')==b.count(b'</html>')==1
    assert metadata()['preceding_dashboard_sha256']==PRECEDING
    for term in ('RE-802','RE-803','AnimateItem','40','2408','privée','pas de GREEN global'):
        assert term in b[a:z].decode()
def test_named_successor_fails_closed():
    g=runpy.run_path(str(ROOT/'tests/reverse/test_re801_private_door_control_checkpoint.py'))
    assert 'dashboard_before_named_re802' in g,'RED: garde RE802 absente'
    check=g['dashboard_before_named_re802'];b=DASH.read_bytes()
    assert hashlib.sha256(check(b)).hexdigest()==PRECEDING
    for m in (b+b'foreign',b.replace(b'RE-801',b'RE-xxx',1),b+START+END,b.replace(END,b'',1),b.replace(START,b'<!-- start re803-private-door-prefix -->',1),b.replace(START,END,1)):
        with pytest.raises(AssertionError):check(m)
def test_new_bytes_safe():
    metadata();assert STORY.exists();b=DASH.read_bytes();assert START in b and END in b
    section=b.split(START,1)[1].split(END,1)[0].decode()
    forbidden=r'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}|word_le_hex|payload_offset|data:image|item_raw|floor_raw|```(?:asm|mips|cpp|c)\b'
    for text in (META.read_text(),STORY.read_text(),section,BLOCKER.read_text()):
        assert not re.search(forbidden,text)

FROZEN_HISTORY = {'docs/stories/RE-797-shutthatdoor-reconstruction.md': '2e52c6c8f73d583f09bf25bf8e9bfd459d6370aa8e9ab4f9a21a8772a11cd3b6', 'docs/stories/RE-796-door-initializer-proof.md': 'b5df86d11ef66cd9b2e5f45a9a528107d8b4152a490ee6d017fc95051cdfab87', 'docs/stories/RE-800-openthatdoor-production-integration.md': '03b9eb99aa0b19e159f2fdb50b63f72930d07c3e182c5fe3f49ac770c8ba3c66', 'docs/stories/RE-799-private-door-open-proof.md': '05c6cc30760d450c615348323b867a563b5c099a0d1a0bdc2ebe439f03e4e019', 'docs/stories/RE-794-native-first-portal.md': 'ab7ecfc87c9f45c5a05a05e38389985533823a0dff925838d728fb180b93c4f2', 'docs/stories/RE-795-door-registration-prerequisite.md': '08d4ec220dc9d1570d4c4cbeec3684dff22f60f2dd3ea4aa7f896bbd2e88f68f', 'docs/stories/RE-798-private-generic-door-initializer.md': '1bbf6dc859cf1fda5cc5389c508a1a057a1d53ca1432004d6ae5e9553172f0a1', 'docs/stories/RE-801-private-door-control-lift-proof.md': '0e81d1e6ee8cb1d2bc001887cf43a83986af3665bedb4c76f10ac32823f47307', 'docs/reverse/generated/re801-private-door-control.json': 'e97d28e0582cde3ceb9751e65315737428ca8056b46c6531afeb1a88b3b2664e', 'docs/reverse/generated/re800-openthatdoor-integration.json': '2350f8c8bf4a7b0618140facef0f4cb563d04ca370f8df62c172e8e1d20bf971', 'docs/reverse/generated/re794-re797-door-progress.json': '7fd343b5da164e88d52287fafa81f14e4f7264e88a3a3395295c0ab30bff600f', 'docs/reverse/generated/re799-door-open-proof.json': '4fd3a6cd8696ca6c29d71a77fe8abd71a0cddedbf93a612684165ea18c6d498c'}
def test_frozen_predecessor_stories_and_metadata():
    for name, digest in FROZEN_HISTORY.items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
