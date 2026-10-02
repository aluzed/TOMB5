"""RE787 documentary contract; predecessor dashboard pinned without modification."""
import hashlib
import html
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
STORY=ROOT/'docs/stories/RE-787-signed-roof-callback-offset.md'
DASH=ROOT/'docs/reverse/reconstruction-progress.html'
START='<section id="re787">'
END='<!-- end re787 -->'
BASE='c5a150fbf5dffc5a909c65ccdeb5e187e47dc3b8f63c06d6081525dec7f40256'


def test_re787_scope():
    assert STORY.exists(), 'RED documentaire story absente'
    text=DASH.read_text()
    assert text.count(START)==text.count(END)==1
    section=html.unescape(text.split(START)[1].split(END)[0])
    for data in (STORY.read_text(),section):
        for token in ('GetCeiling','7680','2304','309','UBSan','PSX_VERSION','PSXPC_TEST','offset signé','adaptateur','registration','pas de runtime','pas de GREEN global'):
            assert token in data,token
        assert not re.search(r'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}|data:image|<img\b|```(?:asm|mips|c|cpp)\b',data)
    assert '## Tracker' in STORY.read_text()
    assert '- [x]' in STORY.read_text() and '- [ ]' in STORY.read_text()
    assert '../stories/RE-787-signed-roof-callback-offset.md' in section


def test_re787_history_byte_exact():
    data=DASH.read_bytes()
    # Only RE788 is excluded; its own guard pins every preceding byte including RE787.
    successor_start, successor_end = b'<section id="re788">', b'<!-- end re788 -->'
    if successor_start in data:
        assert data.count(successor_start) == data.count(successor_end) == 1
        a = data.index(successor_start); b = data.index(successor_end, a) + len(successor_end)
        data = data[:a] + data[b:]
    start,end=START.encode(),END.encode()
    assert data.count(start)==data.count(end)==1
    i=data.index(start);j=data.index(end)+len(end)
    assert hashlib.sha256(data[:i]+data[j:]).hexdigest()==BASE
    assert data.count(b'</html>')==data.count(b'</body>')==1
