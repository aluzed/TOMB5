"""RE785 bounded publication and byte-exact preceding dashboard."""
import hashlib
import html
import re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
STORY = ROOT / 'docs/stories/RE-785-terminal-floor-records.md'
DASH = ROOT / 'docs/reverse/reconstruction-progress.html'
START = '<section id="re785">'
END = '<!-- end re785 -->'
BASE = 'e65d242591bbd4875756446fb53e1f813b03dcb7ca1b546f48cb1c22cb34fc46'


def test_re785_scope():
    assert STORY.exists(), 'RED documentaire: story absente'
    text = DASH.read_text()
    assert text.count(START) == text.count(END) == 1
    section = html.unescape(text.split(START)[1].split(END)[0])
    for data in (STORY.read_text(), section):
        for token in ('GetCeiling', '56', '21', 'UBSan', 'terminal', 'PSX_VERSION', 'PSXPC_TEST', 'pas de runtime', 'pas de GREEN global'):
            assert token in data, token
        assert not re.search(r'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}|data:image|<img\b|```(?:asm|mips|c|cpp)\b', data)
    assert '## Tracker' in STORY.read_text()
    assert '- [x]' in STORY.read_text() and '- [ ]' in STORY.read_text()


def test_re785_history():
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
    # Only RE788 is excluded; its own guard pins every preceding byte including RE787.
    successor_start, successor_end = b'<section id="re788">', b'<!-- end re788 -->'
    if successor_start in data:
        assert data.count(successor_start) == data.count(successor_end) == 1
        a = data.index(successor_start); b = data.index(successor_end, a) + len(successor_end)
        data = data[:a] + data[b:]
    # Only RE787 is excluded here; its own guard pins the complete preceding dashboard.
    successor_start, successor_end = b'<section id="re787">', b'<!-- end re787 -->'
    if successor_start in data:
        assert data.count(successor_start) == data.count(successor_end) == 1
        a = data.index(successor_start); b = data.index(successor_end, a) + len(successor_end)
        data = data[:a] + data[b:]
    # Only the named successor is excluded; RE786 proves the preceding bytes unchanged.
    successor_start, successor_end = b'<section id="re786">', b'<!-- end re786 -->'
    if successor_start in data:
        assert data.count(successor_start) == data.count(successor_end) == 1
        a = data.index(successor_start); b = data.index(successor_end, a) + len(successor_end)
        data = data[:a] + data[b:]
    start, end = START.encode(), END.encode()
    assert data.count(start) == data.count(end) == 1
    i = data.index(start); j = data.index(end) + len(end)
    assert hashlib.sha256(data[:i] + data[j:]).hexdigest() == BASE
    assert data.count(b'</html>') == data.count(b'</body>') == 1
