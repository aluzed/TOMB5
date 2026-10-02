"""Public metadata contracts; no game files, private archive or runtime replay."""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROOF = ROOT / 'docs/reverse/generated/re790-re793-native-bridge-progress.json'
DASH = ROOT / 'docs/reverse/reconstruction-progress.html'
START, END = '<section id="re790">', '<!-- end re790 -->'
STORIES = [
    'RE-790-natural-registration-runtime.md',
    'RE-791-authentic-bridge-corpus.md',
    'RE-792-natural-base-registration.md',
    'RE-793-bridge-navigation-boundary.md',
]


def proof():
    assert PROOF.exists(), 'RED: reviewed native progress metadata absent'
    return json.loads(PROOF.read_text())


def test_accepted_scope_and_preserved_refusal():
    d = proof()
    assert d['schema'] == 'native-bridge-progress-v1'
    assert d['review']['passed'] is True
    assert d['review']['security_concerns'] == d['review']['logic_errors'] == []
    assert d['review']['scope'] == 'natural-base-selection-and-registration-only'
    assert d['broad_review']['passed'] is False
    assert d['readiness'] == {
        'natural_registration': 'verified-bounded',
        'natural_bridge_callback': 'blocked',
        'source_patch': 'blocked',
        'fullbuild': 'not-performed',
        'global_gameplay': 'not-validated',
    }
    for k in ('verdict_sha256',):
        assert re.fullmatch('[a-f0-9]{64}', d['review'][k])
    assert d['limits'] and d['next_story'] == 'RE-794'


def test_real_runtime_counts_are_separated_from_samples():
    d = proof()
    assert d['rome']['items'] == 151 and d['rome']['bridge_items'] == 0
    b = d['base']
    assert (b['native_level'], b['container_ordinal']) == (4, 5)
    assert (b['items'], b['rooms'], b['bridge_items']) == (177, 169, 8)
    assert b['producer_calls'] == 2 and b['unique_registered_slots'] == 6
    assert b['slot_comparisons'] == 12 and b['callback_entries'] == 0
    assert b['reported_draws'] == 452 and b['release_draw'] == 2
    assert b['retained_pairs'] == {'GetHeight': 964, 'GetCeiling': 840, 'GetCollisionInfo': 100}
    assert b['reported_entries'] == {'GetHeight': 17149, 'GetCeiling': 13367, 'GetCollisionInfo': 450}
    assert b['totals_are_archived_counters_not_full_trace'] is True
    assert d['relink']['fresh_translation_units'] == ['GETSTUFF', 'SETUP', 'OBJECTS', 'BRIDGE_CALLBACKS']
    assert d['relink']['classification'] == 'mixed-provenance-not-fullbuild'


def test_corpus_cardinality_and_navigation_boundary():
    d = proof()
    assert d['corpus']['levels'] == 15 and d['corpus']['items'] == 2084
    assert d['corpus']['bridge_totals'] == {'BRIDGE_FLAT': 35, 'BRIDGE_TILT1': 0, 'BRIDGE_TILT2': 31}
    assert sum(r['bridge_items'] for r in d['corpus']['positive_levels']) == 66
    assert d['navigation']['rooms'] == 169 and d['navigation']['cells'] == 11459
    assert d['navigation']['geometric_portals'] == 626
    assert d['navigation']['private_tests_passed'] == 11
    assert d['navigation']['runtime_performed'] is False
    assert d['navigation']['gameplay_reachability'] == 'unproven'


def test_stories_have_trackers_and_honest_limits():
    d = proof()
    for name in STORIES:
        p = ROOT / 'docs/stories' / name
        assert p.exists(), 'RED: native progress story absent'
        text = p.read_text()
        assert '## Tracker' in text and '- [x]' in text and '- [ ]' in text
        assert 'pas de GREEN global' in text and 'RE-794' in text
        assert not re.search(r'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}|word_le_hex|data:image|```(?:asm|mips)\b', text)
    blocker = ROOT / 'docs/stories/blocked/BLOCKED-003-RE793-natural-bridge-navigation.md'
    assert blocker.exists(), 'RED: fresh navigation blocker handoff absent'
    assert '## Critères de reprise' in blocker.read_text()


def test_append_only_dashboard_history():
    d = proof()
    dashboard = DASH.read_bytes()
    # Exclude only RE794; its own guard pins every preceding dashboard byte.
    successor_start, successor_end = b'<section id="re794">', b'<!-- end re794 -->'
    if successor_start in dashboard:
        assert dashboard.count(successor_start) == dashboard.count(successor_end) == 1
        a = dashboard.index(successor_start)
        b = dashboard.index(successor_end, a) + len(successor_end)
        dashboard = dashboard[:a] + dashboard[b:]
    start, end = START.encode(), END.encode()
    assert dashboard.count(start) == dashboard.count(end) == 1
    a = dashboard.index(start)
    b = dashboard.index(end, a) + len(end)
    assert hashlib.sha256(dashboard[:a] + dashboard[b:]).hexdigest() == d['preceding_dashboard_sha256']
    assert dashboard.count(b'</body>') == dashboard.count(b'</html>') == 1
    section = dashboard[a:b].decode()
    assert 'RE-790' in section and 'RE-793' in section and 'RE-794' in section
    assert 'callback' in section and 'bloqué' in section


def test_public_manifest_is_metadata_only():
    proof()
    text = PROOF.read_text()
    assert not re.search(r'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}|word_le_hex|data:image|item_raw|floor_raw|payload_offset|world_vertices', text)
