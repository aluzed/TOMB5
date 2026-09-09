"""RE758 integration publication guards; never read private proof artifacts."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
STORY = ROOT / 'docs/stories/RE-758-smash-production-integration.md'


def test_re758_public_scope_limits_and_handoff():
    assert STORY.exists(), 'RE758 integration story missing'
    story = STORY.read_text()
    dashboard = (ROOT / 'docs/reverse/reconstruction-progress.html').read_text()
    assert dashboard.count('<h2>RE-758 ·') == 1
    section = dashboard.split('<h2>RE-758 ·', 1)[1].split('<h2>', 1)[0].split('</body>', 1)[0]
    assert STORY.name in section
    for text in (story, section):
        for token in ('RE-757', 'vraie TU GAME/OBJECTS.C', 'SmashObjectControl',
                      'SmashObject inchangé', 'item_number', 'PSX_VERSION && PSXPC_TEST',
                      'source partagée', 'autres backends non validés',
                      'garde de préprocesseur', 'i386', '-O0', '128 cas',
                      'dimensions indépendantes', '64 appels directs', '16 wrappers',
                      '48 échecs comportementaux', '1 échec de garde', '133 tests',
                      'I=576', 'B=32', 'F=64', 'room=80', 'événements ordonnés',
                      'SoundEffect', 'ExplodingDeath2', 'RemoveActiveItem',
                      'trois doubles ABI', 'sans effets mémoire',
                      'aucun rejeu cible', 'gardes historiques inchangées',
                      'indices négatifs/extrêmes', 'états hétérogènes',
                      'pas de build complet', 'pas de sanitizer',
                      'pas de sûreté mémoire générale', 'pas de preuve gameplay',
                      'revue indépendante', 'parent', 'non exécutés par ce worker',
                      'Vérification parent effectuée', 'Revue indépendante PASS',
                      'parent-suite.json', 'parent-audit-command.json',
                      '1 353 tests réussis en 51,66 s', '188 tests frais',
                      'aucun rejeu privé'):
            # HTML escapes are accepted; historical sections cannot satisfy this check.
            assert token.casefold() in text.replace('&amp;', '&').casefold(), token
        assert not re.search(r'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}', text)
        assert not re.search(r'```(?:c|cpp|asm|mips)\b|<pre\b', text)
        assert not re.search(r'(?:\\x[0-9a-fA-F]{2}){2,}|(?:\b[0-9A-Fa-f]{2} ){12,}', text)
        assert not re.search(r'(?i)\b(?:lui|addiu|sw|lw)\s+\$', text)
    for token in ('## Tracker', '## Handoff', '- [x]', '- [ ]', 'red.log', 'green.log',
                  'suite.log', 'commands.json', 'test_smash_object_control.py'):
        assert token in story
    handoff = dashboard.split('<h2>Suite de la recherche</h2>', 1)[1].split('<h2>', 1)[0]
    assert 'Après RE-758' in handoff
    assert 'revue indépendante' in handoff
    assert 'Suivi au 9 septembre 2026, intégration RE-758' in dashboard


def test_public_regression_has_no_private_dependency():
    source = (ROOT / 'tests/emulator/test_smash_object_control.py').read_text()
    assert 'build/reverse' not in source
    assert 'unresolved-symbols' not in source
    assert 'import engine' not in source
    assert 'GAME/OBJECTS.C' in source
