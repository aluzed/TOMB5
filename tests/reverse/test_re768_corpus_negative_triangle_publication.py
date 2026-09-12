"""Metadata-only contract: never imports or replays private proof."""
from pathlib import Path
import html
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
STORY = ROOT / 'docs/stories/RE-768-getfloor-corpus-negative-triangle-proof.md'
DASH = ROOT / 'docs/reverse/reconstruction-progress.html'
BASE = '2cba1d50eae37cd32e220c2eeaa0504f51cacec2'


def test_re768_bounded_claims_and_attribution():
    assert STORY.exists(), 'RED documentaire : story RE768 absente'
    dashboard = DASH.read_text()
    assert dashboard.count('<h2>RE-768 ·') == 1
    section = html.unescape(dashboard.split('<h2>RE-768 ·', 1)[1].split('<h2>', 1)[0].split('</body>', 1)[0])
    for text in (STORY.read_text(), section):
        for token in (
            'six appels directs GetFloor', 'zéro divergence',
            '243 rooms', '5824 cellules', '521688 octets',
            'entrée corpus 10', '7 → 15', 'index floor-data 891',
            'type 11 non nul', 'trois négatifs', 'trois positifs',
            'below/equal/above', 'seuil de room 15', 'deux transitions pit vers room 19',
            'RE767', 'index nul', 'arguments construits', 'aucun caller réel',
            'pas de gameplay', 'pas de matériel PSX', 'non exhaustif',
            '255 comme sentinelle', 'pas une destination explicite 255',
            '1193 visites de hooks', '153 lectures', 'huit stores inférés',
            'pas des instructions retirées', 'suffixe loader',
            'TU entière', 'Ghidra frais', '12 méthodes unittest',
            '18 fichiers comportementaux', 'interpréteur indépendant',
            '2097152 octets', 'six images RAM finales',
            'pas une émulation PSX complète', 'pas de trace exhaustive',
            're768-proof/HANDOFF.md', 're768-proof/COMMANDS.md',
            're768-review/rapport.md', 're768-review/verdict.json',
            're768-review/post-report-verification.json',
            'selon le contexte explicite de la délégation actuelle',
            'parent', 'aucun replay privé ni audit buffers parent dans ce tick à ce stade',
            'publisher', 'aucun rejeu privé', 'ELF32', '-m32 -O0',
            'PSX_VERSION=1', 'PSXPC_TEST=1', 'pas de sanitizer',
            'source de production inchangée', 'code_change_readiness=blocked',
            'gardes historiques inchangées', '17:40', '18:45',
            'revue finale de publication PASS au 12 septembre 2026 à 17:26 Europe/Paris',
            'RED documentaire', 'red.log', 'green.log', 'suite.log',
            'overview actif', 'Après RE-767', 'Après RE-768',
            'Prochaine recherche proposée', 'non commencée',
        ):
            assert token in text, token
        assert not re.search(r'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}|\b[0-9a-f]{64}\b', text)
        assert not re.search(r'```(?:c|cpp|asm|mips)\b|<pre\b|word_le_hex|payload_offset', text)
    assert '## Tracker' in STORY.read_text() and '## Handoff' in STORY.read_text()
    assert '- [x]' in STORY.read_text() and '- [ ]' in STORY.read_text()
    assert STORY.name in section


def test_re768_dashboard_exact_history():
    old = subprocess.check_output(['git', 'show', f'{BASE}:docs/reverse/reconstruction-progress.html'], cwd=ROOT)
    new = DASH.read_bytes()
    restored = re.sub(rb'<h2>RE-768 \xc2\xb7.*?(?=</body>)', b'', new, flags=re.S)
    assert restored == old, 'all predecessor bytes and closing tags must remain identical'
    sections = re.findall(rb'<h2>RE-\d+ \xc2\xb7.*?(?=<h2>|</body>)', old, re.S)
    assert sections
    for section in sections:
        assert section in new
    assert new.count(b'</body>') == old.count(b'</body>') == 1
    assert new.count(b'</html>') == old.count(b'</html>') == 1
