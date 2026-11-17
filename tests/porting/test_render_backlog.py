"""Contrats documentaires du backlog vivant de migration du rendu.

`docs/porting/render-backlog.json` suit la migration 64 bits/Vulkan/ImGui/RT.
Contrairement au lot initial figé (`backlog.json`), les statuts y évoluent :
ce test vérifie la cohérence du suivi (dépendances, cycles, preuves) et que
les fichiers rendus ne dérivent pas de la source.
"""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'docs/porting/render-backlog.json'
SCRIPT = ROOT / 'scripts/porting/render_tickets.py'
OUT = ROOT / 'docs/porting/render'


def load():
    assert DATA.exists(), 'render backlog missing'
    return json.loads(DATA.read_text())


def module():
    spec = importlib.util.spec_from_file_location('render_tickets', SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_schema_and_dependencies():
    data = load()
    mod = module()
    mod.validate(data)  # lève ValueError si incohérent
    ids = {t['id'] for t in data['tickets']}
    assert len(data['tickets']) >= 10
    assert 'RMIG-001' in ids
    for t in data['tickets']:
        assert t['status'] in ('Todo', 'In progress', 'Blocked', 'Done')
        assert all(dep in ids for dep in t['dependencies'])


def test_done_tickets_carry_evidence():
    data = load()
    done = [t for t in data['tickets'] if t['status'] == 'Done']
    assert done, 'au moins un ticket terminé (étude 32/64 bits)'
    for t in done:
        assert t['evidence'], t['id']
        assert any(ev.get('note') for ev in t['evidence']), t['id']


def test_generated_files_match_source():
    proc = subprocess.run([sys.executable, '-B', str(SCRIPT), '--check'],
                          capture_output=True, text=True, cwd=str(ROOT))
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_tracking_page_lists_every_ticket():
    data = load()
    html = (OUT / 'index.html').read_text()
    for t in data['tickets']:
        assert t['id'] in html
        assert t['title'] in html
        page = OUT / (t['id'] + '.md')
        assert page.exists()
        text = page.read_text()
        assert ('Status: **%s**' % t['status']) in text
        assert '## Critères d’acceptation' in text


def test_counts_are_consistent():
    data = load()
    tickets = data['tickets']
    done = sum(1 for t in tickets if t['status'] == 'Done')
    html = (OUT / 'index.html').read_text()
    assert ('**%d/%d terminés**' % (done, len(tickets))) in html
