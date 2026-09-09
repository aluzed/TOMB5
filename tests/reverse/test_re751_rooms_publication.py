"""Contrat documentaire public : aucun accès ni rejeu des preuves privées."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]


def test_re751_rooms_publication_scope():
    path = ROOT / 'docs/stories/RE-751-complete-room-loop-proof.md'
    assert path.exists(), 'RE751 publication missing'
    story = path.read_text(encoding='utf-8')
    dashboard = (ROOT / 'docs/reverse/reconstruction-progress.html').read_text(encoding='utf-8')
    assert path.name in dashboard
    section = dashboard.split('<h2>RE-751 ·', 1)
    assert len(section) == 2, 'RE751 active section missing'
    current = section[1].split('</body>', 1)[0]
    for text in (story, current):
        for token in (
            '116 salles', '3 364 mots', '3 335 mots', '524 000 octets',
            '161 entrées actives', '1 155 valeurs', 'valeur de départ',
            '580', '461', '119', '205 856', '318 144', '[0,24]',
            '7 buffers', '680 secteurs', '329 832', '5 allocations', '3 libérations',
            'pas aux retours de lecture host', 'allocateur double',
            'delay slot', 'avant la remise à zéro', 'SETUP.C:1274', 'i=116', 'j=24',
            '32 bits', '--unresolved-symbols=ignore-all', 'écriture absolue nulle',
            '6 tests', '17,011 s', 'deux exécutions', 'recompilation', '44 fichiers',
            'audit parent', '09:43', 'pas de rejeu cible ni de compilation par le parent',
            '1 584 596 visites', '64 interceptions', 'une visite d’arrêt',
            'pas un compte d’instructions retirées', '182 dépendances',
            'HEAD prépublication', '8265c8c0', '23:25 Paris', 'non continus',
            'code RE751 non auto-épinglé', 'en-têtes système', 'gardes historiques',
            'nouvelle unité explicitement autorisée', 'aucun correctif de production',
            'consommateur roomlet non exécuté', 'GTE non exécuté',
            'pas de sanitizer', 'pas de sûreté mémoire générale',
            'résoudre les dépendances',
        ):
            assert token in text, token
        assert not re.search(r'0x[0-9a-fA-F]{6,}|FUN_[0-9a-fA-F]{8}', text)
    for token in ('## Tracker', '- [x]', '- [ ]', '## Handoff', 'RED', 'GREEN',
                  'S_LoadLevelFile', 'Name=0', '2 784 additions',
                  'DISC_VERSION=1', 'DEBUG_VERSION=0', 'PSX_VERSION=1', 'PSXPC_TEST=1',
                  'Level 228', 'room_info 80', 'Python optimisé',
                  '67 fichiers', 'host-output.log', 'metadata-only'):
        assert token in story, token
    assert 'Après RE-751' in dashboard
