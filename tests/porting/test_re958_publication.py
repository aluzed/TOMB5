"""Documentary publication checks, not recorder behavioral tests."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
STORY = 'docs/stories/RE-958-linux32-recorder-reservation.md'
DASHBOARD = 'docs/reverse/tomb5-progress-dashboard-re958-v1.html'


def test_scope_and_limits():
    for name in (STORY, DASHBOARD):
        text = (ROOT / name).read_text()
        for token in ('integration=false', 'production_patch=false', 'BLOCKED-008', 'BLOCKED-009', '459', 'Cleanup'):
            assert token in text, (name, token)
        assert 'gameplay' in text


def test_publication_links_resolve():
    for name in (STORY, DASHBOARD):
        path = ROOT / name
        text = path.read_text()
        links = re.findall(r'href=["\']([^"\']+)', text) if name.endswith('.html') else re.findall(r'\]\(([^)]+)\)', text)
        assert links
        for link in links:
            if '://' not in link and not link.startswith('#'):
                assert (path.parent / link.split('#')[0]).resolve().is_file(), (name, link)
