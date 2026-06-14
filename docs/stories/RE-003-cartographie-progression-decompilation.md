# RE-003 — Cartographier la progression de décompilation par module

Status: Done
Owner: Hermes
Priority: P1
Type: Tracking

## Goal

Produire un tableau de bord local de progression par dossier, fichier et fonction à partir des marqueurs du repo et du mapping Ghidra.

## Status model

Le rapport définit une hiérarchie de statuts de fonction :

- `unknown` : pas de marqueur final/débug et pas de signal utile de nom/mapping.
- `named` : mappée/nommée, mais sans marqueur final/décompilé/débug.
- `decompiled` : fonction nommée côté repo sans marqueur final/debug.
- `final` : contient `(F)`.
- `debugged` : contient `(D)`, plus fort que `(F)` pour le tracking.
- `binary_matched` : contient `(**)`.

`(ND)` est compté séparément comme flag transversal.

## Files

- Created: `scripts/reverse/progress_report.py`
- Created: `docs/reverse/progress.md`
- Created: `docs/reverse/generated/progress.json`

Input consumed:

- `docs/reverse/generated/repo-function-map.csv`

## Command

From repo root:

```bash
python3 scripts/reverse/progress_report.py
```

The command reads the Ghidra ↔ repo mapping, computes overall/module/file metrics, identifies files with most non-final functions, and produces a `next candidates` list based on mapped non-final functions, body size, callers, and callees.

## Current verified snapshot

- source rows: `1250`
- modules: `5`
- files: `138`
- mapped: `866` (`69.28%`)
- final/debug/binary-matched: `925` (`74.0%`)
- `(ND)` flags: `23`

Overall statuses:

- `final`: `842`
- `debugged`: `83`
- `binary_matched`: `0`
- `decompiled`: `324`
- `named`: `0`
- `unknown`: `1`

Module snapshot:

- `GAME`: total `811`, mapped `620`, final/debug/binary-matched `672` (`82.86%`)
- `SPEC_PSXPC_N`: total `212`, mapped `102`, final/debug/binary-matched `119` (`56.13%`)
- `SPEC_PSXPC`: total `144`, mapped `88`, final/debug/binary-matched `66` (`45.83%`)
- `SPEC_PSX`: total `79`, mapped `55`, final/debug/binary-matched `67` (`84.81%`)
- `SPEC_PC_N`: total `4`, mapped `1`, final/debug/binary-matched `1` (`25.0%`)

Top files with non-final work:

- `SPEC_PSXPC_N/ANIMITEM.C`: `24` non-final / `25`
- `SPEC_PSXPC_N/MATHS.C`: `19` non-final / `40`
- `SPEC_PSXPC/MATHS.C`: `18` non-final / `27`
- `GAME/SWITCH.C`: `15` non-final / `21`
- `GAME/TRAPS.C`: `15` non-final / `30`

## Verification

Last verified command:

```bash
/usr/bin/time -f 'elapsed=%es' python3 scripts/reverse/progress_report.py
```

Result:

- elapsed: `0.04s`
- report: `docs/reverse/progress.md`
- JSON: `docs/reverse/generated/progress.json`

Syntax check:

```bash
python3 -m py_compile scripts/reverse/prepare_ghidra_psx.py scripts/reverse/map_ghidra_to_repo.py scripts/reverse/progress_report.py
```

## Tasks

- [x] Définir les statuts de fonction : unknown, named, decompiled, final, debugged, binary-matched.
- [x] Parser les marqueurs `(F)`, `(D)`, `(ND)` et `(**)`.
- [x] Calculer les pourcentages par dossier et fichier.
- [x] Lister les fichiers avec le plus de fonctions non finalisées.
- [x] Produire un rapport Markdown lisible sans table Telegram-incompatible si nécessaire.
- [x] Ajouter une section "next candidates" basée sur impact et dépendances.

## Acceptance criteria

- [x] `python3 scripts/reverse/progress_report.py` génère le rapport.
- [x] Le rapport contient les compteurs par module.
- [x] Le rapport distingue clairement `F`, `D`, `ND` et non marqué.
- [x] Le rapport est assez précis pour suivre la progression à chaque PR/commit.
