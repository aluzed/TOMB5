"""RE786 metadata-only publication with byte-exact previous dashboard."""
import hashlib
import html
import re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
STORY = ROOT / 'docs/stories/RE-786-roof-triangle-family.md'
DASH = ROOT / 'docs/reverse/reconstruction-progress.html'
START = '<section id="re786">'
END = '<!-- end re786 -->'
BASE = '9e04bda00160a042c2b2f7fa89995b5a29d5c0d9ed347a8fa61c3008d3eb70fd'


def test_re786_scope():
    assert STORY.exists(), 'RED documentaire: story absente'
    text = DASH.read_text()
    assert text.count(START) == text.count(END) == 1
    section = html.unescape(text.split(START)[1].split(END)[0])
    for data in (STORY.read_text(), section):
        for token in ('GetCeiling', '1536', '256', 'UBSan', 'type 10', 'PSX_VERSION', 'PSXPC_TEST', 'offsets négatifs', 'callbacks exclus', 'pas de runtime', 'pas de GREEN global'):
            assert token in data, token
        assert not re.search(r'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}|data:image|<img\b|```(?:asm|mips|c|cpp)\b', data)
    assert '## Tracker' in STORY.read_text()
    assert '- [x]' in STORY.read_text() and '- [ ]' in STORY.read_text()


def test_re786_history():
    data = DASH.read_bytes()
    start, end = START.encode(), END.encode()
    assert data.count(start) == data.count(end) == 1
    i = data.index(start); j = data.index(end) + len(end)
    assert hashlib.sha256(data[:i] + data[j:]).hexdigest() == BASE
    assert data.count(b'</html>') == data.count(b'</body>') == 1
