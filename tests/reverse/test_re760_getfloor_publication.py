"""Public RE760 documentation only; never imports or executes private proofs."""
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
STORY = ROOT / 'docs/stories/RE-760-getfloor-selection-portal-proof.md'
DASHBOARD = ROOT / 'docs/reverse/reconstruction-progress.html'
BASE = '5f5b3515a7380e8db3043043650a8cc8b02156a6'


def test_re760_scoped_characterization_and_attribution():
    assert STORY.exists(), 'RE760 story missing: expected documentary RED'
    story = STORY.read_text()
    dashboard = DASHBOARD.read_text()
    assert dashboard.count('<h2>RE-760 ·') == 1
    section = dashboard.split('<h2>RE-760 ·', 1)[1].split('<h2>', 1)[0].split('</body>', 1)[0]
    assert STORY.name in section
    for text in (story, section):
        for token in (
            '3888 cas', '1044 triplets divergents', '972 différences room_number',
            '555 différences d’indice de cellule', '2844 accords', '489 room seule',
            '483 room et cellule', '72 cellule seule', 'PAS équivalence',
            '470232 visites de hook', 'pas des instructions retirées',
            '6804 entrées cibles GetDoor', '2916 visites de store', 'stores inférés',
            '3 méthodes unittest', 'pas un RED comportemental',
            '255 explicitement testé comme destination DOOR', 'short négatif',
            'unsigned char', '16 bits signés', 'clamp haut Z', 'domain proof',
            'vraie TU SPEC_PSXPC_N/GETSTUFF.C', 'i386', '-m32 -O0',
            'GetFloor entrée→retour', 'GetDoor réellement exécuté',
            'images RAM non archivées', 'aucun caller englobant',
            'helpers triangle non exécutés', 'aucun patch', 'pas de preuve gameplay',
            'Revue indépendante PASS', 'review/verdict.json', 'review/audit.py',
            'parent-01', '17:19:20.619538–17:20:17.882597',
            'parent n’a pas exécuté l’audit indépendant', 'byte-identiques',
            'aucun rejeu privé pendant cette publication', 'gardes historiques inchangées',
            'red.log', 'green.log', 'suite.log',
        ):
            assert token.casefold() in text.casefold(), token
        assert not re.search(r'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}', text)
        assert not re.search(r'```(?:c|cpp|asm|mips)\b|<pre\b', text)
        assert not re.search(r'(?:\\x[0-9a-fA-F]{2}){2,}|(?:\b[0-9A-Fa-f]{2} ){12,}', text)
        assert not re.search(r'(?i)\b(?:lui|addiu|sw|lw)\s+\$', text)
    for token in ('## Tracker', '## Handoff', '- [x]', '- [ ]', 'commands.json'):
        assert token in story
    assert 'Suivi au 9 septembre 2026, publication RE-760' in dashboard
    handoff = dashboard.split('<h2>Suite de la recherche</h2>', 1)[1].split('<h2>', 1)[0]
    assert 'Après RE-760' in handoff
    assert 'clamp haut Z' in handoff
    assert 'Après RE-759' in handoff


def test_re760_historical_sections_byte_identical():
    old = subprocess.check_output(['git', 'show', f'{BASE}:docs/reverse/reconstruction-progress.html'], cwd=ROOT)
    new = DASHBOARD.read_bytes()
    def sections(data):
        return {m.group(1): m.group(0) for m in re.finditer(
            rb'<h2>(RE-\d+) \xc2\xb7.*?(?=<h2>|</body>)', data, re.S)}
    before, after = sections(old), sections(new)
    assert before
    for ticket, content in before.items():
        assert after[ticket] == content, ticket.decode()
