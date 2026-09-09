"""Public integration record; no private proof execution or imports."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
STORY = ROOT / 'docs/stories/RE-755-boxes-production-integration.md'


def test_re755_integration_scope_and_handoff():
    assert STORY.exists(), 'RE755 integration story missing'
    story = STORY.read_text()
    dashboard = (ROOT / 'docs/reverse/reconstruction-progress.html').read_text()
    assert dashboard.count('<h2>RE-755 ·') == 1
    section = dashboard.split('<h2>RE-755 ·', 1)[1].split('<h2>', 1)[0].split('</body>', 1)[0]
    assert STORY.name in section
    for text in (story, section):
        for token in ('deux références', 'i - 1', 'GAME/SETUP.C', 'RE-754',
                      'vraie TU', 'synthétiques', '6 échecs', '7 tests',
                      'premier', 'dernier', 'sentinelle', 'compteur', '37',
                      'PSX_VERSION=1', 'PSXPC_TEST=1', 'i386', '-O0',
                      'source partagée', 'autres backends non validés',
                      '48 octets', 'GDB', 'CFG', 'avant exécution',
                      'avant camera.fixed', '--unresolved-symbols=ignore-all',
                      'ne jamais exécuter ce binaire autonome',
                      'pas de retour LoadLevel', 'pas de sûreté mémoire générale',
                      'pas de sanitizer', 'pas de preuve gameplay',
                      'aucun rejeu cible', 'gardes historiques inchangées',
                      'revue indépendante', 'parent', 'revue PASS', '1 216 tests',
                      '51,07 s', 'parent-audit.json',
                      'ne pas étendre objets'):
            assert token.casefold() in text.casefold(), token
        assert not re.search(r'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}', text)
        assert not re.search(r'```(?:c|cpp|asm|mips)\b|<pre\b', text)
    for token in ('## Tracker', '## Handoff', '- [x]', '- [ ]', 'red.log',
                  'green.log', 'suite.log', 'commands.json', 'test_setup_boxes.py'):
        assert token in story
    handoff = dashboard.split('<h2>Suite de la recherche</h2>', 1)[1].split('<h2>', 1)[0]
    assert 'Après RE-755' in handoff
    assert 'revue indépendante' in handoff
