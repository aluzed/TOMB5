"""Publication RE752 uniquement : aucune lecture ou exécution de preuves privées."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
STORY = ROOT / 'docs/stories/RE-752-post-room-mesh-animation-proof.md'


def test_re752_postroom_publication_scope():
    assert STORY.exists(), 'RE752 publication missing'
    story = STORY.read_text(encoding='utf-8')
    dashboard = (ROOT / 'docs/reverse/reconstruction-progress.html').read_text(encoding='utf-8')
    assert dashboard.count('<h2>RE-752 ·') == 1
    current = dashboard.split('<h2>RE-752 ·', 1)[1].split('</body>', 1)[0]
    assert STORY.name in current
    for text in (story, current):
        for token in (
            'PASS borné', '11 globales', '834', '576', '1 410 mots', '4 774 mots',
            '524 000 octets', '329 832 octets', '4 230 octets', '116 salles',
            '7 lectures', '5 allocations', '3 libérations', '15 événements',
            'SETUP.C:1274', 'SETUP.C:1332', 'AnimTextureRanges', 'CFG',
            'avant de continuer', '111 instructions statiques', 'delay slot',
            '--unresolved-symbols=ignore-all', 'ne jamais exécuter ce binaire autonome',
            'OLD_CODE=1', 'addition directe', 'arrondi signé vers zéro',
            'pairs et non négatifs', 'modèle', 'pas l’équivalence de la vraie TU',
            'objets complets', '1 155', 'inactifs', 'pas de sûreté mémoire générale',
            'pas aux retours de lecture hôtes', 'pas de sanitizer', 'Name=0',
            'ROOMLOAD.C', '9 tests', '17,392 s', 'recompilation', 'parent',
            '10:29:45', '10:30:03', '198 dépendances', '53', '19',
            'en-têtes système', 'non hermétique', 'Python optimisé', 'exit 1',
            '7900232d', '23:25 Paris', 'gardes historiques',
            '1 602 924 visites', '47 100 visites', '64 interceptions',
            'pas des instructions retirées', 'aucun correctif de production',
            'nouvelle unité explicitement autorisée',
        ):
            assert token in text, token
        # Allow SHA-256 fingerprints, never addresses, listings or payload literals.
        safe = re.sub(r'\b[0-9a-f]{64}\b', '<fingerprint>', text)
        assert not re.search(r'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}', safe)
        assert not re.search(r'(?:\\x[0-9a-fA-F]{2}){2,}|(?:\b[0-9A-Fa-f]{2} ){12,}', safe)
        assert not re.search(r'```(?:c|cpp|asm|mips)\b|<pre\b', safe)
    for token in ('## Tracker', '- [x]', '- [ ]', '## Handoff', 'RED', 'GREEN',
                  'metadata-only', 'publication-red.log', 'publication-green.log',
                  'publication-suite.log', 'parent-replay.log', 'parent-check.log',
                  'execution-commands.json', 'host-command.json',
                  '90/93', 'PID', 'horodatages', 'durée', 'après la suite',
                  'ne relance aucun probe privé'):
        assert token in story, token
    assert 'Après RE-752' in dashboard
