"""Publication RE754 seulement : aucun import ni rejeu des preuves privées."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
STORY = ROOT / 'docs/stories/RE-754-boxes-correction-proof.md'


def test_re754_boxes_correction_publication_scope():
    assert STORY.exists(), 'RE754 publication missing'
    story = STORY.read_text(encoding='utf-8')
    dashboard = (ROOT / 'docs/reverse/reconstruction-progress.html').read_text(encoding='utf-8')
    assert dashboard.count('<h2>RE-754 ·') == 1
    current = dashboard.split('<h2>RE-754 ·', 1)[1].split('<h2>', 1)[0].split('</body>', 1)[0]
    assert STORY.name in current
    for text in (story, current):
        for token in (
            'PASS de preuve corrective bornée privée', 'vraie TU',
            'deux références', 'i - 1', 'aucun patch de production',
            'RED archivé', 'pas réexécuté par le reviewer', '13 échecs',
            'un octet', 'overlap[3]', '247 fichiers',
            '116 salles', '524 000 octets', '4 774 mots', 'zéro différence',
            '329 832 octets', '629 boxes', 'trois écritures',
            'sept cas synthétiques', 'zero', 'one-clear', 'one-last',
            'four-0', 'four-1', 'four-8', 'four-9',
            'compteur', '37', 'réaffecté', 'ascendant', 'descendant',
            'watchpoint', 'champ sentinelle', 'pas tous les stores natifs',
            '15 événements', '7 lectures', '5 allocations', '3 libérations',
            'pas aux retours de lecture hôtes', '285 instructions statiques',
            '10 branches', 'ELF', 'avant exécution', 'delay slot',
            'SETUP.C:1429', 'huitième lecture objets', 'avant son corps',
            'aucun retour LoadLevel', '--unresolved-symbols=ignore-all',
            'ne jamais exécuter ce binaire autonome', 'ni dépasser la borne',
            '1 608 071 visites', '52 246', '5 147', '64 interceptions',
            'pas des instructions retirées', '6 tests', '1 test post-audit',
            '9 sous-processus', '8 inférieurs GDB', 'une compilation',
            '12:08:45', '12:08:57', '12:12:04', '12:14:58', '12:15:11',
            'parent', 'review_check.py', 'exit 0', '521/539', '18 logs',
            '47 fichiers historiques', '356 dépendances', 'setup 53', 'harness 27',
            'non hermétique', 'Python optimisé', 'exit 1 attendu',
            '6ced3343', '23:25 Paris', 'gardes historiques', 'Name=0',
            'doubles allocation/CD/SDK', 'pas oracle matériel',
            'pas de sanitizer', 'pas de sûreté mémoire générale',
            'comptes négatifs/extrêmes', '1 155 fixups',
            'patch minimal', 'backend prouvé', 'TDD', 'tests publics',
            'attribution', 'ne pas étendre objets',
        ):
            assert token in text, token
        safe = re.sub(r'\b[0-9a-f]{64}\b', '<fingerprint>', text)
        assert not re.search(r'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}', safe)
        assert not re.search(r'(?:\\x[0-9a-fA-F]{2}){2,}|(?:\b[0-9A-Fa-f]{2} ){12,}', safe)
        assert not re.search(r'```(?:c|cpp|asm|mips)\b|<pre\b', safe)
    for token in ('## Tracker', '- [x]', '- [ ]', '## Handoff', 'GREEN',
                  'metadata-only', 'publication-red.log', 'publication-green.log',
                  'publication-suite.log', 'publication-final.log',
                  'publication-commands.json', 'parent-replay.log', 'parent-check.log',
                  'review.md', 'handoff.md', 'ne relance aucun probe privé'):
        assert token in story, token
    handoff = dashboard.split('<h2>Suite de la recherche</h2>', 1)[1].split('<h2>', 1)[0]
    for token in ('Après RE-750', 'Après RE-752', 'Après RE-753', 'Après RE-754',
                  'test différentiel RED', 'vraie TU', 'avant tout patch suivi',
                  'patch minimal', 'backend prouvé', 'TDD', 'tests publics',
                  'attribution', 'ne pas étendre objets'):
        assert token in handoff, token
