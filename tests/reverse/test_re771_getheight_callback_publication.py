"""RE771 documentary checks only: no private proof access or execution."""
from pathlib import Path
import html
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
STORY = ROOT / 'docs/stories/RE-771-getheight-callback-source.md'
DASH = ROOT / 'docs/reverse/reconstruction-progress.html'
BASE = 'df9e796fb70a344a00acc7eaa7ac0dd5a6be30fe'


def test_re771_source_limits_and_attributions():
    assert STORY.exists(), 'RED documentaire : story RE771 absente'
    dashboard = DASH.read_text()
    assert dashboard.count('<h2>RE-771 ·') == 1
    section = html.unescape(dashboard.split('<h2>RE-771 ·', 1)[1].split('<h2>', 1)[0].split('</body>', 1)[0])
    for text in (STORY.read_text(), section):
        for token in (
            'SOURCE GetHeight TRIGGER/callback → item.floor',
            '24 cas', '12 directs', '12 UpdateLaraRoom alias',
            '12 appels callback', '24 événements ordonnés',
            '432 octets', 'trois ITEM_INFO', '144 octets', 'quatre méthodes',
            'void(ITEM_INFO*,int,int,int,int*)', 'sans cast',
            'écrit sans lire', 'local non initialisé', '3072',
            '777/-2222/70000', '878/-2121/70101', '628/1701/4096',
            'ne sont pas des retours rétrécis', 'globaux persistent',
            'inhibition homogène', 'pas d’inhibition mixte',
            'pas de callback jeu', 'pas de non-alias', 'pas de triangles',
            'TU entières non modifiées', 'GETSTUFF.C', 'COLLIDE_S.C',
            'g++', 'C++17', '-m32 -O0', '--gc-sections',
            'sans wrapper', 'sans symboles non résolus tolérés',
            'pas de build du jeu entier', 'conversion du masque vers short',
            'compilateur retenu', 'pas de sanitizer', 'pas de preuve générale d’absence d’UB',
            'autres zones : memcmp du harness', 'pas de reconstruction indépendante de ces autres buffers',
            'pas de surveillance mémoire générale',
            'RED setup/contrat', 'zéro test exécuté', 'pas un RED comportemental',
            'neuf corruptions de copies', 'pas des contre-exemples source',
            'reviewer délégué distinct', 'reconstruction indépendante',
            'getheight-callback/HANDOFF.md', 'getheight-callback-review/REVIEW.md',
            'getheight-callback-review/verdict.json', 'getheight-callback-review/post-report.json',
            'verdict/erreurs/remarques', 'pas un booléen passed=true',
            'callback-parent-verification.json', '10:28:51', 'trois hashes',
            'selon le contexte explicite de cette délégation',
            'aucun replay privé ni audit buffers parent', 'publisher : aucun rejeu privé',
            'SOURCE uniquement', 'cible historique non exécutée',
            'source de production inchangée', 'code_change_readiness=blocked',
            'gardes historiques inchangées', 'revue finale de publication PASS au 13 septembre 2026 à 10:40 Europe/Paris',
            'distincte du PASS privé', 'snapshot avant revue',
            '13 septembre 2026', 'Europe/Paris', 'overview actif', 'handoff actif',
            'Après RE-770', 'Après RE-771', 'collision amont/cible GetHeight',
            'preuve authentique reste manquante', 'aucun nouveau topic ouvert',
            'RE769 reste le stop à l’entrée GetHeight', 'pas d’équivalence cible',
            'RED documentaire', 'red.log', 'green.log', 'suite.log',
        ):
            assert token in text, token
        assert not re.search(r'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}|\b[0-9a-f]{64}\b', text)
        assert not re.search(r'```(?:c|cpp|asm|mips)\b|<pre\b|word_le_hex|payload_offset', text)
    assert '## Tracker' in STORY.read_text() and '## Handoff' in STORY.read_text()
    assert '- [x]' in STORY.read_text() and '- [ ]' in STORY.read_text()
    assert STORY.name in section


def test_re771_dashboard_exact_history():
    old = subprocess.check_output(['git', 'show', f'{BASE}:docs/reverse/reconstruction-progress.html'], cwd=ROOT)
    new = DASH.read_bytes()
    assert new.count('<h2>RE-771 ·'.encode()) == 1, 'RED documentaire : section RE771 absente'
    restored = re.sub(rb'<h2>RE-771 \xc2\xb7.*?(?=</body>)', b'', new, flags=re.S)
    assert restored == old, 'remove only RE771: every HEAD byte must survive'
    for section in re.findall(rb'<h2>RE-\d+ \xc2\xb7.*?(?=<h2>|</body>)', old, re.S):
        assert section in new
    assert new.count(b'</body>') == old.count(b'</body>') == 1
    assert new.count(b'</html>') == old.count(b'</html>') == 1
