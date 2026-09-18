"""Active implementation overlay does not rewrite the initial planning contract."""
import json
from test_backlog import DATA, module


def test_authorized_progress_overlay():
    data = json.loads(DATA.read_text())
    progress = data['progress']
    assert progress['date'] == '2026-09-18'
    assert progress['authorization_until'] == '2026-09-18T08:30:00+02:00'
    assert progress['ticket'] == 'PORT-001'
    assert progress['status'] == 'In progress'
    assert data['implementation_authorized'] is False  # initial documentary lot
    outputs = module().render(data)
    for name in ('PORT-001.md', 'README.md', 'index.html'):
        assert 'Progression active du 2026-09-18' in outputs[name]
        assert 'linux32.md' in outputs[name]
        assert 'WM_DELETE_WINDOW' in outputs[name]
        assert 'menu et gameplay non validés' in outputs[name]
    assert 'Status: In progress' in outputs['PORT-001.md']
    for name in ('PORT-002.md', 'PORT-003.md'):
        assert 'Progression active' not in outputs[name]
