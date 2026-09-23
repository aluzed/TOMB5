"""Public RE-773 runtime milestone: documentary checks; no private probe execution."""
from pathlib import Path
import html
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.reverse.generate_tomb5_progress_dashboard import build, write

STORY = ROOT / 'docs/stories/RE-773-interactive-title-runtime.md'
DASH = ROOT / 'docs/reverse/reconstruction-progress.html'
INDEX = ROOT / 'docs/reverse/tomb5-progress-dashboard.html'
BASE = '315216e2f2c40d072dbf93b0a2da3a3e89896806'


def test_re773_integrated_runtime_evidence_and_limits():
    assert STORY.exists(), 'RED documentaire : RE-773 absente'
    dashboard = DASH.read_text(encoding='utf-8')
    assert dashboard.count('<h2>RE-773 ·') == 1
    section = html.unescape(dashboard.split('<h2>RE-773 ·', 1)[1].split('<h2>', 1)[0].split('</body>', 1)[0])
    for text in (STORY.read_text(encoding='utf-8'), section):
        for token in (
            '23 septembre 2026', 'Europe/Paris', 'Après RE-772', 'Après RE-773',
            'ELF32', 'build exit 0', 'DISC_VERSION=ON', 'GLEW',
            '45 secondes', '80 secondes', 'exit 124', 'limite temporelle',
            'New Game', 'Special Features', 'XTest', 'flèche bas', 'flèche haut',
            'touche C', 'menu visible', 'gameplay non validé',
            'runtime.json', 'interactive.json', 'interactive.log',
            'select-gdb.log', 'ret=3', 'gfLevelComplete=1',
            'source de production inchangée', 'code_change_readiness=blocked',
            'aucun asset public', 'GetHeight',
        ):
            assert token in text, token
        assert not re.search(r'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}|\b[0-9a-f]{64}\b', text)
        assert not re.search(r'<img\b|data:image|```(?:c|cpp|asm|mips)\b|<pre\b', text)
    assert '## Tracker' in STORY.read_text() and '## Handoff' in STORY.read_text()
    assert '- [x]' in STORY.read_text() and '- [ ]' in STORY.read_text()
    assert STORY.name in section


def test_re773_preserves_prior_reconstruction_dashboard_bytes():
    before = subprocess.check_output(['git', 'show', f'{BASE}:docs/reverse/reconstruction-progress.html'], cwd=ROOT)
    current = DASH.read_bytes()
    assert current.count('<h2>RE-773 ·'.encode()) == 1
    restored = re.sub(rb'<h2>RE-773 \xc2\xb7.*?(?=</body>)', b'', current, flags=re.S)
    assert restored == before
    assert current.count(b'</body>') == before.count(b'</body>') == 1
    assert current.count(b'</html>') == before.count(b'</html>') == 1


def test_re773_historical_inventory_links_current_runtime_without_reopening_queue(tmp_path):
    index = INDEX.read_text(encoding='utf-8')
    assert 'RE-773 — menu visible, gameplay non validé' in index
    assert 'reconstruction-progress.html' in index
    assert 'Historique clôturé — aucun backlog actif' in index
    assert write(build(ROOT), tmp_path).read_bytes() == index.encode('utf-8')
