"""Public metadata contract; no private evidence imports or probe execution."""
from pathlib import Path
import html
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
STORY = ROOT / 'docs/stories/RE-767-getfloor-corpus-composition-proof.md'
DASH = ROOT / 'docs/reverse/reconstruction-progress.html'
BASE = '307eb67f3c05ddc99fd0b596049f62f82428cf55'


def test_re767_bounded_corpus_claims():
    assert STORY.exists(), 'RED documentaire : story RE767 absente'
    dashboard = DASH.read_text()
    assert dashboard.count('<h2>RE-767 ·') == 1
    section = html.unescape(dashboard.split('<h2>RE-767 ·', 1)[1].split('<h2>', 1)[0].split('</body>', 1)[0])
    for text in (STORY.read_text(), section):
        for token in (
            'huit appels directs GetFloor', 'zéro divergence',
            'door, portal, door, floor, pit', 'intersection et union nulles',
            '243 rooms', '5824 cellules', '521688 octets',
            '3065 requêtes de modèle', 'pas des appels cible',
            'index floor-data nul', 'aucun triangle négatif',
            'aucun caller réel', 'arguments construits', 'non exhaustif',
            '222/223', 'pas de destination explicite 255',
            'pas de sky', 'multi-pit', 'contrôle négatif de non-traversée',
            '1444 visites de hook', '224 lectures', '16 stores inférés',
            'pas des instructions matériellement retirées',
            'suffixe loader', 'pas un loader complet',
            'TU entière', 'Ghidra frais', 'cinq méthodes unittest',
            '12 fichiers comportementaux', 'pas une deuxième émulation CPU',
            're767-corpus/HANDOFF.md', 're767-corpus/COMMANDS.md',
            're767-review/rapport.md', 're767-review/verdict.json',
            're767-review/final-verification.json',
            'reviewer', 'parent', 'selon le contexte explicite',
            'dans ce tick', 'aucun replay ni audit buffers parent',
            'ELF32', '-m32 -O0', 'PSX_VERSION=1', 'PSXPC_TEST=1',
            'pas de sanitizer', 'pas de trace exhaustive',
            'source de production inchangée', 'readiness inchangée',
            'gardes historiques inchangées', 'garde expirée',
            'aucun rejeu privé',
            'revue finale de publication PASS au 11 septembre 2026 à 21:49 Europe/Paris',
            'RED documentaire', 'red.log', 'green.log', 'suite.log',
            'overview actif', 'Après RE-766', 'Après RE-767',
            'Prochaine recherche proposée', 'non commencée',
        ):
            assert token in text, token
        assert not re.search(r'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}', text)
        assert not re.search(r'```(?:c|cpp|asm|mips)\b|<pre\b', text)
    assert '## Tracker' in STORY.read_text() and '## Handoff' in STORY.read_text()
    assert '- [x]' in STORY.read_text() and '- [ ]' in STORY.read_text()
    assert STORY.name in section


def test_re767_dashboard_exact_history():
    old = subprocess.check_output(['git', 'show', f'{BASE}:docs/reverse/reconstruction-progress.html'], cwd=ROOT)
    new = DASH.read_bytes()
    restored = re.sub(rb'<h2>RE-767 \xc2\xb7.*?(?=</body>)', b'', new, flags=re.S)
    assert restored == old, 'all historical bytes including closing tags must remain identical'
    sections = re.findall(rb'<h2>RE-\d+ \xc2\xb7.*?(?=<h2>|</body>)', old, re.S)
    assert sections
    for section in sections:
        assert section in new
