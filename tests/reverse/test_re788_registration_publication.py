"""RE788 source integration scope and byte-exact preservation of prior dashboard."""
import hashlib
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STORY = ROOT / 'docs/stories/RE-788-roof-real-registration.md'
DASH = ROOT / 'docs/reverse/reconstruction-progress.html'
REVIEW = ROOT / 'docs/reverse/generated/re788-source-review.json'
START, END = '<section id="re788">', '<!-- end re788 -->'
BASE = 'c8816137c9684ebca6e6dcd9ec40ca47a9850f2a4d7a980598153f17014184ff'


def test_source_only_scope_and_remaining_work():
    assert STORY.exists(), 'RED documentaire : story absente'
    text = DASH.read_text()
    assert text.count(START) == text.count(END) == 1
    section = html.unescape(text.split(START, 1)[1].split(END, 1)[0])
    for data in (STORY.read_text(), section):
        for token in ('ObjectObjects', 'GetCeiling', '13824', '3456', 'zéro divergence de retour',
                      'UBSan', 'PSX_VERSION', 'PSXPC_TEST', 'i386', 'source-only',
                      'pas de runtime', 'pas de GREEN global', 'registration', 'RE-789'):
            assert token in data, token
        assert not re.search(r'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}|data:image|<img\b|```(?:asm|mips|c|cpp)\b', data)
    assert '## Tracker' in STORY.read_text()
    assert '- [x]' in STORY.read_text() and '- [ ]' in STORY.read_text()
    assert '../stories/RE-788-roof-real-registration.md' in section


def test_preceding_dashboard_bytes_unchanged():
    data = DASH.read_bytes()
    # Only the named RE790 successor is excluded; its own guard pins all previous bytes.
    successor_start, successor_end = b'<section id="re790">', b'<!-- end re790 -->'
    if successor_start in data:
        assert data.count(successor_start) == data.count(successor_end) == 1
        a = data.index(successor_start); b = data.index(successor_end, a) + len(successor_end)
        data = data[:a] + data[b:]
    # Only RE789 is excluded; its successor guard pins all preceding bytes including RE788.
    successor_start, successor_end = b'<section id="re789">', b'<!-- end re789 -->'
    if successor_start in data:
        assert data.count(successor_start) == data.count(successor_end) == 1
        a = data.index(successor_start); b = data.index(successor_end, a) + len(successor_end)
        data = data[:a] + data[b:]
    start, end = START.encode(), END.encode()
    assert data.count(start) == data.count(end) == 1
    a = data.index(start)
    b = data.index(end, a) + len(end)
    assert hashlib.sha256(data[:a] + data[b:]).hexdigest() == BASE
    assert data.count(b'</html>') == data.count(b'</body>') == 1


def test_persisted_scoped_review_matches_source_files():
    assert REVIEW.exists(), 'RED documentaire : revue publique absente'
    review = json.loads(REVIEW.read_text())
    assert review['passed'] is True
    assert review['security_concerns'] == review['logic_errors'] == []
    assert review['scope'] == 'source-only-synthetic-i386'
    assert review['limits'] and review['validation']['pytest_exit'] == 0
    assert review['validation']['pytest_tests'] == 4
    files = review['validation']['sha256']
    assert set(files) == {'tests/reverse/test_re788_roof_registration.py',
                          'tests/reverse/fixtures/re788/run_test.py',
                          'tests/reverse/fixtures/re788/roof_registration.cpp'}
    for name, digest in files.items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest
