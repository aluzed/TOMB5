"""Documentation contract, not a replay of private binary evidence."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]


def test_re750_room_publication_scope():
    path = ROOT / 'docs/stories/RE-750-first-room-consumer-proof.md'
    assert path.exists(), 'RE750 publication missing'
    story = path.read_text(encoding='utf-8')
    dashboard = (ROOT / 'docs/reverse/reconstruction-progress.html').read_text(encoding='utf-8')
    assert path.name in dashboard
    for token in ('RE-749', 'S_LoadLevelFile', 'GAME/SETUP.C', '32 bits',
                  '5 allocations', '3 libérations', '7 buffers', '29 mots',
                  'data/door/floor/light/mesh', 'avant la deuxième salle',
                  '2 entrées actives', '22 mots', '4, 16 et 24',
                  'delay slot', 'troisième', 'CPU/RAM frais', 'GTE non exécuté',
                  '41 fichiers', '4 tests', 'Revue indépendante',
                  '--unresolved-symbols=ignore-all', 'pas de sanitizer',
                  'HEAD prépublication', 'gardes historiques',
                  'aucun correctif de production', '## Handoff',
                  '- [x]', '- [ ]', 'RED', 'GREEN'):
        assert token in story, token
    assert 'Après RE-750' in dashboard
    assert not re.search(r'0x[0-9a-fA-F]{6,}|FUN_[0-9a-fA-F]{8}', story)
