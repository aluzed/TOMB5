import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from scripts.reverse.generate_tomb5_progress_dashboard import build, write


def test_dashboard_generator_tracks_latest_handoff_and_next_ticket(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    model = build(repo)

    assert model['latest_ticket'] == 'RE-723'
    assert model['next_ticket'] == 'TBD'
    assert model['next_topic'] == 'none'
    assert model['stop_condition'] == ('external source-backed behavioral contracts and ABI proof are required '
                                       'before reopening this inventory')
    assert model['history_heading'] == 'Historique clôturé — aucun backlog actif'
    assert model['recent_ticket_count'] >= 151
    dashboard = (repo / 'docs/reverse/tomb5-progress-dashboard.html').read_text(encoding='utf-8')
    assert 'RE-720' in dashboard
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


def test_dashboard_generator_rejects_terminal_handoff_without_stop_condition(tmp_path):
    generated = tmp_path / 'docs/reverse/generated'
    generated.mkdir(parents=True)
    (generated / 're705-incomplete-handoff.csv').write_text(
        'story_id,topic,next_ticket,next_topic,stop_condition\n'
        'RE-705,terminal-proof-intake,TBD,none,\n',
        encoding='utf-8',
    )

    with pytest.raises(ValueError, match='incomplete terminal handoff stop_condition: re705-incomplete-handoff.csv'):
        build(tmp_path)


def test_dashboard_generator_rejects_a_whitespace_only_terminal_stop_condition(tmp_path):
    generated = tmp_path / 'docs/reverse/generated'
    generated.mkdir(parents=True)
    (generated / 're716-whitespace-stop-handoff.csv').write_text(
        'story_id,topic,next_ticket,next_topic,stop_condition\n'
        'RE-716,terminal-proof-intake,TBD,none,   \n',
        encoding='utf-8',
    )

    with pytest.raises(ValueError, match='incomplete terminal handoff stop_condition: re716-whitespace-stop-handoff.csv'):
        build(tmp_path)


@pytest.mark.parametrize('predecessor', ('', 'RE-717', 'RE-719', 'not-a-ticket'))
def test_dashboard_generator_rejects_an_incoherent_declared_terminal_predecessor(tmp_path, predecessor):
    generated = tmp_path / 'docs/reverse/generated'
    generated.mkdir(parents=True)
    (generated / 're719-incoherent-predecessor-handoff.csv').write_text(
        'story_id,topic,predecessor,next_ticket,next_topic,stop_condition\n'
        f'RE-719,terminal-handoff-predecessor-coherence,{predecessor},TBD,none,external proof required\n',
        encoding='utf-8',
    )

    with pytest.raises(ValueError, match='incoherent terminal handoff predecessor: re719-incoherent-predecessor-handoff.csv'):
        build(tmp_path)


@pytest.mark.parametrize('placeholder', ('none', ' TBD ', 'Unknown', 'n/a', '?'))
def test_dashboard_generator_rejects_a_placeholder_terminal_topic(tmp_path, placeholder):
    generated = tmp_path / 'docs/reverse/generated'
    generated.mkdir(parents=True)
    (generated / 're718-placeholder-topic-handoff.csv').write_text(
        'story_id,topic,next_ticket,next_topic,stop_condition\n'
        f'RE-718,{placeholder},TBD,none,external proof required\n',
        encoding='utf-8',
    )

    with pytest.raises(ValueError, match='unmeaningful terminal handoff topic: re718-placeholder-topic-handoff.csv'):
        build(tmp_path)


@pytest.mark.parametrize('placeholder', ('none', ' TBD ', 'Unknown', 'n/a', '?'))
def test_dashboard_generator_rejects_a_placeholder_terminal_stop_condition(tmp_path, placeholder):
    generated = tmp_path / 'docs/reverse/generated'
    generated.mkdir(parents=True)
    (generated / 're717-placeholder-stop-handoff.csv').write_text(
        'story_id,topic,next_ticket,next_topic,stop_condition\n'
        f'RE-717,terminal-proof-intake,TBD,none,{placeholder}\n',
        encoding='utf-8',
    )

    with pytest.raises(ValueError, match='unmeaningful terminal handoff stop_condition: re717-placeholder-stop-handoff.csv'):
        build(tmp_path)


@pytest.mark.parametrize(('field', 'value'), (
    ('topic', 'terminal\tproof-intake'),
    ('next_ticket', 'TBD\x7f'),
    ('next_topic', 'no\nnone'),
    ('stop_condition', 'external\nproof required'),
    ('stop_condition', 'external\x85proof required'),
    ('stop_condition', 'external\u200bproof required'),
    ('stop_condition', 'external\u2028proof required'),
))
def test_dashboard_generator_rejects_control_characters_in_terminal_fields(tmp_path, field, value):
    generated = tmp_path / 'docs/reverse/generated'
    generated.mkdir(parents=True)
    row = {
        'story_id': 'RE-720', 'topic': 'terminal-proof-intake', 'next_ticket': 'TBD',
        'next_topic': 'none', 'stop_condition': 'external proof required',
    }
    row[field] = value
    (generated / 're720-control-character-handoff.csv').write_text(
        'story_id,topic,next_ticket,next_topic,stop_condition\n'
        + ','.join(f'"{row[name]}"' for name in ('story_id', 'topic', 'next_ticket', 'next_topic', 'stop_condition')) + '\n',
        encoding='utf-8',
    )

    with pytest.raises(ValueError, match=f'unsafe terminal handoff {field}: re720-control-character-handoff.csv'):
        build(tmp_path)


def test_dashboard_generator_rejects_a_closed_terminal_handoff_with_a_next_topic(tmp_path):
    generated = tmp_path / 'docs/reverse/generated'
    generated.mkdir(parents=True)
    (generated / 're706-ambiguous-handoff.csv').write_text(
        'story_id,topic,next_ticket,next_topic,stop_condition\n'
        'RE-706,terminal-proof-intake,TBD,source-contract-intake,external proof required\n',
        encoding='utf-8',
    )

    with pytest.raises(ValueError, match='incoherent terminal handoff direction: re706-ambiguous-handoff.csv'):
        build(tmp_path)


def test_dashboard_generator_rejects_a_multirow_handoff_instead_of_silently_using_its_first_row(tmp_path):
    generated = tmp_path / 'docs/reverse/generated'
    generated.mkdir(parents=True)
    (generated / 're707-ambiguous-handoff.csv').write_text(
        'story_id,topic,next_ticket,next_topic,stop_condition\n'
        'RE-707,terminal-proof-intake,TBD,none,external proof required\n'
        'RE-708,unauthorized-reopen,RE-709,unsafe,\n',
        encoding='utf-8',
    )

    with pytest.raises(ValueError, match='invalid handoff: re707-ambiguous-handoff.csv'):
        build(tmp_path)


def test_dashboard_generator_rejects_a_handoff_with_a_story_id_that_disagrees_with_its_filename(tmp_path):
    generated = tmp_path / 'docs/reverse/generated'
    generated.mkdir(parents=True)
    (generated / 're707-invalid-handoff.csv').write_text(
        'story_id,topic,next_ticket,next_topic,stop_condition\n'
        'RE-708,terminal-proof-intake,TBD,none,external proof required\n',
        encoding='utf-8',
    )

    with pytest.raises(ValueError, match='invalid handoff story_id: re707-invalid-handoff.csv'):
        build(tmp_path)


def test_dashboard_generator_rejects_a_handoff_without_a_story_id(tmp_path):
    generated = tmp_path / 'docs/reverse/generated'
    generated.mkdir(parents=True)
    (generated / 're708-missing-story-id-handoff.csv').write_text(
        'story_id,topic,next_ticket,next_topic,stop_condition\n'
        ',terminal-proof-intake,TBD,none,external proof required\n',
        encoding='utf-8',
    )

    with pytest.raises(ValueError, match='invalid handoff story_id: re708-missing-story-id-handoff.csv'):
        build(tmp_path)


def test_dashboard_generator_preserves_legacy_handoffs_without_story_ids(tmp_path):
    generated = tmp_path / 'docs/reverse/generated'
    generated.mkdir(parents=True)
    (generated / 're148-legacy-handoff.csv').write_text(
        'topic,next_ticket,next_topic,stop_condition\n'
        'legacy,RE-149,next,legacy format\n',
        encoding='utf-8',
    )
    (generated / 're708-current-handoff.csv').write_text(
        'story_id,topic,next_ticket,next_topic,stop_condition\n'
        'RE-708,current,TBD,none,external proof required\n',
        encoding='utf-8',
    )

    model = build(tmp_path)

    assert model['latest_ticket'] == 'RE-708'


def test_dashboard_generator_rejects_duplicate_terminal_ticket_handoffs(tmp_path):
    generated = tmp_path / 'docs/reverse/generated'
    generated.mkdir(parents=True)
    for suffix in ('authoritative', 'shadow'):
        (generated / f're709-{suffix}-handoff.csv').write_text(
            'story_id,topic,next_ticket,next_topic,stop_condition\n'
            'RE-709,terminal-proof-intake,TBD,none,external proof required\n',
            encoding='utf-8',
        )

    with pytest.raises(ValueError, match='ambiguous terminal handoff ticket: RE-709'):
        build(tmp_path)


def test_dashboard_generator_rejects_a_terminal_handoff_without_next_ticket(tmp_path):
    generated = tmp_path / 'docs/reverse/generated'
    generated.mkdir(parents=True)
    (generated / 're710-missing-direction-handoff.csv').write_text(
        'story_id,topic,next_ticket,next_topic,stop_condition\n'
        'RE-710,terminal-proof-intake,,none,external proof required\n',
        encoding='utf-8',
    )

    with pytest.raises(ValueError, match='incomplete terminal handoff next_ticket: re710-missing-direction-handoff.csv'):
        build(tmp_path)


@pytest.mark.parametrize(
    ('next_ticket', 'next_topic', 'message'),
    [
        ('later', 'proof-intake', 'invalid terminal handoff next_ticket'),
        ('TBD', 'proof-intake', 'incoherent terminal handoff direction'),
        ('RE-712', 'none', 'incoherent terminal handoff direction'),
        ('RE-713', 'proof-intake', 'non-successor terminal handoff next_ticket'),
    ],
)
def test_dashboard_generator_rejects_an_incoherent_terminal_direction(tmp_path, next_ticket, next_topic, message):
    generated = tmp_path / 'docs/reverse/generated'
    generated.mkdir(parents=True)
    (generated / 're711-incoherent-direction-handoff.csv').write_text(
        'story_id,topic,next_ticket,next_topic,stop_condition\n'
        f'RE-711,terminal-proof-intake,{next_ticket},{next_topic},external proof required\n',
        encoding='utf-8',
    )

    with pytest.raises(ValueError, match=message):
        build(tmp_path)


@pytest.mark.parametrize('next_ticket', ('RE-711', 'RE-710'))
def test_dashboard_generator_rejects_a_non_forward_terminal_successor(tmp_path, next_ticket):
    generated = tmp_path / 'docs/reverse/generated'
    generated.mkdir(parents=True)
    (generated / 're712-non-forward-handoff.csv').write_text(
        'story_id,topic,next_ticket,next_topic,stop_condition\n'
        f'RE-712,terminal-proof-intake,{next_ticket},proof-intake,external proof required\n',
        encoding='utf-8',
    )

    with pytest.raises(ValueError, match='non-successor terminal handoff next_ticket: re712-non-forward-handoff.csv'):
        build(tmp_path)


def test_dashboard_generator_rejects_a_terminal_successor_without_its_handoff(tmp_path):
    generated = tmp_path / 'docs/reverse/generated'
    generated.mkdir(parents=True)
    (generated / 're713-dangling-handoff.csv').write_text(
        'story_id,topic,next_ticket,next_topic,stop_condition\n'
        'RE-713,terminal-proof-intake,RE-714,proof-intake,external proof required\n',
        encoding='utf-8',
    )

    with pytest.raises(ValueError, match='dangling latest terminal handoff successor: RE-713'):
        build(tmp_path)


def test_dashboard_generator_rejects_duplicate_handoff_headers(tmp_path):
    generated = tmp_path / 'docs/reverse/generated'
    generated.mkdir(parents=True)
    (generated / 're714-duplicate-header-handoff.csv').write_text(
        'story_id,topic,next_ticket,next_ticket,next_topic,stop_condition\n'
        'RE-714,terminal-proof-intake,RE-715,TBD,none,external proof required\n',
        encoding='utf-8',
    )

    with pytest.raises(ValueError, match='invalid handoff: re714-duplicate-header-handoff.csv'):
        build(tmp_path)
