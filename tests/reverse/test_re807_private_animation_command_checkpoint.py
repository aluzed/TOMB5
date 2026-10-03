"""RE807 metadata-only private checkpoint; exact historical bytes and fail-closed scope."""
import hashlib,json,re,runpy
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[2]
META=ROOT/'docs/reverse/generated/re807-private-animation-command.json'
STORY=ROOT/'docs/stories/RE-807-private-animation-command-proof.md'
DASH=ROOT/'docs/reverse/reconstruction-progress.html'
START=b'<!-- start re807-private-animation-command -->'
END=b'<!-- end re807-private-animation-command -->'
PRECEDING='1b8fbec4f99ed0d80260ecc755acf6205dcb0cadeefe7c069eb254474fee2f96'
REVIEW='08a0fde2ff8e2139dfe01f6d086f488912b134f9775e30d9dee7fe0675dd2c9a'
def dashboard_before_named_re807(b):
    if START in b or END in b:
        assert b.count(START)==b.count(END)==1
        a=b.index(START);assert END in b[a:]
        z=b.index(END,a)+len(END)
        b=b[:a]+b[z:]
    assert hashlib.sha256(b).hexdigest()==PRECEDING
    return b

def test_private_scope_and_review():
    assert META.exists(),'RED: RE807 metadata missing'
    d=json.loads(META.read_text())
    assert d['schema']=='re807-private-animation-command-v1'
    assert d['status']=='progress' and d['author']=='AlexP'
    assert d['approval_scope']=='private-bounded-fixtures-only'
    assert d['review_sha256']==REVIEW
    assert d['candidate_sha256']=='9a8e3bd10933ed163ee72a17d373ff575192e23a54f7f19ead515ed6ff4bef25'
    for k in ('source_integrated','integration_approved','activation_approved','registration_activated','AnimateItem_activated','DoorControl_activated','runtime_performed','gameplay_performed','fullbuild_performed','global_green','production_ready','publication_worker_modified_production'):
        assert d[k] is False,k
    assert d['independent_final_publication_review']=='pending'
    assert d['next_story']=='RE-808'
    assert d['next_frontier']=={'status':'planned-not-proven','discriminant':'command2 jump/gravity or another newly reached discriminant','repeat_closed_matrices':False,'activation_allowed':False}

def test_observed_bounded_contract_and_honest_incidents():
    assert META.exists(),'RED: RE807 metadata missing'
    d=json.loads(META.read_text())
    assert d['observed']=={'cases':6,'command':1,'helper':'TranslateItem','target_returns':6,'target_hook_visits':1080,'complete_buffer_bytes':16716,'buffer_parts':{'ITEM':144,'ANIM':80,'CHANGE':12,'RANGE':32,'COMMAND':64,'TRIG':16384},'calls_total':6,'GetChange_linked':True,'GetChange_exercised':False}
    assert d['native']=={'modes':['normal','strict-ASan-UBSan'],'baseline_failures_per_mode':6,'candidate_pass_per_mode':6,'omission_mutant_failures':4,'omission_control_pass_cases':[0,3],'baseline_causal_scope':'whole-AnimateItem-stub-not-isolated-TranslateItem'}
    assert d['incidents']=={'MEM_WRITE':'anomaly-reproduced-by-independent-review; declared-pass-code-and-read-hooks-only','original_firstbuild_stderr':'unavailable-sealed-producer-stderr-empty','fresh_missing_extern_diagnostic':'independently-reproduced-not-original'}
    assert len(d['limits'])>=10
    assert d['preceding_dashboard_sha256']==PRECEDING

def test_named_append_and_mutation_rejection():
    b=DASH.read_bytes();assert b.count(START)==b.count(END)==1,'RED: RE807 section missing'
    before=dashboard_before_named_re807(b)
    assert dashboard_before_named_re807(before)==before
    for m in (b+b'foreign',b.replace(b'RE-806',b'RE-xxx',1),b+START+END,b.replace(END,b'',1),b.replace(START,END,1),b.replace(START,b'<!-- start re808 -->',1),b.replace(END,START,1)):
        with pytest.raises(AssertionError):dashboard_before_named_re807(m)
    for name,fn in [('test_re806_getchange_integration_checkpoint.py','dashboard_before_named_re806'),('test_re805_public_getchange_checkpoint.py','dashboard_before_named_re805'),('test_re803_private_stationary_animation_checkpoint.py','dashboard_before_named_re804')]:
        old=runpy.run_path(str(ROOT/'tests/reverse'/name))
        assert old[fn](b)==old[fn](before)
        for m in (b+START+END,b.replace(END,b'',1),b.replace(b'RE-806',b'RE-xxx',1)):
            with pytest.raises(AssertionError):old[fn](m)

def test_safe_story_and_explicit_limits():
    assert STORY.exists(),'RED: RE807 story missing'
    b=DASH.read_bytes();assert START in b and END in b
    section=b.split(START)[1].split(END)[0].decode()
    for t in (META.read_text(),STORY.read_text(),section):
        assert not re.search(r'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}|word_le_hex|payload_offset|data:image|item_raw|floor_raw|```(?:asm|mips|cpp|c)\b',t)
    for term in ('## Tracker','- [x]','- [ ]','actual-TU','TranslateItem','1080','16716','MEM_WRITE','stderr original indisponible','diagnostic frais','pas de GREEN global','GetChange non atteint','RE-808','planned-not-proven','11:25','11:45','11:55','12:00','AlexP'):
        assert term in STORY.read_text(),term

def test_production_unchanged():
    frozen={'GAME/CONTROL.C':'5a24abe8b574054875a1fd2e4d66499400cbbfa427d2b0a1f7aa3956000b4158','SPEC_PSXPC_N/CONTROL_S.C':'359970bfdd33ee5342a60c96dbe06be649028e26918250c290850b34a21fd8c1','GAME/CAMERA.C':'52b878651e24858ac3a8f23b4a826b10f58f179ea22176e1d372cb629bfd7a9c','GAME/TYPES.H':'e2549b524b52b1b50dea1412a5c2fc259f9177aa784d9d2a7c18fe3c670d5272'}
    for p,h in frozen.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
