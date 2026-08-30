import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from scripts.reverse.generate_tomb5_progress_dashboard import build, write


def test_dashboard_generator_tracks_latest_handoff_and_next_ticket(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    model = build(repo)

    assert model['latest_ticket'] == 'RE-702'
    assert model['next_ticket'] == 'TBD'
    assert model['next_topic'] == 'none'
    assert model['stop_condition'] == ('external source-backed behavioral contracts and ABI proof are required '
                                       'before reopening this inventory')
    assert model['history_heading'] == 'Historique clôturé — aucun backlog actif'
    assert model['recent_ticket_count'] >= 151
    dashboard = (repo / 'docs/reverse/tomb5-progress-dashboard.html').read_text(encoding='utf-8')
    assert 'RE-702' in dashboard
    assert 'TBD' in dashboard
    assert 'Statut terminal : external source-backed behavioral contracts and ABI proof are required before reopening this inventory' in dashboard

    output = write(model, tmp_path)
    text = output.read_text(encoding='utf-8')
    assert 'Statut terminal : external source-backed behavioral contracts and ABI proof are required before reopening this inventory' in text
    assert 'Historique clôturé — aucun backlog actif' in text
    assert 'Historique &amp; reste à faire' not in text
    assert write(model, tmp_path).read_bytes() == text.encode('utf-8')
    assert 'RE-449' in text
    assert 'RE-450' in text
    assert 'RE-700' in text


def test_dashboard_generator_marks_terminal_handoff_without_stop_condition_incomplete(tmp_path):
    generated = tmp_path / 'docs/reverse/generated'
    generated.mkdir(parents=True)
    (generated / 're705-incomplete-handoff.csv').write_text(
        'story_id,topic,next_ticket,next_topic,stop_condition\n'
        'RE-705,terminal-proof-intake,TBD,none,\n',
        encoding='utf-8',
    )

    model = build(tmp_path)

    assert model['latest_ticket'] == 'RE-705'
    assert model['history_heading'] == 'État terminal incomplet — validation requise'
    assert 'backlog actif' not in model['history_heading']

    text = write(model, tmp_path).read_text(encoding='utf-8')
    assert '<h2>État terminal incomplet — validation requise</h2>' in text
    assert 'Historique clôturé — aucun backlog actif' not in text
    assert 'Historique &amp; reste à faire' not in text
