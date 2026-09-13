"""Documentary SOURCE contract only; never reads or executes private evidence."""
from pathlib import Path
import html
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
STORY = ROOT / 'docs/stories/RE-770-getheight-source-consumer.md'
DASH = ROOT / 'docs/reverse/reconstruction-progress.html'
BASE = '2a5e20aa498b6e85f7b51d4b659f9dd851cb94a9'


def test_re770_source_claims_and_attribution():
    assert STORY.exists(), 'RED documentaire : story RE770 absente'
    dashboard = DASH.read_text()
    assert dashboard.count('<h2>RE-770 ·') == 1
    section = html.unescape(dashboard.split('<h2>RE-770 ·', 1)[1].split('<h2>', 1)[0].split('</body>', 1)[0])
    for text in (STORY.read_text(), section):
        for token in (
            'SOURCE GetHeight → item.floor', '63 observations', '21 appels directs',
            '42 retours normaux complets UpdateLaraRoom', '21 alias', '21 non-alias',
            'sept géométries', 'trois points', '3072', '3515', '4364', '-32512',
            'cellule issue de item', 'coordonnées de pente issues de Lara',
            '288 octets', 'deux ITEM_INFO', 'autres zones : memcmp du harness seulement',
            'quatre méthodes', 'TU entières', 'GETSTUFF.C', 'COLLIDE_S.C',
            'sans wrapper', 'sans stub', 'pas de build du jeu entier',
            'GCC 13.3.0', 'C++17', '-m32 -O0', 'char signé',
            'shift gauche négatif', 'potentiellement indéfini', 'shift droit négatif',
            'pas de sanitizer', 'RED setup/contrat', 'FileNotFoundError',
            'zéro méthode exécutée', 'pas un RED comportemental', 'première exécution géométrique verte',
            'reviewer délégué distinct', 'reconstruction indépendante',
            'getheight-native/HANDOFF.md', 'getheight-review/RAPPORT.md',
            'getheight-review/verdict.json', 'getheight-review/delivery-verification.json',
            'parent-review-verification.json', '49 hashes', '09:56:19',
            'aucun replay privé ni audit buffers parent', 'publisher : aucun rejeu privé',
            'cible historique non exécutée', 'RE769 reste le stop à l’entrée GetHeight',
            'source de production inchangée', 'code_change_readiness=blocked',
            'gardes historiques inchangées', 'revue finale de publication PASS au 13 septembre 2026 à 10:09 Europe/Paris',
            'distincte du PASS privé', '13 septembre 2026', 'Europe/Paris',
            'overview actif', 'handoff actif', 'Après RE-769', 'Après RE-770',
            'collision amont/cible GetHeight', 'non commencée',
            'RED documentaire', 'red.log', 'green.log', 'suite.log',
            'salle inchangée', 'ItemNewRoom non exécuté', 'Y constant',
            'pas de gameplay', 'pas d’équivalence cible',
        ):
            assert token in text, token
        assert not re.search(r'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}|\b[0-9a-f]{64}\b', text)
        assert not re.search(r'```(?:c|cpp|asm|mips)\b|<pre\b|word_le_hex|payload_offset', text)
    assert '## Tracker' in STORY.read_text() and '## Handoff' in STORY.read_text()
    assert '- [x]' in STORY.read_text() and '- [ ]' in STORY.read_text()
    assert STORY.name in section


def test_re770_dashboard_exact_history():
    old = subprocess.check_output(['git', 'show', f'{BASE}:docs/reverse/reconstruction-progress.html'], cwd=ROOT)
    new = DASH.read_bytes()
    restored = re.sub(rb'<h2>RE-770 \xc2\xb7.*?(?=</body>)', b'', new, flags=re.S)
    assert restored == old, 'removing only RE770 must reproduce all HEAD bytes'
    for section in re.findall(rb'<h2>RE-\d+ \xc2\xb7.*?(?=<h2>|</body>)', old, re.S):
        assert section in new
    assert new.count(b'</body>') == old.count(b'</body>') == 1
    assert new.count(b'</html>') == old.count(b'</html>') == 1
