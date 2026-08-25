from pathlib import Path

from scripts.reverse.generate_tomb5_progress_dashboard import build, write


def test_dashboard_generator_tracks_latest_handoff_and_next_ticket(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    model = build(repo)

    assert model['latest_ticket'] == 'RE-530'
    assert model['next_ticket'] == 'RE-531'
    assert model['recent_ticket_count'] >= 83

    output = write(model, tmp_path)
    text = output.read_text(encoding='utf-8')
    assert 'RE-449' in text
    assert 'RE-450' in text
    assert 'Historique &amp; reste à faire' in text
