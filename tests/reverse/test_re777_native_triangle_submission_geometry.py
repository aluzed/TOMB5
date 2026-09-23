"""RE-777 documentary contract: submitted triangle path and projected geometry."""
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.reverse.generate_tomb5_progress_dashboard import build, write
STORY = ROOT / 'docs/stories/RE-777-native-triangle-submission-geometry.md'
DASH = ROOT / 'docs/reverse/reconstruction-progress.html'
INDEX = ROOT / 'docs/reverse/tomb5-progress-dashboard.html'
BASE = '37e008e62e0c41346c5edc941909b3f813440b74'


def section():
    text = DASH.read_text(encoding='utf-8')
    assert text.count('<h2>RE-777 ·') == 1
    return html.unescape(text.split('<h2>RE-777 ·', 1)[1].split('<h2>', 1)[0].split('</body>', 1)[0])


def test_re777_qualifies_submitted_triangles_and_screenshot_visibility():
    assert STORY.exists(), 'RED documentaire : story RE-777 absente'
    story = STORY.read_text(encoding='utf-8')
    for text in (story, section()):
        for token in (
            'Après RE-776', 'Après RE-777', '24 septembre 2026', 'ELF32',
            'sessions distinctes', 'DrawAggregatedSplits', 'Emulator_DrawTriangles',
            'Emulator_EndScene', 'non nulles', 'sommets projetés',
            'triangles non dégénérés', 'rectangle de rendu', '512', '240',
            'pas une preuve de rasterisation', 'capture non interprétable',
            'source de production inchangée', 'code_change_readiness=blocked',
            'GetHeight', 'gameplay complet non validé', 'exit 124',
            'wrapper GDB', 'aucun asset public', 'session.json',
            'submit.jsonl', 'vertex-metadata.jsonl', 'forward-vertices.png',
        ):
            assert token in text, token
        assert not re.search(r'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}|\b[0-9a-f]{64}\b', text)
        assert not re.search(r'<img\b|data:image|```(?:c|cpp|asm|mips)\b|<pre\b', text)
    assert '## Tracker' in story and '## Handoff' in story
    assert '- [x]' in story and '- [ ]' in story
    assert STORY.name in section()


def test_re777_dashboard_append_only_preserves_re776_bytes():
    before = subprocess.check_output(['git', 'show', f'{BASE}:docs/reverse/reconstruction-progress.html'], cwd=ROOT)
    current = DASH.read_bytes()
    assert current.count(b'<h2>RE-777 \xc2\xb7') == 1
    restored = re.sub(rb'<h2>RE-777 \xc2\xb7.*?(?=</body>)', b'', current, flags=re.S)
    assert restored == before
    assert current.count(b'</body>') == before.count(b'</body>') == 1
    assert current.count(b'</html>') == before.count(b'</html>') == 1


def test_re777_active_index_preserves_re776_and_terminal_scope(tmp_path):
    index = INDEX.read_text(encoding='utf-8')
    assert 'RE-777 — soumission et géométrie projetée du niveau' in index
    assert 'RE-776 — rendu et borne de collision observés' in index
    assert 'Historique clôturé — aucun backlog actif' in index
    assert write(build(ROOT), tmp_path).read_bytes() == INDEX.read_bytes()
