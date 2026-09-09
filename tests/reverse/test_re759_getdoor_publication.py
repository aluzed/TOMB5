"""Public documentary contract only: no private probe import or execution."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
STORY = ROOT / 'docs/stories/RE-759-getdoor-floor-data-proof.md'
DASHBOARD = ROOT / 'docs/reverse/reconstruction-progress.html'


def test_re759_scoped_proof_and_limits():
    assert STORY.exists(), 'RE759 story missing: expected documentary RED'
    story = STORY.read_text()
    dashboard = DASHBOARD.read_text()
    assert dashboard.count('<h2>RE-759 ·') == 1
    section = dashboard.split('<h2>RE-759 ·', 1)[1].split('<h2>', 1)[0].split('</body>', 1)[0]
    assert STORY.name in section
    for text in (story, section):
        for token in (
            '674 cas', '576', '98 chaînes', '642 différences de valeurs promues',
            '0 différence d’octet', '2 méthodes unittest', '17129 visites de hook',
            'pas des instructions retirées', 'vraie TU SPEC_PSXPC_N/GETSTUFF.C',
            'i386', '-m32 -O0', 'PSX_VERSION', 'PSXPC_TEST',
            'aucune équivalence ABI', 'aucun caller complet exécuté', 'aucun patch',
            'unsigned char', '16 bits', '255', 'pas testé comme destination',
            '17/128/254', 'EAX brut', 'images RAM non archivées',
            'pas de preuve gameplay', 'Revue indépendante PASS',
            'review/verdict.json', 'review/review.md', 'reviewer-01',
            'parent-01', '16:24:29.527416–16:24:33.431566', 'exit 0',
            'byte-identiques', 'aucun rejeu privé pendant cette publication',
            'gardes historiques inchangées', 'GetFloor', 'sélection de cellule', 'portail',
            'red.log', 'green.log', 'suite.log',
        ):
            assert token.casefold() in text.casefold(), token
        assert not re.search(r'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}', text)
        assert not re.search(r'```(?:c|cpp|asm|mips)\b|<pre\b', text)
        assert not re.search(r'(?:\\x[0-9a-fA-F]{2}){2,}|(?:\b[0-9A-Fa-f]{2} ){12,}', text)
        assert not re.search(r'(?i)\b(?:lui|addiu|sw|lw)\s+\$', text)
    for token in ('## Tracker', '## Handoff', '- [x]', '- [ ]', 'commands.json'):
        assert token in story
    handoff = dashboard.split('<h2>Suite de la recherche</h2>', 1)[1].split('<h2>', 1)[0]
    assert 'Après RE-759' in handoff
    assert 'GetFloor' in handoff
    assert 'Suivi au 9 septembre 2026, publication RE-759' in dashboard


def test_re759_historical_transition_preserved():
    dashboard = DASHBOARD.read_text()
    assert '<h2>RE-758 ·' in dashboard
    assert 'Après RE-758' in dashboard
    assert 'Suivi au 9 septembre 2026, intégration RE-758' in dashboard
