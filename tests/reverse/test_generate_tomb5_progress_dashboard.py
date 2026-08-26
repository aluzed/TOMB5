import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from scripts.reverse.generate_tomb5_progress_dashboard import build, write


def test_dashboard_generator_tracks_latest_handoff_and_next_ticket(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    model = build(repo)

    assert model['latest_ticket'] == 'RE-643'
    assert model['next_ticket'] == 'RE-644'
    assert model['recent_ticket_count'] >= 147

    output = write(model, tmp_path)
    text = output.read_text(encoding='utf-8')
    assert 'RE-449' in text
    assert 'RE-450' in text
    assert 'Historique &amp; reste à faire' in text
