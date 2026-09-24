"""RE-778 documentary contract; no runtime or private evidence replay."""
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.reverse.generate_tomb5_progress_dashboard import build, write

STORY = ROOT / 'docs/stories/RE-778-native-fade-camera-control.md'
DASH = ROOT / 'docs/reverse/reconstruction-progress.html'
INDEX = ROOT / 'docs/reverse/tomb5-progress-dashboard.html'
BASE = '84d6548c921749ee63c2b74593d2e59019bae841'


def section():
    text = DASH.read_text(encoding='utf-8')
    assert text.count('<h2>RE-778 ·') == 1
    return html.unescape(text.split('<h2>RE-778 ·', 1)[1].split('</body>', 1)[0])


def test_re778_documents_native_fade_intro_and_bounded_movement():
    assert STORY.exists(), 'RED documentaire : story RE-778 absente'
    story = STORY.read_text(encoding='utf-8')
    for text in (story, section()):
        for token in (
            'Après RE-777', 'Après RE-778', '24 septembre 2026', 'ELF32',
            'run03', 'BM_SUBTRACT', '988', 'DrawAggregatedSplits',
            'pas 988 frames', 'DrawPhaseGame', 'SetScreenFadeIn',
            'frame 16', 'frame 300', 'InitialiseSpotCam', 'CalculateSpotCams',
            'bDisableLaraControl', 'Δz=3450', 'Lara visible',
            '1 PASS, 1 FAIL', '3 tests PASS', 'revue indépendante',
            'source de production inchangée', 'code_change_readiness=blocked',
            'GetHeight', 'gameplay complet non validé', 'équivalence cible non validée',
            'aucun asset public', 'pas une sortie naturelle du jeu',
            'Revue indépendante de publication PASS borné au snapshot',
        ):
            assert token in text, token
        assert not re.search(r'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}|\b[0-9a-f]{64}\b', text)
        assert not re.search(r'<img\b|data:image|```(?:c|cpp|asm|mips)\b|<pre\b', text)
    assert '## Tracker' in story and '## Handoff' in story
    assert '- [x]' in story and '- [ ]' in story
    assert STORY.name in section()


def test_re778_dashboard_append_only_preserves_re777_bytes():
    before = subprocess.check_output(['git', 'show', f'{BASE}:docs/reverse/reconstruction-progress.html'], cwd=ROOT)
    current = DASH.read_bytes()
    assert current.count(b'<h2>RE-778 \xc2\xb7') == 1
    restored = re.sub(rb'<h2>RE-778 \xc2\xb7.*?(?=</body>)', b'', current, flags=re.S)
    assert restored == before
    assert current.count(b'</body>') == before.count(b'</body>') == 1
    assert current.count(b'</html>') == before.count(b'</html>') == 1


def test_re778_live_index_and_generator_preserve_history(tmp_path):
    index = INDEX.read_text(encoding='utf-8')
    assert 'Jalon actif : <a href="reconstruction-progress.html">RE-778 — fondu natif, intro caméra et contrôle libéré</a>' in index
    assert 'RE-777 — soumission et géométrie projetée du niveau' in index
    assert 'Historique clôturé — aucun backlog actif' in index
    assert write(build(ROOT), tmp_path).read_bytes() == INDEX.read_bytes()
