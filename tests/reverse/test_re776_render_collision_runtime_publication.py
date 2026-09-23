"""RE-776 documentary contract: rendering path and held-input collision gate."""
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.reverse.generate_tomb5_progress_dashboard import build, write
STORY = ROOT / 'docs/stories/RE-776-render-collision-runtime-gate.md'
DASH = ROOT / 'docs/reverse/reconstruction-progress.html'
INDEX = ROOT / 'docs/reverse/tomb5-progress-dashboard.html'
BASE = 'ff29db5acf5c9c897184107d171db9ee3f04b11f'


def section():
    text = DASH.read_text(encoding='utf-8')
    assert text.count('<h2>RE-776 ·') == 1
    return html.unescape(text.split('<h2>RE-776 ·', 1)[1].split('<h2>', 1)[0].split('</body>', 1)[0])


def test_re776_documents_separate_render_and_collision_observations():
    assert STORY.exists(), 'RED documentaire : story RE-776 absente'
    story = STORY.read_text(encoding='utf-8')
    for text in (story, section()):
        for token in (
            'Après RE-775', 'Après RE-776', '24 septembre 2026', 'ELF32',
            'sessions distinctes', 'DrawRooms', 'DrawLaraL1',
            'DrawRoomletListAsmRL1', 'GPU_EndScene', '960',
            'écart de pointeurs en octets', 'pas un compte de primitives',
            'capture non interprétable', 'LaraDeflectEdge', 'CT_FRONT',
            'IN_FORWARD', '38813', 'état d’arrêt', 'avant relâchement',
            'LaraCollideStop', 'première sonde', 'exit 124', 'wrapper GDB',
            'preuve cible manquante', 'GetHeight', 'gameplay complet non validé',
            'source de production inchangée', 'code_change_readiness=blocked',
            'aucun asset public', 'session.json', 'collision.jsonl',
            'held-at-limit.png',
        ):
            assert token in text, token
        assert not re.search(r'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}|\b[0-9a-f]{64}\b', text)
        assert not re.search(r'<img\b|data:image|```(?:c|cpp|asm|mips)\b|<pre\b', text)
    assert '## Tracker' in story and '## Handoff' in story
    assert '- [x]' in story and '- [ ]' in story
    assert STORY.name in section()


def test_re776_dashboard_appends_without_changing_historical_bytes():
    before = subprocess.check_output(['git', 'show', f'{BASE}:docs/reverse/reconstruction-progress.html'], cwd=ROOT)
    current = DASH.read_bytes()
    assert current.count(b'<h2>RE-776 \xc2\xb7') == 1
    restored = re.sub(rb'<h2>RE-776 \xc2\xb7.*?(?=</body>)', b'', current, flags=re.S)
    assert restored == before
    assert current.count(b'</body>') == before.count(b'</body>') == 1
    assert current.count(b'</html>') == before.count(b'</html>') == 1


def test_re776_active_index_preserves_re775_and_terminal_scope(tmp_path):
    index = INDEX.read_text(encoding='utf-8')
    assert 'RE-776 — rendu et borne de collision observés' in index
    assert 'RE-775 — contrôle avant/arrière en session continue' in index
    assert 'Historique clôturé — aucun backlog actif' in index
    assert write(build(ROOT), tmp_path).read_bytes() == INDEX.read_bytes()
