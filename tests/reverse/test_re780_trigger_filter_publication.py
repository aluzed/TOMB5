"""Public metadata contract; the separate actual-TU test compiles real source."""
import hashlib
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STORY = ROOT / 'docs/stories/RE-780-trigger-object-filter.md'
DASH = ROOT / 'docs/reverse/reconstruction-progress.html'
MARKER = '<h3 id="re780">RE-780 ·'
BASE_SHA256 = 'f9f9b0aec047d379cbe19374fe11904985528759ea7828a5d7eefb64e089ea66'


def section():
    text = DASH.read_text(encoding='utf-8')
    assert text.count(MARKER) == 1, 'RED documentaire : section RE-780 absente'
    return html.unescape(text.split(MARKER, 1)[1].split('</body>', 1)[0])


def test_re780_separates_evidence_and_unresolved_contract():
    assert STORY.exists(), 'RED documentaire : story RE-780 absente'
    for text in (STORY.read_text(encoding='utf-8'), section()):
        for token in (
            'Après RE-779', 'Après RE-780', '25 septembre 2026',
            'correction réelle du filtre objet', 'quatre lignes',
            'Preuve native', 'ancien binaire', '305 draws', 'draw300',
            'callback nul', '0→0', 'non discriminant',
            'Preuve cible', '48 retours', '2 frontières',
            'Preuve synthétique', '153 cas', '42 échecs', '24 observations',
            'Revue indépendante', 'callbacks non nuls non réparés',
            'initialisation', 'propagation', 'fullbuild neuf bloqué',
            '124', 'SIGKILL', 'callback producer/consumer',
            '7 échecs historiques', 'FAIL fade', 'pas de GREEN global',
            'équivalence complète bloquée', 'gameplay complet non validé',
            'aucun asset public', 'RED documentaire',
        ):
            assert token in text, token
        assert not re.search(r'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}', text)
        assert not re.search(r'<img\b|data:image|```(?:c|cpp|asm|mips)\b|<pre\b', text)
    story = STORY.read_text(encoding='utf-8')
    assert '## Tracker' in story and '## Handoff' in story
    assert '- [x]' in story and '- [ ]' in story


def test_re780_preserves_dashboard_bytes_and_active_handoff():
    text = DASH.read_bytes()
    assert text.count(MARKER.encode()) == 1, 'RED documentaire : section RE-780 absente'
    start = text.index(MARKER.encode())
    end = text.index(b'</body>', start)
    assert hashlib.sha256(text[:start] + text[end:]).hexdigest() == BASE_SHA256
    assert text.count(b'</body>') == text.count(b'</html>') == 1
    for token in ('Overview actif', 'Handoff actif', STORY.name,
                  'autonomy-20260925-publication-0928'):
        assert token in section()


def test_re780_fixture_readme_has_real_public_invocation():
    text = (ROOT / 'tests/reverse/fixtures/re780/README.md').read_text(encoding='utf-8')
    assert 'proposition' not in text.lower()
    assert 'CHEMIN' not in text
    assert 'python3 tests/reverse/fixtures/re780/run_test.py' in text
    assert '--source SPEC_PSXPC_N/GETSTUFF.C' in text
    assert '--output build/reverse/' in text
    assert 'callbacks non nuls non réparés' in text
