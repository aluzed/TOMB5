"""Contrat documentaire RE763 : aucun asset, import ou rejeu privé."""
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
STORY = ROOT / 'docs/stories/RE-763-getdoor-authentic-corpus-proof.md'
DASHBOARD = ROOT / 'docs/reverse/reconstruction-progress.html'
BASE = '1f4f49d4e2c006283713d8afd62e734e2a3309a8'
OVERVIEW = 'Suivi au 9 septembre 2026, publication RE-763 ; caractérisation sur corpus authentique, sans patch. Repère historique : '
HANDOFF = 'Après RE-763 : preuve bornée du corpus GetDoor publiée, revue indépendante PASS et audit reviewer exécuté par le parent. Prochaine preuve proposée : traversées verticales GetFloor et helpers triangles sur corpus chargé, portée à conserver avant tout patch. L’absence de destination supérieure à 255 ne rouvre pas une correction de largeur. Transition historique conservée : '


def test_re763_claims_and_limits_in_both_publications():
    assert STORY.exists(), 'RE763 story absente : RED documentaire attendu'
    story = STORY.read_text()
    dashboard = DASHBOARD.read_text()
    assert dashboard.count('<h2>RE-763 ·') == 1
    section = dashboard.split('<h2>RE-763 ·', 1)[1].split('<h2>', 1)[0].split('</body>', 1)[0]
    for text in (story, section):
        for token in (
            'PASS de caractérisation bornée', '15 niveaux', '2704 rooms',
            '91444 cellules', '34882 appels distincts', '8232344 octets',
            '16791 cellules', '4992 cellules', '0 à 253',
            'zéro destination explicite supérieure à 255',
            '254 et 255 explicites non exercés', 'sentinelle 255',
            '79645 différences', 'zéro différence après unsigned char',
            'pas une équivalence ABI', '2 méthodes unittest',
            'deux imports Ghidra neufs', 'suffixe loader isolé',
            'GetFloor inspecté statiquement, non exécuté',
            '128 fichiers comportementaux', 'ISO locale',
            'review/report.md', 'review/verdict.json', 'parent/run.json',
            'parent-audit/invocation.json', 'parent-audit/independent-result.json',
            '19:59:04.071333–20:00:21.608102', 'moteur enfant',
            '20:00:21.642147–20:00:24.017787',
            'main du reviewer', 'pas un nouvel auteur indépendant',
            'pas de preuve matérielle', 'pas de preuve gameplay',
            'pas de domaine universel', 'pas de sanitizers',
            'images RAM complètes non archivées', 'visites de hooks',
            'source de production inchangée', 'gardes historiques inchangées',
            'aucun rejeu privé pendant cette publication',
            'traversées verticales GetFloor', 'helpers triangles',
            'red.log', 'green.log', 'suite.log',
        ):
            assert token.casefold() in text.casefold(), token
        assert not re.search(r'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}', text)
        assert not re.search(r'```(?:c|cpp|asm|mips)\b|<pre\b', text)
        assert not re.search(r'(?:\\x[0-9a-fA-F]{2}){2,}|(?:\b[0-9A-Fa-f]{2} ){12,}', text)
    for token in ('## Tracker', '## Handoff', '- [x]', '- [ ]'):
        assert token in story
    assert STORY.name in section
    assert OVERVIEW in dashboard
    assert HANDOFF in dashboard


def test_re763_preserves_all_historical_bytes():
    old = subprocess.check_output(['git', 'show', f'{BASE}:docs/reverse/reconstruction-progress.html'], cwd=ROOT)
    new = DASHBOARD.read_bytes()
    # Exact inverse of the only authorized prefixes and the appended section.
    restored = new.replace(OVERVIEW.encode(), b'', 1).replace(HANDOFF.encode(), b'', 1)
    restored = re.sub(rb'<h2>RE-763 \xc2\xb7.*?(?=</body>)', b'', restored, flags=re.S)
    assert restored == old, 'historique ou régions non autorisées modifiés'
    for section in re.findall(rb'<h2>RE-\d+ \xc2\xb7.*?(?=<h2>|</body>)', old, re.S):
        assert section in new, 'section historique modifiée'
