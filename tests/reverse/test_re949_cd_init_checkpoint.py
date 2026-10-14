"""Public metadata contract; private CPU/CD proofs are archived, not replayed here."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
META = ROOT / 'docs/reverse/generated/re949-cd-init-checkpoint.json'
STORY = ROOT / 'docs/stories/RE-949-cd-init-scheduler-checkpoint.md'
DASH = ROOT / 'docs/reverse/tomb5-progress-dashboard-re949-cd-init-v1.html'

class Checkpoint(unittest.TestCase):
    def test_explicit_acceptance_layers(self):
        self.assertTrue(META.is_file(), 'checkpoint metadata missing')
        d = json.loads(META.read_text())
        self.assertEqual(set(d), {'schema', 'integration', 'production_patch', 'global_acceptance', 'procedure', 'units', 'next_frontier'})
        self.assertEqual(d['schema'], 're949.cd-init.checkpoint.v1')
        for key in ('integration', 'production_patch', 'global_acceptance'):
            self.assertIs(d[key], False)
        self.assertEqual(d['procedure'], 'INCOMPLETE')
        self.assertEqual([u['name'] for u in d['units']], ['cd-init-unit01', 'cd-init-unit02'])
        for u, count in zip(d['units'], (184, 123)):
            self.assertEqual(set(u), {'name', 'finite_scope', 'strict_review_passed', 'manifest_sha256', 'members', 'review_manifest_sha256', 'review_members'})
            self.assertEqual(u['finite_scope'], 'ACCEPTED')
            self.assertIs(u['strict_review_passed'], False)
            self.assertIs(type(u['members']), int)
            self.assertIs(type(u['review_members']), int)
            self.assertEqual(u['members'], count)
            self.assertRegex(u['manifest_sha256'], r'^[a-f0-9]{64}$')
            self.assertRegex(u['review_manifest_sha256'], r'^[a-f0-9]{64}$')
        self.assertEqual([u['review_members'] for u in d['units']], [62, 175])
        self.assertEqual(d['units'][1]['review_manifest_sha256'], '1d22d234954369f4ff4ca5fa64732f297f91a9f78cbd9ca8e7e277c1a549e70b')
        self.assertEqual(d['next_frontier'], 'CPU_TIMEBASE_AND_CDRFIFO_DISPATCH')

    def test_story_tracker_limits_cleanup_and_links(self):
        self.assertTrue(STORY.is_file(), 'story missing')
        text = STORY.read_text()
        for marker in ('## Tracker', '## Nettoyage', 'INCOMPLETE', 'integration=false', 'production_patch=false', 'timebase', 'archives', '797', '26993'):
            self.assertIn(marker, text)
        links = re.findall(r'\]\(([^)]+)\)', text)
        self.assertGreaterEqual(len(links), 2)
        for link in links:
            self.assertTrue((STORY.parent / link).resolve().is_file(), link)
        for forbidden in ('word_le_hex', 'raw_opcode', 'payload_offset', '0x1464', '0x1468'):
            self.assertNotIn(forbidden, text)

    def test_dashboard_is_honest_and_self_contained(self):
        self.assertTrue(DASH.is_file(), 'dashboard missing')
        text = DASH.read_text()
        for marker in ('<!doctype html>', 'RE949', 'INCOMPLETE', 'Non intégré', 'timebase', 'Aucun callback', 'Finie'):
            self.assertIn(marker, text)
        self.assertNotIn('<script', text)
        self.assertTrue(text.rstrip().endswith('</html>'))

if __name__ == '__main__':
    unittest.main()
