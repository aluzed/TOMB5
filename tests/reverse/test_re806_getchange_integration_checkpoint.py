"""RE806 safe reviewed integration publication; exact-byte historical dashboard guard."""
import hashlib,json,re,runpy
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[2]
META=ROOT/'docs/reverse/generated/re806-getchange-integration.json'
STORY=ROOT/'docs/stories/RE-806-getchange-reset-integration.md'
DASH=ROOT/'docs/reverse/reconstruction-progress.html'
START=b'<!-- start re806-getchange-integration -->'
END=b'<!-- end re806-getchange-integration -->'
PRECEDING='8d5e908fe4f1d1411eea36e3909226fcdd4f214a43cd24253bfd72fb5cd044d6'
SOURCE='359970bfdd33ee5342a60c96dbe06be649028e26918250c290850b34a21fd8c1'
def dashboard_before_named_re806(b):
    # RE807 successor owns an exact full preceding-dashboard guard.
    start807=b'<!-- start re807-private-animation-command -->'
    end807=b'<!-- end re807-private-animation-command -->'
    if start807 in b or end807 in b:
        assert b.count(start807)==b.count(end807)==1
        a807=b.index(start807);assert end807 in b[a807:]
        z807=b.index(end807,a807)+len(end807)
        b=b[:a807]+b[z807:]
        assert hashlib.sha256(b).hexdigest()=='1b8fbec4f99ed0d80260ecc755acf6205dcb0cadeefe7c069eb254474fee2f96'
    if START in b or END in b:
        assert b.count(START)==b.count(END)==1
        a=b.index(START);assert END in b[a:]
        z=b.index(END,a)+len(END);b=b[:a]+b[z:]
    assert hashlib.sha256(b).hexdigest()==PRECEDING
    return b

def test_reviewed_integration_scope():
    assert META.exists(),'RED: RE806 reviewed integration metadata missing'
    d=json.loads(META.read_text())
    assert d['schema']=='re806-getchange-integration-v1'
    assert d['integration_approved'] is d['source_integrated'] is True
    assert d['source_sha256']==SOURCE
    assert d['cases_per_mode']==1440
    assert d['baseline_failures_per_mode']==48 and d['current_failures_per_mode']==0
    assert d['modes']==['normal','strict-ASan-UBSan']
    assert d['only_integrated_delta']=='GetChange per-matching-change range counter reset'
    for k in ('AnimateItem_activated','DoorControl_activated','runtime_performed','gameplay_performed','global_green','production_ready','target_matrix_replayed','publication_worker_modified_production'):
        assert d[k] is False,k
    assert d['preceding_dashboard_sha256']==PRECEDING
    assert d['fullbuild']['configure_exit']==0
    assert isinstance(d['fullbuild']['build_exit'],int)
    assert d['fullbuild']['game_run'] is False
    assert d['independent_final_publication_review']=='pending'
    repair=d['provenance_guard_repair']
    assert repair['original_final_review']=='FAIL-preserved-immutable'
    assert repair['independent_repair_review']=='pending'
    assert repair['baseline_sha256']=='a1f7e696b08476bdcd3f616cef569e2ac99c6a1764b9c9086ee0304f1dd6545c'
    assert repair['candidate_sha256']==SOURCE
    assert repair['method']=='remove-only-unique-approved-reset-and-hash-reconstructed-baseline'
    assert d['expanded_publication_checks_context']=='historical-before-provenance-repair'
    assert d['current_repaired_publication_checks']=={
        'reviewer_expanded':{'exit':0,'passed':34,'subtests_passed':2},
        'RE800_RE806_with_provenance':{'exit':0,'passed':54,'subtests_passed':2},
        'skipped':0,'extra_exclusions':[]}
    for term in ('FAIL original conservé','revue réparation pending','revue publication pending'):
        assert term in STORY.read_text(),term

def test_named_append_and_mutation_rejection():
    b=DASH.read_bytes();assert b.count(START)==b.count(END)==1,'RED: RE806 section missing'
    before=dashboard_before_named_re806(b)
    assert dashboard_before_named_re806(before)==before
    for m in (b+b'foreign',b.replace(b'RE-805',b'RE-xxx',1),b+START+END,b.replace(END,b'',1),b.replace(START,END,1),b.replace(START,b'<!-- start re807 -->',1)):
        with pytest.raises(AssertionError):dashboard_before_named_re806(m)
    for name,fn in [('test_re805_public_getchange_checkpoint.py','dashboard_before_named_re805'),('test_re803_private_stationary_animation_checkpoint.py','dashboard_before_named_re804')]:
        old=runpy.run_path(str(ROOT/'tests/reverse'/name))
        assert old[fn](b)==old[fn](before)

def test_safe_publication_story_and_limits():
    assert STORY.exists(),'RED: RE806 integration story missing'
    b=DASH.read_bytes();assert START in b and END in b
    section=b.split(START)[1].split(END)[0].decode()
    for t in (META.read_text(),STORY.read_text(),section):
        assert not re.search(r'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}|word_le_hex|payload_offset|data:image|item_raw|floor_raw|```(?:asm|mips|cpp|c)\b',t)
    for term in ('## Tracker','- [x]','- [ ]','actual-TU','GetChange','1440','48','pas de GREEN global','AnimateItem','DoorControl','11:25','11:45','11:55','12:00','AlexP','## Acceptation fullbuild'):
        assert term in STORY.read_text(),term

def test_exact_source_and_historical_re805():
    assert hashlib.sha256((ROOT/'SPEC_PSXPC_N/CONTROL_S.C').read_bytes()).hexdigest()==SOURCE
    frozen={'docs/reverse/generated/re805-public-getchange-contract.json': '472db21578da52d05a4aa58727b03c363bae901c8d54b851d0430d70a811cf8e', 'docs/stories/RE-805-public-getchange-contract.md': '40b70f8d986a0bc270df4c1cc84b98cc0c7f2937e81958c142340347dba30281'}
    for p,h in frozen.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
