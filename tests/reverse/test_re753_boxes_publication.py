"""Contrat documentaire RE753 ; aucun accès aux artefacts/probes privés."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
STORY = ROOT / 'docs/stories/RE-753-box-overlap-divergence-proof.md'


def test_re753_boxes_publication_scope():
    assert STORY.exists(), 'RE753 publication missing'
    story = STORY.read_text(encoding='utf-8')
    dashboard = (ROOT / 'docs/reverse/reconstruction-progress.html').read_text(encoding='utf-8')
    assert dashboard.count('<h2>RE-753 ·') == 1
    current = dashboard.split('<h2>RE-753 ·', 1)[1].split('<h2>', 1)[0].split('</body>', 1)[0]
    assert STORY.name in current
    for text in (story, current):
        for token in (
            'PASS de caractérisation bornée', 'NON-ÉQUIVALENCE', 'un octet',
            'boxes[0..628]', 'boxes[629..1]', 'overlap[3]',
            'hors du bloc logique boxes', 'à l’intérieur de l’allocation',
            'boxes[0]', 'sans effet sur ce corpus', 'pas une trace',
            '524 000 octets', '329 832 octets', '4 774 mots', '116 salles',
            '23 champs pointeurs', '9 scalaires', '15 événements',
            '7 lectures', '5 allocations', '3 libérations',
            'pas aux retours de lecture hôtes',
            'SETUP.C:1274', 'SETUP.C:1429', 'CFG', 'avant de continuer',
            '282 instructions statiques', '10 branches', 'ELF',
            'delay slot', 'number_cameras', 'avant son corps', 'huitième lecture',
            '--unresolved-symbols=ignore-all', 'ne jamais exécuter ce binaire autonome',
            'pas tous les nuls calculés', 'aucun retour LoadLevel',
            '1 608 071 visites', '52 246 visites', '5 147 visites',
            '64 interceptions', 'pas des instructions retirées',
            '5 tests', '1 test', '18,637 s', '0,116 s', '11 sous-processus',
            'après les producteurs', 'review_check.py', 'parent',
            '11:25:56', '11:26:16', 'exit 0', 'recompilation',
            '341 dépendances', '11 fichiers de code', '53 setup', '27 harness',
            'en-têtes système', 'non hermétique', 'Python optimisé', 'exit 1',
            '1676c4d7', '23:25 Paris', 'gardes historiques',
            'nouvelle unité explicitement autorisée', 'Name=0',
            'doubles allocation/CD/SDK', 'ROOMLOAD.C', 'pas de sanitizer',
            'pas de sûreté mémoire générale', 'objets complets', '1 155',
            'aucun impact gameplay démontré', 'aucun correctif de production',
        ):
            assert token in text, token
        safe = re.sub(r'\b[0-9a-f]{64}\b', '<fingerprint>', text)
        assert not re.search(r'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}', safe)
        assert not re.search(r'(?:\\x[0-9a-fA-F]{2}){2,}|(?:\b[0-9A-Fa-f]{2} ){12,}', safe)
        assert not re.search(r'```(?:c|cpp|asm|mips)\b|<pre\b', safe)
    for token in ('## Tracker', '- [x]', '- [ ]', '## Handoff', 'RED', 'GREEN',
                  'metadata-only', 'publication-red.log', 'publication-green.log',
                  'publication-suite.log', 'publication-commands.json',
                  'parent-replay.log', 'parent-check.log', 'review.md',
                  'execution-commands.json', 'host-command.json',
                  'ne relance aucun probe privé', '0, 1 et plusieurs',
                  'premier et dernier', 'sentinelle overlap', 'état vivant'):
        assert token in story, token
    handoff = dashboard.split('<h2>Suite de la recherche</h2>', 1)[1].split('<h2>', 1)[0]
    for token in ('Après RE-750', 'Après RE-752', 'Après RE-753',
                  'test différentiel RED', 'vraie TU', 'correction', 'avant tout patch suivi'):
        assert token in handoff, token
