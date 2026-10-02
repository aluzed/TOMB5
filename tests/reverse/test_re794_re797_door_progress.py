"""Safe public readiness metadata, never replaying private target or runtime data."""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / 'docs/reverse/generated/re794-re797-door-progress.json'
START, END = b'<section id="re794">', b'<!-- end re794 -->'
STORIES = [
    'RE-794-native-first-portal.md',
    'RE-795-door-registration-prerequisite.md',
    'RE-796-door-initializer-proof.md',
    'RE-797-shutthatdoor-reconstruction.md',
]
BLOCKER = 'blocked/BLOCKED-004-door-production-prerequisites.md'
FORBIDDEN = r'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}|word_le_hex|data:image|item_raw|floor_raw|payload_offset|world_vertices|```(?:asm|mips)\b'


def proof():
    assert MANIFEST.exists(), 'RED: RE794–797 reviewed metadata manifest missing'
    return json.loads(MANIFEST.read_text())


def test_readiness_is_not_global_green():
    d = proof()
    assert d['schema'] == 'door-progress-v1'
    assert d['readiness'] == {
        'first_natural_portal': 'observed-native-mixed-relink',
        'generic_door_producer': 'missing-native-behavioral-RED',
        'native_initializer': 'absent-target-proof-only',
        'shutthatdoor': 'integrated-bounded-GREEN',
        'door_registration': 'not-activated',
        'DoorControl': 'blocked', 'OpenThatDoor': 'blocked',
        'ProcessClosedDoors': 'blocked', 'natural_bridge_callback': 'blocked',
        'fullbuild': 'not-performed', 'global_gameplay': 'not-validated',
    }
    assert d['next_story'] == 'RE-798'
    assert d['limits']


def test_runtime_and_missing_producer_are_distinct():
    d = proof()
    assert d['re794'] == {
        'run': 'run03', 'portal_transitions_claimed': 1,
        'transition_draw': 94, 'transition_without_player_input': True,
        'real_input_draws': 60, 'stop_draw': 161,
        'observations_compared': 4, 'rooms_per_observation': 169,
        'cells_per_observation': 11459, 'floor_data_bytes': 16944,
        'selected_buffers_equal': True, 'helper_entry_return_attribution': False,
        'process_observations_capped': 20, 'bridge_callback_entries': 0,
        'shutdown': 'intentional-debugger-kill',
    }
    r = d['re795']
    assert (r['target_generic_slots'], r['target_loaded_conditions']) == (14, 2)
    assert (r['native_cases'], r['native_records_per_case'], r['native_installed_per_case']) == (4, 46, 0)
    assert r['behavioral_requirement_exit'] == 1
    assert r['characterization_exit'] == 0
    assert r['registration_activated'] is False


def test_target_initializer_is_not_native_equivalence():
    r = proof()['re796']
    assert r['complete_authentic_calls'] == 32
    assert r['matrix'] == {'orientations': 4, 'flip_conditions': 2, 'navbox_conditions': 2, 'portal_conditions': 2}
    assert r['authentic_helpers_continuously_executed'] is True
    assert r['comparison_scope'] == 'complete-selected-regions-not-whole-RAM'
    assert (r['target_door_bytes'], r['native_projected_bytes']) == (92, 82)
    assert r['projection_is_native_pointer_adapter'] is False
    assert r['actual_native_initializer_executed'] is False


def test_helper_integration_preserves_failed_history():
    d = proof()
    r = d['re797']
    assert r['target_calls'] == r['normal_cases'] == r['sanitizer_cases'] == 144
    assert r['baseline_behavioral_failures'] == 120
    assert r['actual_production_TU'] is True
    assert r['normal_exit'] == r['sanitizer_exit'] == 0
    assert r['sanitizer_diagnostics'] == []
    assert r['integration_gate'] == 'PSX_VERSION && PSXPC_TEST && defined(__i386__)'
    assert r['alternative_backend'] == 'UNIMPLEMENTED-preserved'
    assert r['original_review_status'] == 'failed-preserved'
    assert r['original_sanitizer_claim_valid'] is False
    assert r['fixture_correction'] == 'direct-packed-member-pointer-stores'
    assert r['whole_door_approved'] is False
    for row in d['reviews'].values():
        assert re.fullmatch('[a-f0-9]{64}', row['sha256'])
        assert row['security_concerns'] == row['logic_errors'] == []
        assert row['passed'] is True
    assert re.fullmatch('[a-f0-9]{64}', r['original_review_sha256'])


def test_stories_blocker_and_metadata_are_safe():
    proof()
    texts = [MANIFEST.read_text()]
    for name in STORIES + [BLOCKER]:
        p = ROOT / 'docs/stories' / name
        assert p.exists(), 'RED: progress story or blocker missing'
        text = p.read_text()
        assert '## Tracker' in text and '- [x]' in text and '- [ ]' in text
        assert 'pas de GREEN global' in text and 'RE-798' in text
        texts.append(text)
    assert '## Critères de reprise' in texts[-1]
    for text in texts:
        assert not re.search(FORBIDDEN, text)


def test_dashboard_is_exactly_append_only_and_frozen_stories_unchanged():
    d = proof()
    dashboard = (ROOT / 'docs/reverse/reconstruction-progress.html').read_bytes()
    assert dashboard.count(START) == dashboard.count(END) == 1
    a = dashboard.index(START)
    b = dashboard.index(END, a) + len(END)
    assert hashlib.sha256(dashboard[:a] + dashboard[b:]).hexdigest() == d['preceding_dashboard_sha256']
    assert dashboard.count(b'</body>') == dashboard.count(b'</html>') == 1
    section = dashboard[a:b].decode()
    for word in ['RE-794', 'RE-795', 'RE-796', 'RE-797', 'RE-798', 'ShutThatDoor', 'bloqué']:
        assert word in section
    assert not re.search(FORBIDDEN, section)
    assert len(d['frozen_history']) == 5
    for name, digest in d['frozen_history'].items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest
