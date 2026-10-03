"""Safe RE805 publication and exact append-only historical preservation."""
import hashlib,json,re,runpy
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[2]
META=ROOT/'docs/reverse/generated/re805-public-getchange-contract.json'
STORY=ROOT/'docs/stories/RE-805-public-getchange-contract.md'
DASH=ROOT/'docs/reverse/reconstruction-progress.html'
START=b'<!-- start re805-public-getchange-contract -->'
END=b'<!-- end re805-public-getchange-contract -->'
PRECEDING='cc625c9a8ddae8d8b96d5b31c214624959c22e74f131a20602e8c32653a5bdb7'
def dashboard_before_named_re805(b):
    if START in b or END in b:
        assert b.count(START)==b.count(END)==1
        a=b.index(START);assert END in b[a:]
        z=b.index(END,a)+len(END);b=b[:a]+b[z:]
    assert hashlib.sha256(b).hexdigest()==PRECEDING
    return b

def test_scope_and_counts():
    assert META.exists(),'RED: RE805 metadata missing'
    d=json.loads(META.read_text())
    assert d['schema']=='re805-public-getchange-v1'
    assert d['author']=='AlexP'
    assert d['cases_per_mode']==1440 and d['baseline_failures_per_mode']==48
    assert d['candidate_failures_per_mode']==0
    assert d['modes']==['normal','strict-ASan-UBSan']
    assert d['helper_definition']=='SPEC_PSXPC_N/CONTROL_S.C'
    assert d['compiled_real_tus']==['SPEC_PSXPC_N/CONTROL_S.C','GAME/ITEMS.C']
    assert d['oracle']=='synthetic-independent-lexicographic-pairs'
    for k in ('production_modified','AnimateItem_activated','runtime_performed','fullbuild_performed','global_green','production_ready','target_matrix_replayed'):
        assert d[k] is False
    assert d['upstream_review_sha256']=='9d2e382e77c4fcd14bcc2e9b94b6debe3458343fa6be90779780c8a669b6c3c1'

def test_named_append_and_malformed_rejection():
    b=DASH.read_bytes();assert b.count(START)==b.count(END)==1
    before=dashboard_before_named_re805(b)
    assert dashboard_before_named_re805(before)==before
    for m in (b+b'foreign',b.replace(b'RE-804',b'RE-xxx',1),b+START+END,b.replace(END,b'',1),b.replace(START,END,1),b.replace(START,b'<!-- start re806 -->',1)):
        with pytest.raises(AssertionError):dashboard_before_named_re805(m)
    old=runpy.run_path(str(ROOT/'tests/reverse/test_re803_private_stationary_animation_checkpoint.py'))
    assert old['dashboard_before_named_re804'](b)==old['dashboard_before_named_re804'](before)

def test_safe_metadata_story_and_section():
    assert STORY.exists(),'RED: RE805 story missing'
    b=DASH.read_bytes();section=b.split(START)[1].split(END)[0].decode()
    for t in (META.read_text(),STORY.read_text(),section):
        assert not re.search(r'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}|word_le_hex|payload_offset|data:image|item_raw|floor_raw|```(?:asm|mips|cpp|c)\b',t)
    for term in ('## Tracker','- [x]','- [ ]','actual-TU','GetChange','1440','48','pas de GREEN global','revue exacte','02:50','AlexP'):
        assert term in STORY.read_text()

def test_public_contract_autonomy():
    runner=(ROOT/'tests/reverse/test_re805_getchange.py').read_text()
    fixture=(ROOT/'tests/reverse/fixtures/re805/getchange.cpp').read_text()
    for token in ('payload.bin','target-rows','autonomy-2026','dependency/glew','read_bytes','fopen('):
        assert token not in runner+fixture
    assert "ROOT/'GAME/ITEMS.C'" in runner
    assert 'GetChange(&item,&animations[1])' in fixture
    assert 'order=12*c+r' in fixture
