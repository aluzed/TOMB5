"""Runtime milestone overlay preserves both earlier documentary snapshots."""
import copy
import json
import pytest
from test_backlog import DATA, module


def test_historical_runtime_overlay_preserves_earlier_history():
    data = json.loads(DATA.read_text())
    # Isolate the September 18 overlay; later append-only milestones have
    # their own preservation contract in test_runtime_milestones.py.
    data.pop('runtime_milestones', None)
    p = data['runtime_progress']
    assert p['ticket'] == 'PORT-002'
    assert p['status'] == 'In progress'
    assert p['authorization_until'] == '2026-09-18T10:30:00+02:00'
    assert p['date'] == '2026-09-18'
    assert 'SIGILL' in p['summary']
    assert 'gameplay non validé' in p['summary']
    baseline = copy.deepcopy(data)
    del baseline['runtime_progress']
    old = module().render(baseline)
    new = module().render(data)
    for name in ('PORT-001.md', 'PORT-002.md', 'README.md', 'index.html'):
        assert 'Progression runtime du 2026-09-18' in new[name]
        assert 'runtime-menu.md' in new[name]
        assert old[name] in new[name] if name != 'index.html' else (
            new[name].split('<!-- runtime milestone end -->', 1)[1] == old[name].split('<body>', 1)[1])
    for name in old:
        if name not in ('PORT-001.md', 'PORT-002.md', 'README.md', 'index.html'):
            assert new[name] == old[name]
    assert data['implemented'] == 0
    assert data['progress'] == baseline['progress']


@pytest.mark.parametrize('field,value', [('status', 'Done'), ('ticket', 'PORT-999'),
                                        ('authorization_until', ''), ('summary', '')])
def test_runtime_overlay_fails_closed(field, value):
    data = json.loads(DATA.read_text())
    data['runtime_progress'][field] = value
    with pytest.raises(ValueError, match='runtime progress'):
        module().render(data)
