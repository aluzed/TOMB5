"""RE-784 publication contract, metadata-only and append-only historical bytes."""
import hashlib
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STORY = ROOT / 'docs/stories/RE-784-signed-base-heights.md'
DASH = ROOT / 'docs/reverse/reconstruction-progress.html'
START = '<section id="re784">'
END = '<!-- end re784 -->'
BASE = 'cc703675c09cab3cc01a05cf33091279713e22d62131c485543208304df35204'


def test_re784_publication_scope():
    assert STORY.exists(), 'RED documentaire: story absente'
    dashboard = DASH.read_text()
    assert dashboard.count(START) == 1 and dashboard.count(END) == 1
    section = html.unescape(dashboard.split(START, 1)[1].split(END, 1)[0])
    for text in (STORY.read_text(), section):
        for token in ('30 septembre 2026', 'GetHeight', 'GetCeiling', '512', '256',
                      'PSX_VERSION', 'PSXPC_TEST', 'UBSan', 'sentinelle',
                      'char', 'index nul', 'pas de runtime', 'pas de GREEN global'):
            assert token in text, token
        assert not re.search(r'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}|<img\b|data:image|```(?:c|cpp|asm|mips)\b', text)
    assert '## Tracker' in STORY.read_text()
    assert '- [x]' in STORY.read_text() and '- [ ]' in STORY.read_text()


def test_re784_history_byte_exact():
    data = DASH.read_bytes()
    # Exclude only RE794; its own guard pins every preceding dashboard byte.
    successor_start, successor_end = b'<section id="re794">', b'<!-- end re794 -->'
    if successor_start in data:
        assert data.count(successor_start) == data.count(successor_end) == 1
        a = data.index(successor_start)
        b = data.index(successor_end, a) + len(successor_end)
        data = data[:a] + data[b:]
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
    # The explicitly authorized successor has its own byte-exact history guard.
    successor_start, successor_end = b'<section id="re785">', b'<!-- end re785 -->'
    if successor_start in data:
        assert data.count(successor_start) == data.count(successor_end) == 1
        a = data.index(successor_start); b = data.index(successor_end, a) + len(successor_end)
        data = data[:a] + data[b:]
    start, end = START.encode(), END.encode()
    assert data.count(start) == data.count(end) == 1
    i = data.index(start); j = data.index(end, i) + len(end)
    assert hashlib.sha256(data[:i] + data[j:]).hexdigest() == BASE
    assert data.count(b'</body>') == data.count(b'</html>') == 1
