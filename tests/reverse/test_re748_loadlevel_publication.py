from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]


def test_re748_loadlevel_publication_scope():
    path = ROOT / 'docs/stories/RE-748-loadlevel-prefix-proof.md'
    assert path.exists()
    story = path.read_text(encoding='utf-8')
    dashboard = (ROOT / 'docs/reverse/reconstruction-progress.html').read_text(encoding='utf-8')
    assert path.name in dashboard
    for token in ('S_LoadLevelFile', 'LoadLevel', 'LoadSoundEffects', 'GAME/SETUP.C',
                  '32 bits', '228 octets', '4 effets sonores', '7 616 octets',
                  '3 allocations', '3 libérations', '5 lectures', '262 secteurs',
                  'SpuMalloc', 'SpuIsTransferCompleted', 'SpuSetTransferStartAddr',
                  'SpuWrite', '--unresolved-symbols=ignore-all', 'exception',
                  'troisième free', 'immédiatement après',
                  'pas un descripteur host complet', 'compteur d’octets utilisés',
                  'visites du hook', 'pas des instructions exécutées',
                  'Pas de preuve matérielle', '07:51', '3 tests cible', '1 test host',
                  'HEAD prépublication', 'nouvelle unité explicitement autorisée',
                  'sans désactiver les anciennes gardes', 'frames', 'roomInfo',
                  '## Handoff', '- [x]', '- [ ]', 'RED', 'GREEN'):
        assert token in story, token
    assert 'aucun correctif de production justifié' in story
    assert 'Revue indépendante' in story
    assert '262 secteurs' in dashboard
    assert 'frames' in dashboard and 'roomInfo' in dashboard
    assert not re.search(r'0x[0-9a-fA-F]{6,}|FUN_[0-9a-fA-F]{8}', story)
