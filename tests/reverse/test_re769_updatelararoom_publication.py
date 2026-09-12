"""Public metadata-only contract; no private proof imports or execution."""
from pathlib import Path
import html
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
STORY = ROOT / 'docs/stories/RE-769-updatelararoom-caller-proof.md'
DASH = ROOT / 'docs/reverse/reconstruction-progress.html'
BASE = 'c8303f6e3a0ed075f8e3886b6c13a03235d5c0e9'


def test_re769_bounded_claims_and_attribution():
    assert STORY.exists(), 'RED documentaire : story RE769 absente'
    dashboard = DASH.read_text()
    assert dashboard.count('<h2>RE-769 ·') == 1
    section = html.unescape(dashboard.split('<h2>RE-769 ·', 1)[1].split('<h2>', 1)[0].split('</body>', 1)[0])
    for text in (STORY.read_text(), section):
        for token in (
            'PASS privé borné', 'UpdateLaraRoom', 'GetFloor', 'GetHeight',
            'deux contrôles alias/non-alias', 'une divergence x/z',
            'zéro divergence GetFloor', 'cinq événements ordonnés',
            'door → portal → door → floor → pit',
            'item', 'lara_item', 'arguments construits',
            'même état cible pertinent', 'pas deux scénarios cible distincts',
            'stop à l’entrée GetHeight', 'aucune instruction de GetHeight',
            'pas de lecture du record', 'pas de hauteur finale',
            'pas de store item.floor', 'pas de retour complet UpdateLaraRoom',
            'préconditions alias/caller', 'non-alias atteignable en jeu non établi',
            'pas de gameplay', 'pas de matériel', 'pas d’équivalence universelle',
            '521688 octets', '2097152 octets', '288 octets',
            '235 visites', '36 lectures', 'six stores inférés',
            'pas des instructions retirées', 'suffixe loader',
            'Ghidra frais', 'TU entières', 'COLLIDE_S.C', 'GETSTUFF.C',
            'ELF32', '-m32 -O0', 'deux méthodes unittest',
            '11 fichiers comportementaux', 'interpréteur reviewer indépendant',
            'sans import du producteur ni Unicorn', 'RAM/stack native complète non comparée',
            'pas de sanitizer', 'ItemNewRoom', 'appel intra-TU non intercepté',
            're769-proof/HANDOFF.md', 're769-review/rapport.md',
            're769-review/verdict.json', 're769-review/postreport-verification.json',
            'final-verification.json absent', 'lacune historique',
            'pas un échec de la caractérisation', 'clôture producteur non démontrée',
            'producteur non réparé', 'réserves non vides',
            'selon le contexte explicite de la délégation actuelle',
            '17:53:23+02', 'aucun replay privé ni audit buffers parent dans ce tick',
            'publisher', 'aucun rejeu privé',
            'source de production inchangée', 'code_change_readiness=blocked',
            'gardes historiques inchangées', '18:05', '18:12',
            'revue finale de publication PASS au 12 septembre 2026 à 18:06 Europe/Paris', 'distincte du PASS privé',
            'RED documentaire', 'red.log', 'green.log', 'suite.log',
            'overview actif', 'handoff actif', 'Après RE-768', 'Après RE-769',
            'Prochaine recherche proposée', 'non commencée',
        ):
            assert token in text, token
        assert not re.search(r'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}|\b[0-9a-f]{64}\b', text)
        assert not re.search(r'```(?:c|cpp|asm|mips)\b|<pre\b|word_le_hex|payload_offset|record offset|door\d|floor\d', text)
    assert '## Tracker' in STORY.read_text() and '## Handoff' in STORY.read_text()
    assert '- [x]' in STORY.read_text() and '- [ ]' in STORY.read_text()
    assert STORY.name in section


def test_re769_dashboard_exact_history():
    old = subprocess.check_output(['git', 'show', f'{BASE}:docs/reverse/reconstruction-progress.html'], cwd=ROOT)
    new = DASH.read_bytes()
    restored = re.sub(rb'<h2>RE-769 \xc2\xb7.*?(?=</body>)', b'', new, flags=re.S)
    assert restored == old, 'all predecessor bytes and closing tags must remain identical'
    sections = re.findall(rb'<h2>RE-\d+ \xc2\xb7.*?(?=<h2>|</body>)', old, re.S)
    assert sections
    for section in sections:
        assert section in new
    assert new.count(b'</body>') == old.count(b'</body>') == 1
    assert new.count(b'</html>') == old.count(b'</html>') == 1
