"""RE-774 documentary contract: real source level-loop and input observation."""
from pathlib import Path
import html
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.reverse.generate_tomb5_progress_dashboard import build, write

STORY = ROOT / 'docs/stories/RE-774-level-loop-keyboard-runtime.md'
DASH = ROOT / 'docs/reverse/reconstruction-progress.html'
INDEX = ROOT / 'docs/reverse/tomb5-progress-dashboard.html'
BASE = '2ccef8b843d90077a4f5955220d244c8694807ad'


def section():
    dashboard = DASH.read_text(encoding='utf-8')
    assert dashboard.count('<h2>RE-774 ·') == 1
    return html.unescape(dashboard.split('<h2>RE-774 ·', 1)[1].split('<h2>', 1)[0].split('</body>', 1)[0])


def test_re774_publication_records_level_loop_and_movement_limits():
    assert STORY.exists(), 'RED documentaire : story RE-774 absente'
    for text in (STORY.read_text(encoding='utf-8'), section()):
        for token in (
            'Après RE-773', 'Après RE-774', '23 septembre 2026',
            'ELF32', '105 secondes', 'exit 124', 'DoLevel', 'ControlPhase',
            'gfCurrentLevel=1', 'GAME_LOOP_ENTRY', 'LaraControl',
            'GLOBAL_playing_cutseq=0', 'IN_FORWARD', 'watchpoint',
            '31232', '31255', 'niveau chargé', 'contrôle observé',
            'gameplay complet non validé', 'GetHeight',
            'code_change_readiness=blocked', 'source de production inchangée',
            'aucun asset public', 'run.json', 'level.json', 'control.json',
            'movement.json', 'after-50.png',
        ):
            assert token in text, token
        assert not re.search(r'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}|\b[0-9a-f]{64}\b', text)
        assert not re.search(r'<img\b|data:image|```(?:c|cpp|asm|mips)\b|<pre\b', text)
    assert '## Tracker' in STORY.read_text() and '## Handoff' in STORY.read_text()
    assert '- [x]' in STORY.read_text() and '- [ ]' in STORY.read_text()
    assert STORY.name in section()


def test_re774_append_only_preserves_re773_dashboard_bytes():
    before = subprocess.check_output(['git', 'show', f'{BASE}:docs/reverse/reconstruction-progress.html'], cwd=ROOT)
    current = DASH.read_bytes()
    assert current.count(b'<h2>RE-774 \xc2\xb7') == 1
    restored = re.sub(rb'<h2>RE-774 \xc2\xb7.*?(?=</body>)', b'', current, flags=re.S)
    assert restored == before
    assert current.count(b'</body>') == before.count(b'</body>') == 1
    assert current.count(b'</html>') == before.count(b'</html>') == 1


def test_re774_index_keeps_historical_terminal_scope_and_re773_link(tmp_path):
    text = INDEX.read_text(encoding='utf-8')
    assert 'RE-774 — boucle du niveau et entrée contrôlée' in text
    assert 'RE-773 — menu visible, gameplay non validé' in text
    assert 'Historique clôturé — aucun backlog actif' in text
    assert write(build(ROOT), tmp_path).read_bytes() == text.encode('utf-8')
