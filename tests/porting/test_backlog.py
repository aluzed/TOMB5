"""Documentary contracts only; no game build, runtime, or historical generators."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'docs/porting/backlog.json'


def load():
    assert DATA.exists(), 'functional backlog missing'
    return json.loads(DATA.read_text())


def module():
    path = ROOT / 'scripts/porting/render_backlog.py'
    assert path.exists(), 'renderer missing'
    spec = importlib.util.spec_from_file_location('port_backlog', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_initial_delivery_contract():
    data = load()
    assert data['date'] == '2026-09-13'
    assert data['scope_status'] == 'Proposed'
    assert '32' in data['scope'] and 'PSXPC_N' in data['scope']
    assert data['implementation_authorized'] is False
    assert 6 <= len(data['tickets']) <= 10
    assert data['drafted'] == len(data['tickets'])
    assert data['implemented'] == 0
    assert all(t['status'] in ('Todo', 'Blocked') for t in data['tickets'])
    assert len(data['domains']) >= 10
    assert {'Covered', 'Partial', 'To inventory', 'Separate'} <= {d['status'] for d in data['domains']}
    module().validate(data)


def test_ticket_contents_and_references():
    data = load()
    for t in data['tickets']:
        for key in ('id', 'title', 'status', 'reason', 'priority', 'goal', 'facts', 'scope',
                    'exclusions', 'dependencies', 'tasks', 'acceptance', 'validation',
                    'unknowns', 'estimate', 'confidence', 'references'):
            assert key in t, (t.get('id'), key)
        for key in ('tasks', 'acceptance', 'references'):
            assert len(t[key]) >= 2
        assert t['confidence'] in ('Low', 'Medium')
        for ref in t['references']:
            assert (ROOT / ref['path']).is_file(), ref
            assert 1 <= ref['line'] <= len((ROOT / ref['path']).read_text().splitlines())
        text = (ROOT / 'docs/porting' / (t['id'] + '.md')).read_text()
        assert f"Status: {t['status']}" in text
        assert text.count('- [ ]') >= len(t['tasks'])
        assert 'pas une mesure' in text


def test_generated_bytes_and_local_links():
    data = load()
    m = module()
    for name, expected in m.render(data).items():
        assert (ROOT / 'docs/porting' / name).read_text() == expected
    html = (ROOT / 'docs/porting/index.html').read_text()
    for t in data['tickets']:
        assert f'href="#{t["id"]}"' in html
        assert f'id="{t["id"]}"' in html
        assert f'href="{t["id"]}.md"' in html
    assert '0/8' in html
    assert 'menu interactif et gameplay non validés' in html
    assert 'snapshot' in html
    assert '<script' not in html and '<img' not in html


@pytest.mark.parametrize('mutation,error', [
    ('duplicate', 'duplicate'), ('missing', 'dependency'), ('cycle', 'cycle'),
    ('status', 'status'), ('count', 'drafted'), ('implementation', 'implemented'),
    ('scope', 'scope_status'), ('authorization', 'implementation_authorized'),
    ('blocked', 'reason'), ('domain', 'domain'),
])
def test_fail_closed(mutation, error):
    d = copy.deepcopy(load())
    if mutation == 'duplicate': d['tickets'][1]['id'] = d['tickets'][0]['id']
    elif mutation == 'missing': d['tickets'][0]['dependencies'] = ['PORT-999']
    elif mutation == 'cycle': d['tickets'][0]['dependencies'] = [d['tickets'][1]['id']]
    elif mutation == 'status': d['tickets'][0]['status'] = 'Done'
    elif mutation == 'count': d['drafted'] = 999
    elif mutation == 'implementation': d['implemented'] = 1
    elif mutation == 'scope': d['scope_status'] = 'Approved'
    elif mutation == 'authorization': d['implementation_authorized'] = True
    elif mutation == 'blocked': d['tickets'][1]['reason'] = ''
    elif mutation == 'domain': d['domains'][0]['tickets'] = ['PORT-999']
    with pytest.raises(ValueError, match=error):
        module().validate(d)
