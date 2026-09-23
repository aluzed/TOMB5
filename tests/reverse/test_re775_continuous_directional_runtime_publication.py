"""RE-775: bounded continuous native input observation, not gameplay equivalence."""
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.reverse.generate_tomb5_progress_dashboard import build, write
STORY = ROOT / 'docs/stories/RE-775-continuous-directional-runtime.md'
DASH = ROOT / 'docs/reverse/reconstruction-progress.html'
INDEX = ROOT / 'docs/reverse/tomb5-progress-dashboard.html'
BASE = '5399f2904fce05cea5964927c85cac8cbf01f153'


def section():
    text = DASH.read_text(encoding='utf-8')
    assert text.count('<h2>RE-775 ·') == 1
    return html.unescape(text.split('<h2>RE-775 ·', 1)[1].split('<h2>', 1)[0].split('</body>', 1)[0])


def test_re775_records_continuous_control_without_claiming_collision_or_gameplay():
    assert STORY.exists(), 'RED documentaire : story RE-775 absente'
    story = STORY.read_text(encoding='utf-8')
    for text in (story, section()):
        for token in (
            'Après RE-774', 'Après RE-775', '24 septembre 2026', 'ELF32',
            'même session', 'sans entrée', 'IN_FORWARD', 'IN_BACK', 'LaraControl',
            'chambre 0', 'chambre 2', '31232', '38818', '29797',
            'caméra', 'collision non prouvée', 'progression non validée',
            'gameplay complet non validé', 'exit 124', 'wrapper GDB',
            'source de production inchangée', 'code_change_readiness=blocked',
            'session.json', 'samples.jsonl', 'forward-held.png', 'back-held.png',
            'aucun asset public', 'GetHeight',
        ):
            assert token in text, token
        assert not re.search(r'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}|\b[0-9a-f]{64}\b', text)
        assert not re.search(r'<img\b|data:image|```(?:c|cpp|asm|mips)\b|<pre\b', text)
    assert '## Tracker' in story and '## Handoff' in story
    assert '- [x]' in story and '- [ ]' in story
    assert STORY.name in section()


def test_re775_dashboard_appends_without_changing_historical_bytes():
    before = subprocess.check_output(['git', 'show', f'{BASE}:docs/reverse/reconstruction-progress.html'], cwd=ROOT)
    current = DASH.read_bytes()
    assert current.count(b'<h2>RE-775 \xc2\xb7') == 1
    restored = re.sub(rb'<h2>RE-775 \xc2\xb7.*?(?=</body>)', b'', current, flags=re.S)
    assert restored == before
    assert current.count(b'</body>') == before.count(b'</body>') == 1
    assert current.count(b'</html>') == before.count(b'</html>') == 1


def test_re775_active_index_preserves_re774_and_historical_scope(tmp_path):
    index = INDEX.read_text(encoding='utf-8')
    assert 'RE-775 — contrôle avant/arrière en session continue' in index
    assert 'RE-774 — boucle du niveau et entrée contrôlée' in index
    assert 'Historique clôturé — aucun backlog actif' in index
    assert write(build(ROOT), tmp_path).read_bytes() == INDEX.read_bytes()
