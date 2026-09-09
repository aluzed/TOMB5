"""Publication documentaire uniquement : aucun asset ni rejeu privé."""
from pathlib import Path
import html
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
STORY = ROOT / 'docs/stories/RE-764-getfloor-vertical-triangle-proof.md'
DASH = ROOT / 'docs/reverse/reconstruction-progress.html'
BASE = 'e2900d026ab3202ed409f0ea280162bbbcc54f9b'


def test_re764_claims_are_scoped_and_qualified():
    assert STORY.exists(), 'RED documentaire attendu : story RE764 absente'
    story = STORY.read_text()
    dashboard = DASH.read_text()
    assert dashboard.count('<h2>RE-764 ·') == 1
    section = html.unescape(dashboard.split('<h2>RE-764 ·', 1)[1].split('<h2>', 1)[0].split('</body>', 1)[0])
    for text in (story, section):
        for token in (
            'PASS de caractérisation', 'équivalence réfutée',
            '15 niveaux', '2704 rooms', '91444 cellules',
            '615 appels de helpers', 'zéro différence',
            '1605 requêtes verticales', '172 cas divergents',
            'intersection = union = 172', 'pas 344',
            'y < current-room minfloor', 'y >= room-zero minfloor',
            'helper négatif', '32 bits O0', 'pas un sanitizer',
            'matrice représentative non exhaustive', 'aucune transition portail',
            'second interpréteur logiciel', 'pas un oracle matériel',
            'pas de dumps RAM complets par appel',
            'frontières de fonctions', 'pas de trace native exhaustive',
            'review/clarification.json', 'verdict original invalide conservé',
            'tableaux bloquants vides', 'parent/run-invocation.json',
            '21:02:25.753374–21:02:43.708125', 'moteur enfant',
            '3 tests privés', '151 fichiers comportementaux',
            'parent-comparison.json', 'identité octet par octet',
            'parent n’a pas relancé l’audit indépendant du reviewer',
            'aucun rejeu privé pendant cette publication',
            'source de production inchangée', 'gardes historiques inchangées',
            'RED comportemental sur la vraie TU', 'correction privée',
            'current-room et room-zero', 'seuils inférieur, égal et supérieur',
            'pas de passage en production', 'red.log', 'green.log', 'suite.log',
        ):
            assert token in text, token
        assert not re.search(r'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}', text)
        assert not re.search(r'```(?:c|cpp|asm|mips)\b|<pre\b', text)
    assert STORY.name in section
    assert '## Tracker' in story and '## Handoff' in story
    assert '- [x]' in story and '- [ ]' in story


def test_re764_preserves_every_historical_section_byte_for_byte():
    old = subprocess.check_output(['git', 'show', f'{BASE}:docs/reverse/reconstruction-progress.html'], cwd=ROOT)
    new = DASH.read_bytes()
    restored = re.sub(rb'<h2>RE-764 \xc2\xb7.*?(?=</body>)', b'', new, flags=re.S)
    assert restored == old, 'seul ajout RE764 autorisé ; historique intégral immuable'
    sections = re.findall(rb'<h2>RE-\d+ \xc2\xb7.*?(?=<h2>|</body>)', old, re.S)
    assert sections
    for section in sections:
        assert section in new, 'section historique altérée'
