"""RE783 publication limits and exact append-only dashboard history."""
import hashlib, html, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
STORY = ROOT / 'docs/stories/RE-783-getceiling-bridge-registration.md'
DASH = ROOT / 'docs/reverse/reconstruction-progress.html'
MARKER = '<h3 id="re783">RE-783 ·'
BASE_SHA256 = '45789e11dec5c4b7b3aeb116e5a106e64af2202093d2f52b778f8185949d4c82'

def test_re783_evidence_and_limits():
    assert STORY.exists(), 'RED documentaire : story absente'
    dash = DASH.read_text()
    assert dash.count(MARKER) == 1, 'RED documentaire : section RE-783 absente'
    section = html.unescape(dash.split(MARKER, 1)[1].split('</body>', 1)[0])
    for text in (STORY.read_text(), section):
        for token in ('28 septembre 2026', '128 cas', '128 callbacks', 'BridgeFlatCeiling',
                      'BridgeTilt1Ceiling', 'BridgeTilt2Ceiling', 'PSX_VERSION', 'PSXPC_TEST',
                      'ObjectObjects', 'GetCeiling', '3072', 'modèle logiciel', 'synthétique',
                      'pas de runtime', 'publication', 'PENDING', '7 échecs', 'RE-778', 'fade',
                      'ILP32', '-m32', 'ELF64'):
            assert token in text, token
        assert not re.search(r'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}', text)
        assert not re.search(r'<img\b|data:image|```(?:c|cpp|asm|mips)\b|<pre\b', text)
    assert '## Tracker' in STORY.read_text()
    assert '- [x]' in STORY.read_text() and '- [ ]' in STORY.read_text()

def test_re783_history_is_byte_exact():
    text = DASH.read_bytes()
    assert text.count(MARKER.encode()) == 1, 'RED documentaire : section absente'
    start = text.index(MARKER.encode()); end = text.index(b'</body>', start)
    assert hashlib.sha256(text[:start] + text[end:]).hexdigest() == BASE_SHA256
    assert text.count(b'</body>') == text.count(b'</html>') == 1
