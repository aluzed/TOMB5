# RE-004 — Prioriser les fonctions non finalisées

Status: Done
Owner: Hermes
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

- Created: `docs/reverse/backlog.md`
- Created: `docs/reverse/generated/function-priority.csv`
- Created: `scripts/reverse/function_priority.py`

## Tasks

- [x] Définir une scoring rule : callers, callees, absence de `(F)`, présence `(ND)`, module prioritaire.
- [x] Consommer le mapping Ghidra/repo généré par RE-002.
- [x] Classer les fonctions en lots actionnables.
- [x] Pour chaque lot, documenter les fichiers source à toucher et les preuves Ghidra à regarder.
- [x] Identifier les fonctions à pré-trier avant travail lorsque le mapping Ghidra est absent.

## Result

Backlog générée par:

```bash
python3 scripts/reverse/function_priority.py
```

Résultat actuel:

- `348` candidats priorisés dans `docs/reverse/generated/function-priority.csv`.
- `35` candidats `P0`, dont fonctions runtime et `(ND)`.
- `103` candidats `P1` mappés avec score élevé.
- `210` candidats `P2` à pré-trier ou à traiter après les lots prioritaires.
- `23` fonctions `(ND)` explicitement mises en évidence.

## Acceptance criteria

- [x] Une liste priorisée existe avec justification.
- [x] Chaque entrée pointe vers un fichier source repo et une adresse Ghidra quand disponible.
- [x] Les fonctions `(ND)` sont mises en évidence.
- [x] Les lots sont assez petits pour être pris un par un.
