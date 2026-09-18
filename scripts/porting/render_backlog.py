"""Render the initial functional planning tranche; no source or RE execution.

Edit docs/porting/backlog.json, then run this script. This first-delivery
contract deliberately rejects implementation progress: a future authorized
implementation milestone must explicitly evolve both schema and tests.
"""
import argparse
from html import escape
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs/porting'


def validate(data):
    def require(ok, name):
        if not ok:
            raise ValueError(name)
    require(data['scope_status'] == 'Proposed', 'scope_status')
    require(data['implementation_authorized'] is False, 'implementation_authorized')
    tickets = data['tickets']
    ids = [t['id'] for t in tickets]
    require(len(ids) == len(set(ids)), 'duplicate')
    require(all(re.fullmatch(r'PORT-\d{3}', i) for i in ids), 'id')
    require(6 <= len(ids) <= 10, 'ticket count')
    require(data['drafted'] == len(ids), 'drafted')
    require(data['implemented'] == 0, 'implemented')
    graph = {}
    for t in tickets:
        require(t['status'] in ('Todo', 'Blocked'), 'status')
        require(bool(t['reason'].strip()), 'reason')
        require(t['priority'] in ('P0', 'P1', 'P2'), 'priority')
        require(all(d in ids for d in t['dependencies']), 'dependency')
        graph[t['id']] = t['dependencies']
        for field in ('goal', 'facts', 'scope', 'exclusions', 'validation', 'unknowns', 'estimate', 'confidence'):
            require(bool(t[field]), field)
        for field in ('tasks', 'acceptance', 'references'):
            require(len(t[field]) >= 2, field)
    done = set()
    def visit(node, ancestors):
        require(node not in ancestors, 'cycle')
        if node in done:
            return
        for dep in graph[node]:
            visit(dep, ancestors | {node})
        done.add(node)
    for node in ids:
        visit(node, set())
    for d in data['domains']:
        require(d['status'] in ('Covered', 'Partial', 'To inventory', 'Separate'), 'domain status')
        require(all(i in ids for i in d['tickets']), 'domain dependency')


def render(data):
    validate(data)
    tickets = data['tickets']
    count = len(tickets)
    note = ('Backlog fonctionnel initial, distinct des tickets historiques RE. '
            'Rédaction terminée ne signifie pas fonctionnalité terminée. '
            'Aucune implémentation, nouvelle RE binaire, compilation ou exécution du jeu dans ce lot. '
            'État hérité de RE-772 : build64 crash LoadLevel ; build32 splash 30 secondes, '
            'timeout 124 ; menu interactif et gameplay non validés. '
            'Les tests de ce backlog valident les documents, pas le jeu.')
    counts = f'Rédaction : {data["drafted"]}/{count} tickets. Implémentation validée dans ce lot : {data["implemented"]}/{count}.'
    intro = (f'# TOMB5 — Backlog fonctionnel, lot initial\n\nDate : {data["date"]} (Europe/Paris). '
             f'Base inspectée : `{data["baseline"]}`.\n\n{data["scope"]}\n\n{note}\n\n{counts}\n\n'
             '## Convention et progression\n\n'
             'P0 = prérequis du premier socle jouable ; P1 = boucle utilisateur intégrée suivante. '
             'Todo = prêt à planifier, non commencé ; Blocked = recette intégrée dépendante de tickets non validés. '
             'Ces dépendances sont des portes de validation : une préparation parallèle peut être proposée, '
             'mais ne change pas leur statut et ne crée pas de cycle. Aucun ticket Done. '
             'Chaque modification d’implémentation nécessite une nouvelle autorisation ; le rédacteur ne marque pas les tâches fonctionnelles [x].\n\n'
             '- [x] Cadrage initial étiqueté comme proposition.\n'
             '- [x] Premier lot rédigé avec références et dépendances.\n'
             '- [ ] Cadrage cible définitivement accepté par l’utilisateur.\n'
             '- [ ] Implémentation et recettes des PORT validées.\n'
             '- [ ] Domaines restants inventoriés ; backlog non exhaustif.\n\n'
             '## Tickets\n\n| ID | Priorité | Status | Objectif | Dépendances |\n|---|---|---|---|---|\n')
    files = {}
    sections = []
    rows = []
    for t in tickets:
        tid = t['id']
        deps = ', '.join(t['dependencies']) or 'Aucune'
        intro += f'| [{tid}]({tid}.md) | {t["priority"]} | {t["status"]} | {t["title"]} | {deps} |\n'
        md = (f'# {tid} — {t["title"]}\n\n[Tracker](README.md) · [Tableau HTML](index.html#{tid})\n\n'
              f'Status: {t["status"]}\n\nPriorité : {t["priority"]}\n\nMotif : {t["reason"]}\n\n'
              f'Dépendances : {deps}\n\nCadrage proposé : {data["scope"]}\n\n'
              f'## Objectif utilisateur\n\n{t["goal"]}\n\n'
              f'## Faits existants — base {data["baseline"]}\n\n{t["facts"]}\n\n'
              f'## Portée\n\n{t["scope"]}\n\n## Exclusions\n\n{t["exclusions"]}\n\n'
              '## Tâches — implémentation non commencée\n\n' + ''.join('- [ ] '+v+'\n' for v in t['tasks']) +
              '\n## Critères d’acceptation futurs\n\n' + ''.join('- [ ] '+v+'\n' for v in t['acceptance']) +
              f'\n## Validation et capture attendues\n\n{t["validation"]}\n\n'
              'Captures, assets, exécutables et données restent dans des dossiers ignorés ; seuls scripts, tests et métadonnées sûrs seront versionnables.\n\n'
              f'## Inconnues\n\n{t["unknowns"]}\n\n'
              f'## Estimation indicative\n\n{t["estimate"]} Confiance : {t["confidence"]}. '
              'Jugement de planification, pas une mesure ; à réviser après les dépendances, non une promesse de délai.\n\n'
              '## Références consultables\n\n' + ''.join(f'- `{r["path"]}:{r["line"]}` — {r["note"]}.\n' for r in t['references']) +
              '\n## Progression séparée\n\n- [x] Ticket rédigé.\n- [ ] Travail fonctionnel autorisé et démarré.\n- [ ] Recette observable validée ; revue avant passage à Done.\n')
        files[tid+'.md'] = md
        rows.append(f'<tr><th><a href="#{tid}">{tid}</a></th><td>{escape(t["priority"])}</td><td>{escape(t["status"])}</td><td>{escape(t["title"])}</td><td>{escape(deps)}</td></tr>')
        sections.append(f'<section id="{tid}"><h2>{tid} — {escape(t["title"])}</h2><p><a href="{tid}.md">Fiche Markdown</a></p><pre>{escape(md)}</pre></section>')
    intro += '\n## Couverture du backlog, pas complétion du port\n\n| Domaine | Couverture | Tickets | Reste / limite |\n|---|---|---|---|\n'
    domain_rows = []
    for d in data['domains']:
        refs = ', '.join(d['tickets']) or '—'
        intro += f'| {d["name"]} | {d["status"]} | {refs} | {d["note"]} |\n'
        domain_rows.append('<tr>'+''.join('<td>'+escape(v)+'</td>' for v in (d['name'],d['status'],refs,d['note']))+'</tr>')
    intro += ('\nCovered = périmètre borné décrit ; Partial = une tranche décrite ; To inventory = pas encore détaillé ; Separate = chantier distinct. '
              'Aucun de ces libellés ne valide le fonctionnement du jeu.\n\n## Estimation et suite\n\n'+data['estimate_note']+
              '\n\nProchaine décision : confirmer la cible proposée et autoriser séparément PORT-001/002 ; '
              'poursuivre le backlog combat/IA, puzzles, eau, cinématiques et campagne après arbitrage. '
              'Le rapport distinct de 20:30 peut réestimer à partir de ce lot ; aucune nouvelle cartographie après 20:30 dans la fenêtre autorisée.\n\n'
              '## Maintenance et vérification documentaire\n\n'
              '`backlog.json` est la source éditoriale. Régénérer avec `python3 scripts/porting/render_backlog.py`. '
              'Contrôler sans écriture avec `python3 scripts/porting/render_backlog.py --check`.\n\n'
              '`PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider tests/porting/test_backlog.py`\n\n'
              'Les garde-fous de ce lot initial refusent Done/autorisation d’implémentation ; faire évoluer explicitement contrat et tests lors d’un futur lot autorisé. '
              'Le HTML partagé est un snapshot documentaire, sans image ni asset. Le dashboard reconstruction historique n’est pas régénéré.\n')
    files['README.md'] = intro
    files['index.html'] = ('<!doctype html>\n<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
        '<title>TOMB5 — Backlog fonctionnel</title><style>'
        'body{font:16px/1.6 system-ui,sans-serif;max-width:1120px;margin:auto;padding:24px;color:#18293a;background:#f6f8fb}'
        'h1,h2{line-height:1.25}a{color:#075a9c}table{width:100%;border-collapse:collapse;background:white}th,td{border:1px solid #ccd5df;padding:10px;text-align:left}'
        '.scroll{overflow-x:auto}.notice{padding:18px;border-left:5px solid #a66a00;background:#fff4d9}pre{font:inherit;white-space:pre-wrap;overflow-wrap:anywhere}section{margin:32px 0;padding:20px;background:white;border:1px solid #ccd5df}'
        '</style></head><body><h1>TOMB5 — Premier backlog fonctionnel</h1>'
        f'<p>Copie snapshot documentaire du {data["date"]} · base {data["baseline"]} · <a href="README.md">Tracker Markdown</a></p>'
        f'<div class="notice"><strong>{escape(data["scope"])}</strong><p>{escape(note)}</p></div>'
        f'<h2>Deux progressions distinctes</h2><p><strong>{escape(counts)}</strong> Aucun pourcentage de portage complet.</p>'
        '<p>Todo : prêt à planifier, non commencé. Blocked : dépendances de recette non validées. P0 : socle jouable ; P1 : boucle intégrée suivante. Rédiger ≠ implémenter.</p>'
        '<div class="scroll"><table><caption>8 tickets proposés, aucune implémentation autorisée</caption><thead><tr><th>ID</th><th>Priorité</th><th>Status</th><th>Objectif</th><th>Dépendances</th></tr></thead><tbody>'+
        ''.join(rows)+'</tbody></table></div><h2>Couverture : backlog non exhaustif</h2>'
        '<p>Covered : périmètre borné décrit ; Partial : tranche décrite ; To inventory : à inventorier ; Separate : chantier distinct. Ce ne sont pas des statuts de jeu.</p>'
        '<div class="scroll"><table><thead><tr><th>Domaine</th><th>Couverture</th><th>Tickets</th><th>Reste / limite</th></tr></thead><tbody>'+
        ''.join(domain_rows)+'</tbody></table></div><h2>Estimation indicative et suite</h2><p>'+escape(data['estimate_note'])+
        '</p><p>Prochaine décision : confirmer la cible, puis autoriser séparément PORT-001/002. Les preuves historiques RE restent distinctes ; GetHeight/callback SOURCE ne signifie pas correctif validé.</p>'+
        ''.join(sections)+'</body></html>\n')
    # The initial lot above is a frozen planning snapshot, including its denial
    # of implementation authorization. A separately dated execution overlay does
    # not convert that historical permission or its counters into current truth.
    if 'progress' in data:
        p = data['progress']
        if (p['ticket'] not in {t['id'] for t in tickets}
                or p['status'] != 'In progress'
                or not p['authorization_until'] or not p['summary']):
            raise ValueError('active progress')
        active = (f'## Progression active du {p["date"]}\n\n'
                  f'{p["ticket"]} — **{p["status"]}**. Autorisation technique bornée jusqu’au '
                  f'{p["authorization_until"]} ; elle ne valide pas définitivement la cible.\n\n'
                  f'{p["summary"]}\n\nRecette : [Linux32](linux32.md).\n\n'
                  'Les statuts, compteurs et restrictions du lot initial ci-dessous restent '
                  'un historique du 13 septembre, pas une nouvelle demande de GO. '
                  'Aucun ticket accepté Done.\n\n')
        files['README.md'] = active + files['README.md']
        ticket_file = p['ticket'] + '.md'
        files[ticket_file] = active + 'Status: In progress\n\n## Fiche initiale historique\n\n' + files[ticket_file]
        old_section = next(s for s in sections if s.startswith(f'<section id="{p["ticket"]}">'))
        new_section = old_section[:old_section.index('<pre>')] + '<pre>' + escape(files[ticket_file]) + '</pre></section>'
        files['index.html'] = files['index.html'].replace(old_section, new_section, 1)
        html_active = '<aside><pre>' + escape(active) + '</pre><a href="linux32.md">Recette Linux32</a></aside>'
        files['index.html'] = files['index.html'].replace('<body>', '<body>' + html_active, 1)
    if 'runtime_progress' in data:
        p = data['runtime_progress']
        if (p['ticket'] != 'PORT-002' or p['status'] != 'In progress'
                or not p['authorization_until'] or not p['summary']):
            raise ValueError('runtime progress')
        runtime = (f'## Progression runtime du {p["date"]}\n\n'
                   f'{p["ticket"]} — **{p["status"]}** ; PORT-001 reste en cours. '
                   f'Autorisation jusqu’au {p["authorization_until"]}. Linux32 provisoire.\n\n'
                   f'{p["summary"]}\n\nDétails : [preuve runtime](runtime-menu.md).\n\n'
                   'Les blocs antérieurs ci-dessous sont historiques, y compris leur '
                   'ancienne échéance et leurs réserves visuelles. Aucun Done attribué.\n\n')
        for name in ('PORT-001.md', 'PORT-002.md', 'README.md'):
            files[name] = runtime + files[name]
        html = ('<aside id="runtime-progress"><pre>' + escape(runtime)
                + '</pre><a href="runtime-menu.md">Preuve runtime</a></aside>'
                + '<!-- runtime milestone end -->')
        files['index.html'] = files['index.html'].replace('<body>', '<body>' + html, 1)
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = json.loads((OUT / 'backlog.json').read_text())
    for name, content in render(data).items():
        path = OUT / name
        if args.check:
            if not path.exists() or path.read_text() != content:
                raise SystemExit('drift: '+str(path))
        else:
            path.write_text(content)
    print('documentary backlog OK; no game validation')


if __name__ == '__main__':
    main()
