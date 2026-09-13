"""Public documentary contract only; never run or read private runtime probes."""
from pathlib import Path
import html
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
STORY = ROOT / 'docs/stories/RE-772-build-runtime-observable.md'
DASH = ROOT / 'docs/reverse/reconstruction-progress.html'
BASE = 'd63b1440f3f591e422aab05a61874e96f87dd942'


def test_re772_runtime_milestone_and_limits():
    assert STORY.exists(), 'RED setup documentaire : story RE772 absente'
    dashboard = DASH.read_text()
    assert dashboard.count('<h2>RE-772 ·') == 1
    section = html.unescape(dashboard.split('<h2>RE-772 ·', 1)[1].split('<h2>', 1)[0].split('</body>', 1)[0])
    for text in (STORY.read_text(), section):
        for token in (
            '13 septembre 2026', 'Europe/Paris', 'overview actif', 'handoff actif',
            'Après RE-771', 'Après RE-772', 'build/runtime observable',
            'build64', 'ELF64', 'LoadLevel', 'GAME/SETUP.C:1225', 'SIGSEGV',
            'exit 139', 'exit -11', 'wrapper exit 0', 'GDB exit 1', 'ROOM_INFO',
            'build32', 'ELF32', 'GLEW 2.2.0', 'compilation privée', '-m32',
            'GLEW_LIBRARY', 'build exit 0', '30 secondes', 'exit 124',
            'limite temporelle', 'pas une réussite fonctionnelle',
            'sans SIGSEGV observé', 'SIGINT volontaire', 'pas un deadlock démontré',
            'pthread_cond_wait', 'Emulator_SwapWindow', 'cause exacte non établie',
            'splash/logo', 'menu interactif et gameplay non validés',
            'runtime-1049/RAPPORT.md', 'runtime-1049/gdb64.log',
            'runtime-1049/build64.json', 'runtime-1049/launch64-xvfb.json',
            'runtime-1058/RAPPORT.md', 'runtime-1058/build32.json',
            'runtime-1058/capture32-app.json', 'runtime-1058/gdb32.json',
            'publisher : lecture des rapports, logs et ledgers',
            'aucun rejeu runtime', 'pas un audit des buffers',
            'captures restent privées', 'aucun asset public',
            'source de production inchangée', 'pas d’équivalence cible',
            'code_change_readiness=blocked', 'nouvelle preuve n’autorise pas de patch',
            'collision amont/cible GetHeight', 'preuve authentique reste manquante',
            'revue finale de publication PASS au snapshot du 13 septembre 2026 à 11:16 Europe/Paris',
            'RED setup documentaire', 'red.log', 'green.log', 'suite.log',
        ):
            assert token in text, token
        assert not re.search(r'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}|\b[0-9a-f]{64}\b', text)
        assert not re.search(r'<img\b|data:image|```(?:c|cpp|asm|mips)\b|<pre\b', text)
    assert '## Tracker' in STORY.read_text() and '## Handoff' in STORY.read_text()
    assert '- [x]' in STORY.read_text() and '- [ ]' in STORY.read_text()
    assert STORY.name in section


def test_re772_dashboard_exact_history():
    old = subprocess.check_output(['git', 'show', f'{BASE}:docs/reverse/reconstruction-progress.html'], cwd=ROOT)
    new = DASH.read_bytes()
    assert new.count('<h2>RE-772 ·'.encode()) == 1, 'RED setup documentaire : section RE772 absente'
    restored = re.sub(rb'<h2>RE-772 \xc2\xb7.*?(?=</body>)', b'', new, flags=re.S)
    assert restored == old, 'remove only RE772: restore every predecessor byte and closing tag'
    for section in re.findall(rb'<h2>RE-\d+ \xc2\xb7.*?(?=<h2>|</body>)', old, re.S):
        assert section in new
    assert new.count(b'</body>') == old.count(b'</body>') == 1
    assert new.count(b'</html>') == old.count(b'</html>') == 1
