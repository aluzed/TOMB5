"""Metadata-only publication and exact append-only history for RE781."""
import hashlib
import html
import re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
STORY = ROOT / 'docs/stories/RE-781-callback-height-producer-consumer.md'
DASH = ROOT / 'docs/reverse/reconstruction-progress.html'
MARKER = '<h3 id="re781">RE-781 ·'
BASE_SHA256 = '3f1d1175fbba2ebda8e9880532c10d0c02715bbb1d33db8b4ec2e7b63baeb171'

def test_re781_evidence_and_limits_are_separate():
    assert STORY.exists(), 'RED documentaire: story absente'
    dash = DASH.read_text()
    assert dash.count(MARKER) == 1
    section = html.unescape(dash.split(MARKER, 1)[1].split('</body>', 1)[0])
    for text in (STORY.read_text(), section):
        for token in ('26 septembre 2026', '288 cas', '114 échecs', 'zéro échec',
                      'BridgeFlatFloor', 'UpdateLaraRoom', 'adaptateur typé',
                      '108 cas', '27 callbacks', '144 cas', '144 callbacks',
                      'UBSan', 'exit 1', 'préexistant', 'int', 'long',
                      '305 draws', '90 appels', '90 retours', 'relink',
                      'pas de fullbuild neuf', 'callback non exercé dans le témoin',
                      '0→0 non discriminant', '7 échecs historiques', 'FAIL fade',
                      'pas de GREEN global', 'registration native non validée',
                      'modèle logiciel', 'Revue indépendante', 'Handoff actif'):
            assert token in text, token
        assert not re.search(r'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}', text)
        assert not re.search(r'<img\b|data:image|```(?:c|cpp|asm|mips)\b|<pre\b', text)
    assert '## Tracker' in STORY.read_text()
    assert '- [x]' in STORY.read_text() and '- [ ]' in STORY.read_text()

def test_re781_history_is_byte_exact():
    text = DASH.read_bytes()
    assert text.count(MARKER.encode()) == 1, 'RED documentaire: section absente'
    start = text.index(MARKER.encode())
    end = text.index(b'</body>', start)
    assert hashlib.sha256(text[:start] + text[end:]).hexdigest() == BASE_SHA256
    assert text.count(b'</body>') == text.count(b'</html>') == 1
