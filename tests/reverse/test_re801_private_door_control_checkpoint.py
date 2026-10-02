"""Publication sûre RE801, indépendante des archives privées."""
import hashlib, json, re, runpy
from pathlib import Path
import pytest
ROOT = Path(__file__).resolve().parents[2]
META = ROOT / 'docs/reverse/generated/re801-private-door-control.json'
STORY = ROOT / 'docs/stories/RE-801-private-door-control-lift-proof.md'
DASH = ROOT / 'docs/reverse/reconstruction-progress.html'
BLOCKER = ROOT / 'docs/stories/blocked/BLOCKED-004-door-production-prerequisites.md'
START, END = b'<!-- start re801-private-door-control -->', b'<!-- end re801-private-door-control -->'
PRECEDING = '5234b7a4b176613bb1525cfa63d3db05f2e3959ae85a869d258bf16d93582403'
def metadata():
    assert META.exists(), 'RED: métadonnées RE801 absentes'
    return json.loads(META.read_text())
def test_private_scope():
    d=metadata()
    assert d['schema']=='re801-private-door-control-v1'
    assert d['approval_scope']=='private-proof-only' and d['production_status']=='DoorControl-stub'
    for k in ('source_integrated','registration_activated','runtime_performed','global_green','full_game_link'):
        assert d[k] is False
    assert d['candidate_sha256']=='d98fe4690e47a82fbfa6fe09f5e01f6b33b99f86ba365e29da8080272a8e65d7'
    assert d['review_sha256']=='2a77bd27399493cfd29bddaeeb738bd834611fd227a39f9aaf68e06353e23803'
    assert d['production_baseline_sha256']=='a538fca3ca3bd0426570d60b7a1c8b3a44d4d96c66b59990a04e716ef4e295ff'
def test_executed_counts_and_attribution():
    d=metadata()
    assert d['target']=={'sequences':16,'calls_per_sequence':6,'calls':96,'visits_per_replay':8342,'prior_reviewer_fresh_replays':2,'cpu_ram_preserved':True}
    assert d['native']['cases_per_mode']==96 and d['native']['baseline_failures_per_mode']==96
    assert d['native']['baseline_run_exit']==1 and d['native']['candidate_run_exit']==0
    assert d['native']['behavioral_doubles'] is False
    assert d['native']['modes']==['normal','strict-ASan-UBSan']
    assert d['sensitivity']=={'expected_output_mutants_rejected':11,'code_mutants':0}
    assert d['observations']=={'bounds_calls':12,'interpolated':6,'open':4,'shut':4,'clamps':8,'events':56,'repaired_copy_entries':8}
    assert d['final_review']=={'kind':'archival','passed':True,'fresh_target_calls':0,'fresh_native_calls':0,'artifact_hashes_verified':1708}
    assert d['prior_review']['verdict_present'] is False
    assert d['projection']['bytes']==2293 and d['projection']['full_ram_archived'] is False
    assert len(d['limits'])>=8 and len(d['failed_attempts'])>=5

def test_story_current_checkpoint():
    assert STORY.exists(), 'RED: story RE801 absente'
    for s in ('## Tracker','- [x]','- [ ]','trigger_flags==1','stub','96','16','8342','2293','ASan','UBSan','archiv','provider','timeout','copies','disjoints','corrél','RE-802','pas de GREEN global','03:00','02:20','02:40','02:50'):
        assert s in STORY.read_text(),s
    for s in ('frontière RE-801','RE-800','OpenThatDoor intégré','RE-798','RE-802','DoorControl','ProcessClosedDoors','registration','pas de GREEN global','preuve privée','non-lift'):
        assert s in BLOCKER.read_text(),s
    d=metadata();assert d['next_story']=='RE-802'
    assert d['next_frontier']['status']=='planned-not-proven'
    assert d['next_frontier']['repeat_old_matrices'] is d['next_frontier']['registration_allowed'] is False

def dashboard_before_named_re802(b):
    """Retire seulement le successeur RE802; épingle chaque octet RE801."""
    start = b'<!-- start re802-private-door-prefix -->'
    end = b'<!-- end re802-private-door-prefix -->'
    if start in b or end in b:
        assert b.count(start) == b.count(end) == 1
        a = b.index(start)
        assert end in b[a:]
        z = b.index(end, a) + len(end)
        b = b[:a] + b[z:]
    assert hashlib.sha256(b).hexdigest() == '75203801505616180d3ed635c737e898f6dba9b219baa60660d9aeb4fcddf595'
    return b

def test_dashboard_preserves_whole_predecessor():
    b=dashboard_before_named_re802(DASH.read_bytes())
    assert b.count(START)==b.count(END)==1,'RED: section RE801 absente'
    a=b.index(START);z=b.index(END,a)+len(END)
    assert hashlib.sha256(b[:a]+b[z:]).hexdigest()==PRECEDING
    assert b.count(b'</body>')==b.count(b'</html>')==1
    for s in ('RE-801','RE-802','96','8342','privée','stub','pas de GREEN global'):
        assert s in b[a:z].decode()

def test_named_successor_rejects_mutations():
    g=runpy.run_path(str(ROOT/'tests/reverse/test_re800_publication.py'))
    assert 'dashboard_before_named_re801' in g,'RED: garde successor absente'
    check=g['dashboard_before_named_re801'];b=DASH.read_bytes()
    assert hashlib.sha256(check(b)).hexdigest()==PRECEDING
    for m in (b+b'foreign',b.replace(b'RE-800',b'RE-xxx',1),b+START+END,b.replace(END,b'',1),b.replace(START,b'<!-- start re802-private-door-control -->',1),b.replace(START,END,1)):
        with pytest.raises(AssertionError):check(m)

def test_new_bytes_safe():
    metadata();assert STORY.exists();b=DASH.read_bytes();assert START in b and END in b
    section=b.split(START,1)[1].split(END,1)[0].decode()
    forbidden=r'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}|word_le_hex|payload_offset|data:image|item_raw|floor_raw|```(?:asm|mips|cpp|c)\b'
    for text in (META.read_text(),STORY.read_text(),section,BLOCKER.read_text()):assert not re.search(forbidden,text)
