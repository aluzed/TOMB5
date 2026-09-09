"""Publication contract only; private binary evidence is not a public fixture."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]


def test_re749_frames_publication_scope():
    path = ROOT / 'docs/stories/RE-749-frames-room-prefix-proof.md'
    assert path.exists()
    story = path.read_text(encoding='utf-8')
    dashboard = (ROOT / 'docs/reverse/reconstruction-progress.html').read_text(encoding='utf-8')
    assert path.name in dashboard
    for token in ('S_LoadLevelFile', 'GAME/SETUP.C', '32 bits',
                  '329 832', '524 000', '116 salles', '80 octets',
                  '5 allocations', '3 libérations', '7 buffers', '680 secteurs',
                  'descripteurs complets normalisés', '24 mots', '4, 16 et 24',
                  'pas une validité de pointeurs', 'avant door',
                  'breakpoint matériel', '--unresolved-symbols=ignore-all',
                  'Pas de preuve matérielle', 'pas de sanitizer',
                  'HEAD prépublication', 'sans désactiver les anciennes gardes',
                  'Revue indépendante', '08:15', '2 tests cible', '1 test host',
                  '## Handoff', '- [x]', '- [ ]', 'RED', 'GREEN'):
        assert token in story, token
    assert 'aucun correctif de production' in story
    assert '24 mots' in dashboard and 'hors allocation' in dashboard
    assert not re.search(r'0x[0-9a-fA-F]{6,}|FUN_[0-9a-fA-F]{8}', story)
