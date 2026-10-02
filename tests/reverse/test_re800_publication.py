"""RE800 publication contracts: public metadata only, no private input dependency."""
import hashlib
import json
import re
import runpy
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[2]
STORY = ROOT / 'docs/stories/RE-800-openthatdoor-production-integration.md'
META = ROOT / 'docs/reverse/generated/re800-openthatdoor-integration.json'
DASH = ROOT / 'docs/reverse/reconstruction-progress.html'
BLOCKER = ROOT / 'docs/stories/blocked/BLOCKED-004-door-production-prerequisites.md'
START, END = b'<!-- start re800-integration -->', b'<!-- end re800-integration -->'
PRECEDING = 'ee30d8b3cfb87ca589fde3c61c5129cc9cdf5eeba738715f0d618caef18edfed'
FORBIDDEN = r'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}|word_le_hex|payload_offset|data:image|item_raw|floor_raw|```(?:asm|mips)\b'


def metadata():
    assert META.exists(), 'RED: RE800 integration metadata absent'
    return json.loads(META.read_text())


def test_accepted_integration_is_bounded_not_global_green():
    d = metadata()
    assert d['schema'] == 're800-openthatdoor-integration-v1'
    assert d['source_integrated'] is True and d['integration_accepted'] is True
    assert d['effective_gate'] == 'PSX_VERSION && PSXPC_TEST && __i386__'
    assert d['candidate_sha256'] == 'a538fca3ca3bd0426570d60b7a1c8b3a44d4d96c66b59990a04e716ef4e295ff'
    assert d['review_sha256'] == 'e094a56b62539a224d18642850248900aaace1fd404644b909ac9237d48c45a9'
    assert d['baseline'] == {'build_exit': 0, 'run_exit': 1, 'cases': 3328, 'failures': 2944, 'modes': ['normal', 'asan-ubsan']}
    assert d['public_actual_tu'] == {'cases_per_mode': 3328, 'modes': ['normal', 'asan-ubsan'], 'build_exit': 0, 'run_exit': 0, 'runtime_diagnostics': []}
    assert d['shutthatdoor_cases_per_mode'] == 144
    assert d['code_mutants_rejected'] == 5
    assert d['registration_activated'] is d['runtime_performed'] is d['full_game_link'] is d['global_green'] is False
    assert d['readiness'] == {'OpenThatDoor': 'integrated-bounded-GREEN', 'initializer': 'private-bounded-not-integrated', 'DoorControl': 'blocked', 'ProcessClosedDoors': 'blocked', 'registration': 'not-activated', 'natural_callback_bridge': 'blocked', 'gameplay': 'not-validated'}


def test_target_review_is_historical_not_fresh_replay():
    d = metadata()
    assert d['target_review'] == {'fresh_target_replay': False, 'fresh_authenticated_decoded_words': 131, 'historical_cases_independently_reconstructed': 3328}
    assert d['public_sweeps'] == 'all-four-meshes-active-different-from-RE799-masks'
    assert len(d['preconditions']) >= 6 and len(d['limits']) >= 5


def test_story_and_blocker_current_frontier():
    assert STORY.exists(), 'RED: RE800 tracked story absent'
    text = STORY.read_text()
    for word in ('## Tracker', '- [x]', '- [ ]', '2944', '3328', 'ASan', 'UBSan', 'disjoints', 'i386', 'pas de GREEN global', 'RE-801', 'DoorControl', 'ProcessClosedDoors', 'ordre', 'alias', 'historique', 'gc-sections', '03:00', '02:20', '02:40', '02:50'):
        assert word in text, word
    blocker = BLOCKER.read_text()
    for word in ('RE-800', 'OpenThatDoor intégré', 'RE-801', 'DoorControl', 'ProcessClosedDoors', 'registration', 'pas de GREEN global', 'RE-798'):
        assert word in blocker, word
    assert 'DoorControl, OpenThatDoor et ProcessClosedDoors non implémentés' not in blocker


def test_next_frontier_is_small_real_doorcontrol_proof():
    d = metadata()
    assert d['next_story'] == 'RE-801'
    n = d['next_frontier']
    assert n['symbol'] == 'DoorControl' and n['status'] == 'planned-not-proven'
    assert n['repeat_old_matrices'] is False and n['registration_allowed'] is False
    for word in ('branche', 'actual-TU', 'RED', 'cible', 'dépendance', 'revue'):
        assert word in n['smallest_real_proof'], word


def dashboard_before_named_re801(b):
    """Retire uniquement RE801 et vérifie le digest entier du dashboard RE800."""
    start = b'<!-- start re801-private-door-control -->'
    end = b'<!-- end re801-private-door-control -->'
    if start in b or end in b:
        assert b.count(start) == b.count(end) == 1
        a = b.index(start)
        assert end in b[a:]
        z = b.index(end, a) + len(end)
        b = b[:a] + b[z:]
    assert hashlib.sha256(b).hexdigest() == '5234b7a4b176613bb1525cfa63d3db05f2e3959ae85a869d258bf16d93582403'
    return b


def test_dashboard_pins_every_preceding_byte():
    b = dashboard_before_named_re801(DASH.read_bytes())
    assert b.count(START) == b.count(END) == 1, 'RED: RE800 dashboard section absent'
    a = b.index(START); z = b.index(END, a) + len(END)
    assert hashlib.sha256(b[:a] + b[z:]).hexdigest() == PRECEDING
    assert b.count(b'</body>') == b.count(b'</html>') == 1
    section = b[a:z].decode()
    for word in ('RE-800', 'RE-801', '3328', '2944', 'intégré', 'historique', 'DoorControl', 'pas de GREEN global'):
        assert word in section


def test_predecessor_exclusion_rejects_all_unrelated_changes():
    guard = runpy.run_path(str(ROOT / 'tests/reverse/test_re799_private_door_open_checkpoint.py'))
    assert 'dashboard_before_named_re800' in guard, 'RED: named successor preservation guard absent'
    check = guard['dashboard_before_named_re800']
    b = dashboard_before_named_re801(DASH.read_bytes())
    assert hashlib.sha256(check(b)).hexdigest() == PRECEDING
    for mutant in (b + b'foreign', b.replace(b'RE-799', b'RE-xxx', 1), b + START + END, b.replace(END, b'', 1), b.replace(START, b'<!-- start re801-integration -->', 1)):
        with pytest.raises(AssertionError):
            check(mutant)


def test_new_public_bytes_are_metadata_only():
    metadata()
    assert STORY.exists()
    b = DASH.read_bytes()
    assert START in b and END in b
    section = b.split(START, 1)[1].split(END, 1)[0].decode()
    for text in (META.read_text(), STORY.read_text(), section, BLOCKER.read_text()):
        assert not re.search(FORBIDDEN, text)
