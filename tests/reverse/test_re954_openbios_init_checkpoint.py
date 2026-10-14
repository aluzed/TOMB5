"""Public metadata contract only; no private replay or production approval."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
META = ROOT / 'docs/reverse/generated/re954_openbios_init_checkpoint.json'
STORY = ROOT / 'docs/stories/RE-954-openbios-init-checkpoint.md'
DASH = ROOT / 'docs/reverse/tomb5-progress-dashboard-re954-v1.html'
PREVIOUS = ROOT / 'docs/reverse/tomb5-progress-dashboard-re953-v1.html'
BEGIN = '<!-- RE954-BEGIN -->'
END = '<!-- RE954-END -->'
EXPECTED = {
    'ticket': 'RE954', 'scope': 'private open-source Init producer checkpoint',
    'redux_pin': 'c313b116e6a55786bc127c9b3a07a90b55d97c21',
    'openbios_pin': '7ffc2b14b3ec4b912e7e79f6e31101ff3f24cc30',
    'producer_manifest': '7bfb277de561fd0eddecc2cf44794a274209e9de2f8878c14f004928d5b1eedc',
    'review_manifest': '29f287931c05dd2dca70e9f72693d0cf5f1820d28468d696602d8e3a62b9b029',
    'producer_members': 204, 'review_members': 191,
    'finite_review': 'PASS', 'strict_review': 'INCOMPLETE',
    'command': 'Init', 'handler_body_executed': False,
    'openbios_return': 0, 'host_cycle_before': 0, 'host_cycle_after': 0,
    'scheduler_deadline': 26993, 'scheduler_arrival': 26996,
    'review_fresh_builds': 16, 'review_fresh_native_runs': 16,
    'review_assertion_rejected_mutants': 14,
    'production_patch': False, 'integration': False, 'global_frontier_changed': False,
    'publication_review_snapshot': 'PENDING',
    'next_frontier': 'genuine cdlInit body and legitimate asynchronous IRQ/state producers',
}

def validate(value):
    if type(value) is not dict or set(value) != set(EXPECTED):
        raise ValueError('schema')
    for key, expected in EXPECTED.items():
        if type(value[key]) is not type(expected) or value[key] != expected:
            raise ValueError(key)
    return value

class Checkpoint(unittest.TestCase):
    def test_exact_metadata(self):
        validate(json.loads(META.read_text()))

    def test_every_field_sensitive(self):
        for key, expected in EXPECTED.items():
            with self.subTest(key=key):
                bad = dict(EXPECTED)
                bad[key] = not expected if type(expected) is bool else (expected + 1 if type(expected) is int else expected + '!')
                with self.assertRaises(ValueError):
                    validate(bad)
        for key, expected in EXPECTED.items():
            if type(expected) in (int, bool):
                bad = dict(EXPECTED)
                bad[key] = bool(expected) if type(expected) is int else int(expected)
                with self.assertRaises(ValueError):
                    validate(bad)

    def test_dashboard_inverse(self):
        previous = PREVIOUS.read_bytes()
        self.assertEqual(hashlib.sha256(previous).hexdigest(), '70fa2b6c5a4e41e6b20548089bf938d5ada78dd1035053b2731bc4753f632c9f')
        current = DASH.read_text()
        self.assertEqual(current.count(BEGIN), 1)
        self.assertEqual(current.count(END), 1)
        start = current.index(BEGIN)
        stop = current.index(END) + len(END) + 1
        self.assertEqual(current[start:stop][-1], '\n')
        self.assertEqual((current[:start] + current[stop:]).encode(), previous)
        self.assertIn('RE954', current[start:stop])
        self.assertIn('INCOMPLETE', current[start:stop])

    def test_story_limits_and_links(self):
        text = STORY.read_text()
        for token in ('timeout', '0/0', 'avant', 'INCOMPLETE', '16', '14', 'Nettoyage', 'Tracker', 'aucun secteur', 'publication'):
            self.assertIn(token, text)
        self.assertTrue(META.is_file())
        self.assertTrue(DASH.is_file())

if __name__ == '__main__':
    unittest.main()
