"""RE782 publication limits and exact append-only dashboard history."""
import hashlib
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STORY = ROOT / 'docs/stories/RE-782-bridge-ceiling-contract.md'
DASH = ROOT / 'docs/reverse/reconstruction-progress.html'
MARKER = '<h3 id="re782">RE-782 ·'
BASE_SHA256 = '0a66032386a136841688abceb767a56689464031b686c2943a9114a01d56c98d'


def test_re782_evidence_and_limits():
    assert STORY.exists(), 'RED documentaire : story absente'
    dash = DASH.read_text()
    assert dash.count(MARKER) == 1
    section = html.unescape(dash.split(MARKER, 1)[1].split('</body>', 1)[0])
    for text in (STORY.read_text(), section):
        for token in ('27 septembre 2026', '1260 cas', '630 échecs', 'zéro échec',
                      'BridgeFlatCeiling', 'BridgeTilt1Ceiling', 'BridgeTilt2Ceiling',
                      'PSX_VERSION', 'PSXPC_TEST', 'égalité exclue', '256',
                      'ObjectObjects', 'registration absente', 'int/long',
                      'GetCeiling', 'NULL', 'Ghidra', 'modèle logiciel',
                      'Revue indépendante', 'UBSan', 'GetFloor',
                      'pas de runtime jeu', 'pas de GREEN global', 'Handoff actif'):
            assert token in text, token
        assert not re.search(r'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}', text)
        assert not re.search(r'<img\b|data:image|```(?:c|cpp|asm|mips)\b|<pre\b', text)
    assert '## Tracker' in STORY.read_text()
    assert '- [x]' in STORY.read_text() and '- [ ]' in STORY.read_text()


def test_re782_history_is_byte_exact():
    text = DASH.read_bytes()
    assert text.count(MARKER.encode()) == 1, 'RED documentaire : section absente'
    start = text.index(MARKER.encode())
    end = text.index(b'</body>', start)
    assert hashlib.sha256(text[:start] + text[end:]).hexdigest() == BASE_SHA256
    assert text.count(b'</body>') == text.count(b'</html>') == 1
