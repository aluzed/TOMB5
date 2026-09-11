"""Public documentary contract only; never reads or executes private proof."""
from pathlib import Path
import html
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
STORY = ROOT / 'docs/stories/RE-766-getfloor-multihop-proof.md'
DASH = ROOT / 'docs/reverse/reconstruction-progress.html'
BASE = '81a74392b056d890c6e28c62a9bb3a58ade116a9'


def test_re766_bounded_claims_and_attribution():
    assert STORY.exists(), 'RED documentaire : story RE766 absente'
    dashboard = DASH.read_text()
    assert dashboard.count('<h2>RE-766 ·') == 1
    section = html.unescape(dashboard.split('<h2>RE-766 ·', 1)[1].split('<h2>', 1)[0].split('</body>', 1)[0])
    for text in (STORY.read_text(), section):
        for token in (
            '22680 appels', '22140 entrées distinctes', '15876 GetFloor',
            '6804 helpers', '36 fixtures', 'zéro divergence',
            '0/1/2/3', 'portails préfixes', 'atterrissage',
            '253 fichiers comportementaux', 'six tests privés',
            're766-multihop/HANDOFF.md', 're766-independent-review/review.md',
            're766-independent-review/verdict.json',
            'auteur', 'reviewer', 'parent', 'pas de replay ni audit parent',
            'aucune comparaison de buffers parent',
            'TU entière', 'Ghidra frais', 'PSX_VERSION=1', 'PSXPC_TEST=1',
            '-m32 -O0', 'GetDoor', 'unsigned char', 'normalisation 16 bits',
            'synthétiques', 'pas de corpus', 'pas de gameplay',
            'pas de sanitizer', 'pas de trace exhaustive',
            'visites de hook', 'pas un oracle matériel',
            'source de production inchangée', 'gardes historiques inchangées',
            '21:10', 'aucun rejeu privé', 'RED documentaire',
            'red.log', 'green.log', 'suite.log', 'overview actif',
            'Après RE-765', 'Après RE-766', 'Prochaine recherche proposée',
            'consommateur réel GetFloor', 'non commencée',
        ):
            assert token in text, token
        assert not re.search(r'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}', text)
        assert not re.search(r'```(?:c|cpp|asm|mips)\b|<pre\b', text)
    assert '## Tracker' in STORY.read_text() and '## Handoff' in STORY.read_text()
    assert '- [x]' in STORY.read_text() and '- [ ]' in STORY.read_text()
    assert STORY.name in section


def test_re766_dashboard_exact_history():
    old = subprocess.check_output(['git', 'show', f'{BASE}:docs/reverse/reconstruction-progress.html'], cwd=ROOT)
    new = DASH.read_bytes()
    restored = re.sub(rb'<h2>RE-766 \xc2\xb7.*?(?=</body>)', b'', new, flags=re.S)
    assert restored == old, 'historical bytes including closing tags must remain identical'
    sections = re.findall(rb'<h2>RE-\d+ \xc2\xb7.*?(?=<h2>|</body>)', old, re.S)
    assert sections
    for section in sections:
        assert section in new
