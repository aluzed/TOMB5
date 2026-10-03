"""RE809 publication of a bounded RED finding, never integration approval."""
import hashlib,json,re,runpy
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[2]
META=ROOT/'docs/reverse/generated/re809-private-deactivate.json'
STORY=ROOT/'docs/stories/RE-809-private-deactivate-proof.md'
BLOCK=ROOT/'docs/stories/blocked/BLOCKED-005-removeactiveitem-predecessor-link.md'
DASH=ROOT/'docs/reverse/reconstruction-progress.html'
START=b'<!-- start re809-private-deactivate -->'
END=b'<!-- end re809-private-deactivate -->'
PRECEDING='2a10621f996faa5d05180b70f52a64d210eed7d6ab0cff46ce9cc214b1e691d3'
REVIEW='5dcae0ee07522d214d38323b90f6d70cae47d661f765db395980cab58839a67b'
def dashboard_before_named_re809(b):
    b=runpy.run_path(str(ROOT/'scripts/reverse/re811_provenance.py'))['dashboard_before_re811'](b)
    if START in b or END in b:
        assert b.count(START)==b.count(END)==1
        a=b.index(START);assert END in b[a:]
        z=b.index(END,a)+len(END);b=b[:a]+b[z:]
    assert hashlib.sha256(b).hexdigest()==PRECEDING
    return b

def test_bounded_red_not_production_pass():
    assert META.exists(),'RED: RE809 metadata missing'
    d=json.loads(META.read_text())
    assert d['schema']=='re809-private-deactivate-v1'
    assert d['status']=='blocked' and d['author']=='AlexP'
    assert d['review_sha256']==REVIEW
    assert d['approval_scope']=='private-archive-characterization-only'
    assert d['independent_final_publication_review']=='pending'
    assert d['original_review_accepted_as_pass'] is False
    assert d['observed']=={'real_returns':12,'hook_visits':1098,'complete_buffer_bytes':17150,'RemoveActiveItem_cases':6,'AnimateItem_opcode3_cases':6}
    assert d['native']=={'modes':['normal','strict-ASan-UBSan'],'RemoveActiveItem_RED_per_mode':2,'RemoveActiveItem_RED_cases':['nonhead-middle','nonhead-tail'],'AnimateItem_stub_RED_per_mode':6,'candidate_cmd3_created':False}
    assert d['readiness']=='blocked' and d['next_story']=='RE-810'
    for k in ('source_integrated','integration_approved','activation_approved','production_correctness_approved','universal_opcode3_absence_approved','runtime_performed','gameplay_performed','fullbuild_performed','global_green','production_ready','target_matrix_replayed_by_publication'):
        assert d[k] is False,k
    assert d['prerequisites']==['BLOCKED-005-removeactiveitem-predecessor-link','RE-810-private-delta-proof','independent-review-before-integration']

def test_named_append_and_predecessor_mutants():
    b=DASH.read_bytes();assert b.count(START)==b.count(END)==1,'RED: RE809 section missing'
    before=dashboard_before_named_re809(b)
    mutations=(b+b'foreign',b.replace(b'RE-808',b'RE-xxx',1),b+START+END,b.replace(END,b'',1),b.replace(START,END,1),b.replace(END,START,1),b.replace(START,b'<!-- start foreign -->',1))
    for m in mutations:
        with pytest.raises(AssertionError):dashboard_before_named_re809(m)
    for name,fn in [('808_private_animation_jump','dashboard_before_named_re808'),('807_private_animation_command','dashboard_before_named_re807'),('806_getchange_integration','dashboard_before_named_re806'),('805_public_getchange','dashboard_before_named_re805'),('803_private_stationary_animation','dashboard_before_named_re804')]:
        old=runpy.run_path(str(ROOT/'tests/reverse'/('test_re'+name+'_checkpoint.py')))
        assert old[fn](b)==old[fn](before)
        for m in mutations:
            with pytest.raises(AssertionError):old[fn](m)

def test_safe_story_blocker_and_honest_limits():
    assert STORY.exists(),'RED: RE809 story missing'
    assert BLOCK.exists(),'RED: BLOCKED005 missing'
    b=DASH.read_bytes();assert START in b and END in b
    texts=[META.read_text(),STORY.read_text(),BLOCK.read_text(),b.split(START)[1].split(END)[0].decode()]
    for t in texts:
        assert not re.search(r'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}|word_le_hex|payload_offset|data:image|item_raw|floor_raw|```(?:asm|mips|cpp|c)\b',t)
    for term in ('## Tracker','- [x]','- [ ]','READINESS : blocked','1098','17150','actual-TU','RE-810','stderr original','verrou','pas de GREEN global','11:25','11:45','11:55','12:00'):
        assert term in STORY.read_text(),term
    for term in ('zero','head','middle','tail','absent','buffers','events','normal','strict','RED','indépendante','avant intégration'):
        assert term in BLOCK.read_text(),term

def test_sources_and_user_deletions_preserved():
    frozen={'GAME/ITEMS.C':'5e9d3337f1c49282520a822d8d9672185fca6ef6d5b681f845307c36c9b12a27','GAME/CONTROL.C':'5a24abe8b574054875a1fd2e4d66499400cbbfa427d2b0a1f7aa3956000b4158','SPEC_PSXPC_N/CONTROL_S.C':'359970bfdd33ee5342a60c96dbe06be649028e26918250c290850b34a21fd8c1'}
    for p,h in frozen.items():
        b=(ROOT/p).read_bytes()
        if p=='GAME/ITEMS.C': b=runpy.run_path(str(ROOT/'scripts/reverse/re811_provenance.py'))['historical_items'](b)
        assert hashlib.sha256(b).hexdigest()==h,p
    for p in ('BLOCKED-001-RE783-closure.md','BLOCKED-002-getfloor-ubsan-closure.md'):
        assert not (ROOT/'docs/stories/blocked'/p).exists()
