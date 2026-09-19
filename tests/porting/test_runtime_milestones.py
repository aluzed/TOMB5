"""Documentary milestone history, not runtime/gameplay tests."""
import copy
import importlib.util
import json
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('renderer', ROOT / 'scripts/porting/render_backlog.py')
renderer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(renderer)


def fixture():
    data = json.loads((ROOT / 'docs/porting/backlog.json').read_text())
    data.pop('runtime_milestones', None)
    return data


def milestone():
    return {'date': '2026-09-19', 'authorization_until': '2026-09-19T10:00:00+02:00',
            'tickets': ['PORT-002', 'PORT-003'], 'status': 'In progress',
            'summary': 'Scène bornée <test>; campagne non validée.'}


def test_append_preserves_historical_markdown_and_html():
    data = fixture()
    old = renderer.render(data)
    data['runtime_milestones'] = [milestone()]
    new = renderer.render(data)
    for name in ('README.md', 'PORT-002.md', 'PORT-003.md'):
        assert new[name].endswith(old[name])
        assert new[name].startswith('## Progression vérifiée du 2026-09-19')
        assert 'In progress' in new[name].split('##', 2)[1]
    assert new['PORT-001.md'] == old['PORT-001.md']
    assert '&lt;test&gt;' in new['index.html']
    assert '<test>' not in new['index.html']
    assert '<aside id="runtime-progress">' in new['index.html']
    assert 'runtime-level.md' in new['index.html']


@pytest.mark.parametrize('field,value', [
    ('status', 'Done'), ('status', 'Blocked'), ('summary', ''),
    ('date', ''), ('authorization_until', ''), ('tickets', []),
    ('tickets', ['PORT-999']), ('tickets', ['PORT-003', 'PORT-003']),
])
def test_milestone_rejects_invalid_claims(field, value):
    data = fixture()
    item = copy.deepcopy(milestone())
    item[field] = value
    data['runtime_milestones'] = [item]
    with pytest.raises(ValueError, match='runtime milestone'):
        renderer.render(data)
