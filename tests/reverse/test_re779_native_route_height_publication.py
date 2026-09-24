"""Metadata-only publication contract: no private evidence or runtime imports."""
import hashlib
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STORY = ROOT / 'docs/stories/RE-779-native-route-height-attribution.md'
DASH = ROOT / 'docs/reverse/reconstruction-progress.html'
BASE_SHA256 = '0ba3eca5cd70cc054478ff1eb478c0fcf15b1a79db18a300fa443a199f44d1d8'
MARKER = '<h2>RE-779 ·'


def section():
    text = DASH.read_text(encoding='utf-8')
    assert text.count(MARKER) == 1, 'RED documentaire : section RE-779 absente'
    current = text.split(MARKER, 1)[1].split('</body>', 1)[0]
    assert '<h2>' not in current, 'RE-779 must remain a bounded latest section'
    return html.unescape(current)


def test_re779_story_and_section_publish_bounded_evidence():
    assert STORY.exists(), 'RED documentaire : story RE-779 absente'
    for text in (STORY.read_text(encoding='utf-8'), section()):
        for token in (
            'Après RE-778', 'Après RE-779', '24 septembre 2026',
            '1062 draws', '0→2→0', 'KillMoveItems', '762', '822', '171',
            '8 PASS / 1 FAIL', 'entrée du draw16', 'présentation',
            '6 appels', 'Ghidra', 'draw401', '1834', '1836',
            '(46592,-376,35857)', 'room2', 'cellule8', 'index40',
            'retour5', 'item.floor5', '10692 octets', 'borne corpus',
            'LoadLevel', 'S_LoadLevelFile', 'DoLevel', 'Name=1',
            'pente simple terminale', 'sans pit', '402 draws',
            'cible archivée', 'pas de rebuild', 'pas une sortie naturelle du jeu',
            'source de production inchangée', 'code_change_readiness=blocked',
            'gameplay complet non validé', 'équivalence universelle non établie',
            '7 échecs historiques', 'RED documentaire', 'aucun asset public',
        ):
            assert token in text, token
        assert not re.search(r'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}', text)
        assert not re.search(r'<img\b|data:image|```(?:c|cpp|asm|mips)\b|<pre\b', text)
    story = STORY.read_text(encoding='utf-8')
    assert '## Tracker' in story and '## Handoff' in story
    assert '- [x]' in story and '- [ ]' in story
    assert 'pas une revue indépendante' in story
    assert 'RED de setup' in story and 'pas comportemental' in story
    assert STORY.name in section()


def test_re779_preserves_exact_predecessor_dashboard():
    text = DASH.read_bytes()
    marker = MARKER.encode()
    assert text.count(marker) == 1, 'RED documentaire : section RE-779 absente'
    start = text.index(marker)
    end = text.index(b'</body>', start)
    restored = text[:start] + text[end:]
    assert hashlib.sha256(restored).hexdigest() == BASE_SHA256
    assert text.count(b'</body>') == text.count(b'</html>') == 1


def test_re779_new_section_has_active_overview_and_handoff():
    text = section()
    assert 'Overview actif' in text and 'Handoff actif' in text
    assert 'RE-779-native-route-height-attribution.md' in text
    assert 'autonomy-20260924-publication-0955' in text
    assert 'sans lancement ni replay privé' in text
