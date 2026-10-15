"""Publication contract for the source-only recorder interruption checkpoint."""
from html.parser import HTMLParser
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
STORY = ROOT / 'docs/stories/RE-957-linux32-recorder-interruption.md'
DASH = ROOT / 'docs/reverse/tomb5-progress-dashboard-re957-v1.html'


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.links.extend(value for name, value in attrs if name == 'href')


def test_publication_scope_and_progress():
    story = STORY.read_text()
    dash = DASH.read_text()
    for text in (story, dash):
        for value in ('integration=false', 'production_patch=false', '452', 'KeyboardInterrupt', 'SystemExit', 'Cleanup'):
            assert value in text
        assert 'gameplay' in text
    assert 'Status: Done' in story
    assert '- [x]' in story
    assert '- [ ]' in story
    assert 'SIGKILL' in story and 'SIGTERM' in story
    assert 'BLOCKED-008' in story and 'BLOCKED-009' in story


def test_all_local_links_resolve():
    parser = Links()
    parser.feed(DASH.read_text())
    assert len(parser.links) >= 2
    for ref in parser.links:
        assert not ref.startswith(('http:', 'https:', '//'))
        assert (DASH.parent / ref.split('#')[0]).is_file(), ref
    refs = re.findall(r'\[[^\]]+\]\(([^)]+)\)', STORY.read_text())
    assert len(refs) >= 2
    for ref in refs:
        assert (STORY.parent / ref.split('#')[0]).is_file(), ref
