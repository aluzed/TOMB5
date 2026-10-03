"""RE808 safe publication: exact historical bytes, bounded claims, source frozen."""
import hashlib,json,re,runpy
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[2]
META=ROOT/'docs/reverse/generated/re808-private-animation-jump.json'
STORY=ROOT/'docs/stories/RE-808-private-animation-jump-proof.md'
DASH=ROOT/'docs/reverse/reconstruction-progress.html'
START=b'<!-- start re808-private-animation-jump -->'
END=b'<!-- end re808-private-animation-jump -->'
PRECEDING='6c75650680b052c468ccea3e8b9861d18d5512878727b3c24b93b31460b2c3bd'
REVIEW='9b2f8c0df5fb4df6c9ed368f7504b3c23d74bb0d04a528e642a0e5b33c7199f1'
def dashboard_before_named_re808(b):
    if START in b or END in b:
        assert b.count(START)==b.count(END)==1
        a=b.index(START);assert END in b[a:]
        z=b.index(END,a)+len(END);b=b[:a]+b[z:]
    assert hashlib.sha256(b).hexdigest()==PRECEDING
    return b

def test_private_scope():
    assert META.exists(),'RED: RE808 metadata missing'
    d=json.loads(META.read_text())
    assert d['schema']=='re808-private-animation-jump-v1'
    assert d['author']=='AlexP' and d['status']=='progress'
    assert d['review_sha256']==REVIEW
    assert d['approval_scope']=='private-bounded-fixtures-only'
    assert d['independent_final_publication_review']=='pending'
    for k in ('source_integrated','integration_approved','activation_approved','registration_activated','AnimateItem_activated','DoorControl_activated','runtime_performed','gameplay_performed','fullbuild_performed','global_green','production_ready','publication_worker_modified_production','target_matrix_replayed_by_publication'):
        assert d[k] is False,k
    assert d['next_story']=='RE-809'
    assert d['next_frontier']=={'status':'planned-not-proven','discriminant':'command3/removeactive or a subsequent newly reached dependency','repeat_closed_matrices':False,'activation_allowed':False}

def test_exact_observations_and_incidents():
    assert META.exists(),'RED: RE808 metadata missing'
    d=json.loads(META.read_text())
    assert d['observed']=={'cases':12,'command':2,'target_returns':12,'target_hook_visits':1543,'complete_buffer_bytes':16716,'GetChange_exercised':False,'frame_threshold':'incremented-frame > frame_end','ordered_events':['old-command2','link','gravity','return']}
    assert d['native']=={'modes':['normal','strict-ASan-UBSan'],'baseline_failures_per_mode':12,'candidate_pass_per_mode':12,'mutant_failures':{'omit-jump':5,'link-before':2,'drop-x-second':5},'baseline_causal_scope':'whole-AnimateItem-stub'}
    assert d['incidents']['producer_timeout_seconds']==600
    assert d['incidents']['historical_manifest_status']=='IN_PROGRESS'
    assert d['incidents']['historical_handoff_status']=='EN COURS'
    assert d['preceding_dashboard_sha256']==PRECEDING
    assert len(d['limits'])>=10

def test_named_append_and_mutation_rejection():
    b=DASH.read_bytes();assert b.count(START)==b.count(END)==1,'RED: RE808 section missing'
    before=dashboard_before_named_re808(b)
    assert dashboard_before_named_re808(before)==before
    mutations=(b+b'foreign',b.replace(b'RE-807',b'RE-xxx',1),b+START+END,b.replace(END,b'',1),b.replace(START,END,1),b.replace(START,b'<!-- start re809 -->',1),b.replace(END,START,1))
    for m in mutations:
        with pytest.raises(AssertionError):dashboard_before_named_re808(m)
    for name,fn in [('test_re807_private_animation_command_checkpoint.py','dashboard_before_named_re807'),('test_re806_getchange_integration_checkpoint.py','dashboard_before_named_re806'),('test_re805_public_getchange_checkpoint.py','dashboard_before_named_re805'),('test_re803_private_stationary_animation_checkpoint.py','dashboard_before_named_re804')]:
        old=runpy.run_path(str(ROOT/'tests/reverse'/name))
        assert old[fn](b)==old[fn](before)
        for m in mutations:
            with pytest.raises(AssertionError):old[fn](m)

def test_safe_story_and_limits():
    assert STORY.exists(),'RED: RE808 story missing'
    b=DASH.read_bytes();assert START in b and END in b
    section=b.split(START)[1].split(END)[0].decode()
    for t in (META.read_text(),STORY.read_text(),section):
        assert not re.search(r'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}|word_le_hex|payload_offset|data:image|item_raw|floor_raw|```(?:asm|mips|cpp|c)\b',t)
    for term in ('## Tracker','- [x]','- [ ]','actual-TU','1543','16716','600s','IN_PROGRESS','EN COURS','pas de GREEN global','GetChange non atteint','RE-809','planned-not-proven','11:25','11:45','11:55','12:00','AlexP'):
        assert term in STORY.read_text(),term

def test_production_unchanged():
    frozen={'GAME/CONTROL.C':'5a24abe8b574054875a1fd2e4d66499400cbbfa427d2b0a1f7aa3956000b4158','SPEC_PSXPC_N/CONTROL_S.C':'359970bfdd33ee5342a60c96dbe06be649028e26918250c290850b34a21fd8c1','GAME/CAMERA.C':'52b878651e24858ac3a8f23b4a826b10f58f179ea22176e1d372cb629bfd7a9c','GAME/TYPES.H':'e2549b524b52b1b50dea1412a5c2fc259f9177aa784d9d2a7c18fe3c670d5272'}
    for p,h in frozen.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
