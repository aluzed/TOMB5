#!/usr/bin/env python3
"""Render the live render-migration backlog (`render-backlog.json`).

Contrairement à `render_backlog.py` (lot initial figé du 13 septembre), ce
backlog-ci est **vivant** : les statuts évoluent avec l'avancement. Le
rendu produit `docs/porting/render/RMIG-xxx.md` (une fiche par ticket) et
`docs/porting/render/index.html` (tableau de suivi), plus un `README.md`.

Usage :
    python3 scripts/porting/render_tickets.py           # écrit les fichiers
    python3 scripts/porting/render_tickets.py --check   # échoue si dérive
"""
import argparse
import json
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'docs/porting/render-backlog.json'
OUT = ROOT / 'docs/porting/render'

STATUSES = ('Todo', 'In progress', 'Blocked', 'Done')
REQUIRED = ('id', 'title', 'status', 'priority', 'goal', 'facts', 'scope',
            'tasks', 'acceptance', 'validation', 'unknowns', 'estimate',
            'confidence', 'dependencies', 'references', 'progress', 'evidence')


def validate(data):
    def require(ok, name, detail=''):
        if not ok:
            raise ValueError('%s %s' % (name, detail))

    require(data.get('kind') == 'render-migration', 'kind')
    tickets = data['tickets']
    require(len(tickets) >= 6, 'ticket count')
    ids = [t['id'] for t in tickets]
    require(len(ids) == len(set(ids)), 'duplicate')
    require(all(re.fullmatch(r'RMIG-\d{3}', i) for i in ids), 'id')

    seen_done = 0
    graph = {}
    for t in tickets:
        for key in REQUIRED:
            require(key in t, 'field', '%s.%s' % (t.get('id'), key))
        require(t['status'] in STATUSES, 'status', t['id'])
        require(t['priority'] in ('P0', 'P1', 'P2'), 'priority', t['id'])
        require(t['confidence'] in ('Low', 'Medium'), 'confidence', t['id'])
        require(all(d in ids for d in t['dependencies']), 'dependency', t['id'])
        for key in ('tasks', 'acceptance', 'references'):
            require(len(t[key]) >= 1, key, t['id'])
        require(isinstance(t['evidence'], list), 'evidence', t['id'])
        require(len(t['tasks']) >= 2 and len(t['acceptance']) >= 2,
                'detail', t['id'])
        for ref in t['references']:
            path = ROOT / ref['path']
            require(path.is_file(), 'reference file', ref['path'])
            lines = path.read_text(errors='ignore').splitlines()
            require(1 <= ref['line'] <= max(1, len(lines)), 'reference line',
                    ref['path'])
        if t['status'] == 'Done':
            seen_done += 1
            require(bool(t['evidence'] and t['evidence'][0].get('note')),
                    'evidence', t['id'])
        graph[t['id']] = t['dependencies']

    done = set()

    def visit(node, ancestors):
        require(node not in ancestors, 'cycle', node)
        if node in done:
            return
        for dep in graph[node]:
            visit(dep, ancestors | {node})
        done.add(node)

    for node in ids:
        visit(node, set())

    # Un ticket non terminé ne peut pas dépendre d'un ticket non terminé qui
    # serait déclaré Done sans preuve : la cohérence est vérifiée ci-dessus.
    return seen_done


def render_ticket(t):
    lines = []
    lines.append('# %s — %s' % (t['id'], t['title']))
    lines.append('')
    lines.append('Status: **%s** — priorité %s — confiance %s' %
                 (t['status'], t['priority'], t['confidence']))
    lines.append('')
    lines.append('Avancement : %s' % t['progress'])
    lines.append('')
    lines.append('## Objectif')
    lines.append('')
    lines.append(t['goal'])
    lines.append('')
    lines.append('## Faits établis')
    lines.append('')
    lines.append(t['facts'])
    lines.append('')
    lines.append('## Périmètre')
    lines.append('')
    lines.append(t['scope'])
    if t.get('exclusions'):
        lines.append('')
        lines.append('Hors périmètre : %s' % t['exclusions'])
    lines.append('')
    lines.append('## Tâches')
    lines.append('')
    for task in t['tasks']:
        lines.append('- [ ] %s' % task)
    lines.append('')
    lines.append('## Critères d’acceptation')
    lines.append('')
    for item in t['acceptance']:
        lines.append('- %s' % item)
    lines.append('')
    lines.append('## Validation')
    lines.append('')
    lines.append(t['validation'])
    lines.append('')
    lines.append('## Inconnues')
    lines.append('')
    lines.append(t['unknowns'])
    lines.append('')
    lines.append('## Estimation')
    lines.append('')
    lines.append(t['estimate'])
    lines.append('')
    lines.append('## Dépendances')
    lines.append('')
    if t['dependencies']:
        for dep in t['dependencies']:
            lines.append('- %s' % dep)
    else:
        lines.append('- aucune')
    lines.append('')
    lines.append('## Preuves')
    lines.append('')
    if t['evidence']:
        for ev in t['evidence']:
            suffix = ' — `%s`' % ev['commit'] if ev.get('commit') else ''
            lines.append('- %s : %s%s' % (ev.get('date', '?'), ev['note'], suffix))
    else:
        lines.append('- à produire (aucune mesure pour l’instant)')
    lines.append('')
    lines.append('## Références')
    lines.append('')
    for ref in t['references']:
        note = ' (%s)' % ref['note'] if ref.get('note') else ''
        lines.append('- `%s:%s`%s' % (ref['path'], ref['line'], note))
    lines.append('')
    return '\n'.join(lines)


def render(data):
    validate(data)
    tickets = data['tickets']
    files = {}
    for t in tickets:
        files[t['id'] + '.md'] = render_ticket(t)

    counts = {s: sum(1 for t in tickets if t['status'] == s) for s in STATUSES}
    rows = []
    for t in tickets:
        rows.append('| %s | %s | %s | %s | %s |' % (
            t['id'], t['title'], t['status'], t['priority'],
            ', '.join(t['dependencies']) or '—'))

    index = ['# Backlog de migration du rendu (64 bits / Vulkan)', '']
    index.append(data['intro'])
    index.append('')
    index.append('## Suivi')
    index.append('')
    index.append('| id | ticket | statut | prio | dépend de |')
    index.append('| --- | --- | --- | --- | --- |')
    index.extend(rows)
    index.append('')
    index.append('**%d/%d terminés** — In progress : %d — Blocked : %d — Todo : %d' %
                 (counts['Done'], len(tickets), counts['In progress'],
                  counts['Blocked'], counts['Todo']))
    index.append('')
    index.append('Dernière mise à jour : %s' % data['updated'])
    index.append('')
    index.append('<ul>')
    for t in tickets:
        index.append('<li><a href="%s.md">%s — %s</a> : %s</li>' %
                     (t['id'], t['id'], escape(t['title']), t['status']))
    index.append('</ul>')
    files['index.html'] = '\n'.join(index) + '\n'

    readme = ['# Render migration (64 bits / Vulkan) — suivi', '']
    readme.append(data['intro'])
    readme.append('')
    readme.append('| id | ticket | statut | prio |')
    readme.append('| --- | --- | --- | --- |')
    for t in tickets:
        readme.append('| [%s](render/%s.md) | %s | %s | %s |' %
                      (t['id'], t['id'], t['title'], t['status'], t['priority']))
    readme.append('')
    readme.append('%d/%d terminés.' % (counts['Done'], len(tickets)))
    readme.append('')
    files['README.md'] = '\n'.join(readme)
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = json.loads(DATA.read_text())
    files = render(data)
    OUT.mkdir(parents=True, exist_ok=True)
    stale = []
    for name, content in files.items():
        path = OUT / name if name != 'README.md' else ROOT / 'docs/porting' / 'render-README.md'
        if args.check:
            if not path.exists() or path.read_text() != content:
                stale.append(str(path))
        else:
            path.write_text(content)
    if args.check and stale:
        raise SystemExit('drift: ' + ', '.join(stale))
    print('render backlog OK (%d tickets)' % len(data['tickets']))


if __name__ == '__main__':
    main()
