"""Documentary assertions only; do not claim execution of private proofs."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_september20_active_milestone_is_bounded():
    data = json.loads((ROOT / 'docs/porting/backlog.json').read_text())
    active = data['runtime_milestones'][-1]
    assert active['date'] == '2026-09-20'
    assert active['authorization_until'] == '2026-09-20T12:00:00+02:00'
    assert active['status'] == 'In progress'
    for text in ('R22', 'mgLOS', 'LookCamera reste stub', '446', '13 captures'):
        assert text in active['summary']
    for path in ('README.md', 'PORT-004.md', 'PORT-005.md', 'index.html'):
        text = (ROOT / 'docs/porting' / path).read_text()
        assert '2026-09-20' in text and 'LookCamera reste stub' in text


def test_new_proof_note_separates_game_fixes_and_private_camera():
    text = (ROOT / 'docs/porting/camera-foundations.md').read_text()
    for token in ('66 failed / 18 passed', '28 failed / 83 passed',
                  '446 passed', '79/79', '12/79', 'géométrie',
                  '11/12', 'non intégré', 'MEDIA', '[x]', '[ ]'):
        assert token in text
    assert 'oracle matériel' in text
