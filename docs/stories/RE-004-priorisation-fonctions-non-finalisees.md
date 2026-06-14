# RE-004 — Prioriser les fonctions non finalisées

Status: Todo
Owner: Unassigned
Priority: P1
Type: Planning

## Goal

Établir une backlog priorisée de fonctions à reverse en premier, en croisant le graphe d'appels Ghidra, les marqueurs repo et l'impact runtime.

## Candidate areas

- `GAME/` : logique partagée, plus gros volume de fonctions.
- `SPEC_PSXPC_N/` : chemin de debug/émulation PC pour code PSX.
- `EMULATOR/` : faible taux de fonctions finalisées selon le snapshot initial.
- Fonctions marquées `(ND)` : probablement présentes mais non validées fonctionnellement.
- Fonctions sans `(F)` proches du title screen et chargement niveau.

## Proposed files

- Create: `docs/reverse/backlog.md`
- Create: `docs/reverse/generated/function-priority.csv`

## Tasks

- [ ] Définir une scoring rule : callers, callees, absence de `(F)`, présence `(ND)`, module prioritaire.
- [ ] Consommer le mapping Ghidra/repo généré par RE-002.
- [ ] Classer les fonctions en lots de 5 à 10.
- [ ] Pour chaque lot, documenter les fichiers source à toucher et les preuves Ghidra à regarder.
- [ ] Identifier les fonctions bloquées par structures/types manquants.

## Acceptance criteria

- [ ] Une liste priorisée existe avec justification.
- [ ] Chaque entrée pointe vers un fichier source repo et une adresse Ghidra quand disponible.
- [ ] Les fonctions `(ND)` sont mises en évidence.
- [ ] Les lots sont assez petits pour être pris un par un.
