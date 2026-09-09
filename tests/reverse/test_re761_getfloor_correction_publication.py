"""RE761 public documentary contract: no private inputs or probe execution."""
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
STORY = ROOT / 'docs/stories/RE-761-getfloor-clamp-private-correction.md'
DASHBOARD = ROOT / 'docs/reverse/reconstruction-progress.html'
BASE = 'e07466efcf4b3e5d0c394b4b8a0e8edc2b222bf2'


def test_re761_private_correction_and_separate_attribution():
    assert STORY.exists(), 'RE761 story missing: expected documentary RED'
    story = STORY.read_text()
    dashboard = DASHBOARD.read_text()
    assert dashboard.count('<h2>RE-761 ·') == 1
    section = dashboard.split('<h2>RE-761 ·', 1)[1].split('</body>', 1)[0]
    assert STORY.name in section
    for text in (story, section):
        for token in (
            'preuve corrective PRIVÉE', '1944 cas', '216 échecs de sous-tests',
            '72 divergences finales', '144 divergences intermédiaires',
            '144 cas distincts', 'intersection 72', '3 méthodes unittest',
            'zéro divergence finale et intermédiaire', 'dx = 1',
            'SPEC_PSXPC_N/GETSTUFF.C', 'source de production inchangée',
            '2916 entrées GetDoor', '206640 visites de hook',
            '28836 événements de lecture cible', '3888 paires RAM complètes',
            '3888 paires de buffers natifs', 'Revue indépendante PASS',
            'review/rapport.md', 'review/verdict.json', 'review/independent_audit.py',
            'reviewer-01', 'parent-01', '18:20:28.640767–18:22:12.885740',
            '104.244974 s', 'parent n’a pas exécuté l’audit indépendant',
            'attribution historique codée en dur', 'byte-identiques',
            'deux géométries synthétiques', '255', 'unsigned char',
            'i386', '-m32 -O0', 'pas de sanitizers', 'chaînes verticales',
            'pas de preuve gameplay', 'domain proof', 'largeur des IDs exclue',
            'intégration au backend attribué', 'régression TU publique',
            'aucun rejeu privé pendant cette publication', 'gardes historiques inchangées',
            'red.log', 'green.log', 'suite.log', 'commands.json',
        ):
            assert token.casefold() in text.casefold(), token
        assert not re.search(r'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}', text)
        assert not re.search(r'```(?:c|cpp|asm|mips)\b|<pre\b', text)
        assert not re.search(r'(?:\\x[0-9a-fA-F]{2}){2,}|(?:\b[0-9A-Fa-f]{2} ){12,}', text)
    for token in ('## Tracker', '## Handoff', '- [x]', '- [ ]'):
        assert token in story
    assert 'Suivi au 9 septembre 2026, publication RE-761' in dashboard
    handoff = dashboard.split('<h2>Suite de la recherche</h2>', 1)[1].split('<h2>', 1)[0]
    assert 'Après RE-761' in handoff
    assert 'Après RE-760' in handoff and 'Après RE-759' in handoff
    assert 'intégration au backend attribué' in handoff


def test_re761_only_active_overview_handoff_and_new_section_change():
    old = subprocess.check_output(['git', 'show', f'{BASE}:docs/reverse/reconstruction-progress.html'], cwd=ROOT)
    new = DASHBOARD.read_bytes()
    def normalize(data):
        data = re.sub(rb'<h2>RE-761 \xc2\xb7.*?(?=</body>)', b'', data, flags=re.S)
        data = re.sub(rb'(?<=<h1>TOMB5 \xe2\x80\x94 Reconstruction fond\xc3\xa9e sur le binaire</h1>\n).*?(?=<h2>)', b'OVERVIEW\n', data, count=1, flags=re.S)
        return re.sub(rb'(?<=<h2>Suite de la recherche</h2>\n)<p>.*?</p>', b'HANDOFF', data, count=1, flags=re.S)
    assert normalize(new) == normalize(old), 'historical dashboard bytes changed'
    old_sections = dict(re.findall(rb'(<h2>(RE-\d+) \xc2\xb7.*?)(?=<h2>|</body>)', old, re.S))
    for section in old_sections:
        assert section in new
