"""Contrat documentaire public : ni replay CPU ni build TU."""
import json
import re
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
PATHS = ['docs/stories/RE-950-cpu-timebase-root-counter-checkpoint.md', 'docs/reverse/generated/re950-cpu-counter-checkpoint.json', 'docs/reverse/tomb5-progress-dashboard-re950-cpu-counter-v1.html', 'tests/reverse/test_re950_cpu_counter_checkpoint.py']
EXPECTED = {'schema': 're950.cpu-counter.checkpoint.v1', 'integration': False, 'production_patch': False, 'global_acceptance': False, 'procedure': 'INCOMPLETE', 'publication_review': 'PENDING', 'sources': [{'name': 'PCSX-Redux', 'revision': 'c313b116e6a55786bc127c9b3a07a90b55d97c21', 'license': 'GPL-2.0-or-later'}, {'name': 'nugget', 'revision': '7ffc2b14b3ec4b912e7e79f6e31101ff3f24cc30', 'license': 'MIT'}], 'units': [{'name': 'cd-init-unit03', 'finite_acceptance': True, 'strict_review_passed': False, 'manifest_sha256': '52bc1ee401d30b1a5b7c49c5d9ee28b51e20d94064321979aaf58b5b9ebfd25b', 'members': 167, 'review_manifest_sha256': 'd9dfec121e1d0dcb157b2bd4261fbd6e00b03f3eefc171689517fd07aa1f767f', 'review_members': 226, 'tests': 6, 'arbitrations': 1200, 'producer_ticks': 15, 'reviewer_ticks': 24, 'mutants': 8, 'diagnostic_visits': 10, 'common_suffix_pcs': 314754, 'ram_bytes': 2097152}, {'name': 'cd-init-unit04', 'finite_acceptance': True, 'strict_review_passed': False, 'manifest_sha256': 'c1323b4cddbd61a88879d7f1e351ae68b935b602523ef01842c05aaeeedf3b65', 'members': 390, 'review_manifest_sha256': 'b4e0f5df73ae90d62350484fd63764eb044870603b89b0bf24ee09238a8bf500', 'review_members': 408, 'tests': 8, 'asserted_projections': 693, 'matrix_projections': 112, 'long_projections': 581, 'long_archived': 583, 'initial_unasserted': 2, 'restored_counter_updates': 545, 'cpu_replays': 0, 'mutants': 8, 'missing_spu_exit': 3, 'missing_spu_stdout_empty': True}], 'next_frontier': 'SPU_CURRENT_FRAMES_REQUIRED_BEFORE_NEXT_COUNTER_SET'}

def exact(test, actual, expected):
    test.assertIs(type(actual), type(expected))
    if isinstance(expected, dict):
        test.assertEqual(set(actual), set(expected))
        for key in expected: exact(test, actual[key], expected[key])
    elif isinstance(expected, list):
        test.assertEqual(len(actual), len(expected))
        for a, e in zip(actual, expected): exact(test, a, e)
    else: test.assertEqual(actual, expected)

class Checkpoint(unittest.TestCase):
    def test_exact_schema_types_pins_counts(self):
        p = ROOT / PATHS[1]
        self.assertTrue(p.is_file(), "metadata missing")
        exact(self, json.loads(p.read_text()), EXPECTED)

    def test_story_tracker_limits_links(self):
        p = ROOT / PATHS[0]
        self.assertTrue(p.is_file(), "story missing")
        text = p.read_text()
        for marker in ("## Tracker", "## Nettoyage", "## Mesures", "INCOMPLETE", "integration=false", "production_patch=false", "DIAGNOSTIC", "693", "545", "branchTest", "int32", "GPL", "MIT", "zéro suppression", "PENDING", EXPECTED["next_frontier"]):
            self.assertIn(marker, text)
        links = re.findall(r"\]\(([^)]+)\)", text)
        self.assertGreaterEqual(len(links), 3)
        for link in links:
            self.assertNotIn("://", link)
            target = (p.parent / link).resolve()
            self.assertTrue(target.is_relative_to(ROOT))
            self.assertTrue(target.is_file(), link)

    def test_dashboard_self_contained_and_links(self):
        p = ROOT / PATHS[2]
        self.assertTrue(p.is_file(), "dashboard missing")
        text = p.read_text()
        for marker in ("<!doctype html>", "RE950", "INCOMPLETE", "Non intégré", "PENDING", "693", "545", "1200", EXPECTED["next_frontier"]): self.assertIn(marker, text)
        self.assertTrue(text.rstrip().endswith("</html>"))
        for tag in ("<script", "<img", "<iframe", "<link", "src="): self.assertNotIn(tag, text.lower())
        links = re.findall(r"href=\"([^\"]+)\"", text)
        self.assertGreaterEqual(len(links), 2)
        for link in links: self.assertTrue((p.parent / link).resolve().is_file(), link)

    def test_metadata_only(self):
        for rel in PATHS[:3]:
            p = ROOT / rel
            self.assertTrue(p.is_file(), rel)
            for token in ("word_le_hex", "raw_opcode", "payload_offset", "build/reverse", "0x"):
                self.assertNotIn(token, p.read_text())

if __name__ == "__main__": unittest.main()
