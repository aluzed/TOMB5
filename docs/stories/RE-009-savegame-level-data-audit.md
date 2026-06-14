# RE-009 — Auditer SaveLevelData / RestoreLevelData

Status: Done
Owner: Hermes
Priority: P0
Type: Reverse verification

## Goal

Appliquer le workflow RE-007 aux fonctions P0 `SaveLevelData` et `RestoreLevelData` afin de produire un verdict actionnable sans versionner les instructions/bytes originaux.

## Context

`docs/reverse/backlog.md` classe `RestoreLevelData` et `SaveLevelData` en tête du lot P0 runtime/savegame. Les deux fonctions sont mappées dans Ghidra et disposent d'une taille de corps, ce qui permet de générer des dumps originaux locaux ignorés par git.

## Scope

- `RestoreLevelData` — `GAME/SAVEGAME.C:82`, `0x80054f6c`, `FUN_80054f6c`, body size `4080`.
- `SaveLevelData` — `GAME/SAVEGAME.C:100`, `0x80053f10`, `FUN_80053f10`, body size `4188`.

## Progress

- [x] Générer les dumps originaux sous `build/reverse/re007/original/`.
- [x] Vérifier les dumps par self-comparison avec `compare_function.py`.
- [x] Auditer l'état source actuel dans `GAME/SAVEGAME.C`.
- [x] Relever les appels/couverture structurelle sans committer de bytes/instructions originaux.
- [x] Écrire un rapport versionnable avec verdict par fonction.
- [x] Contrôler que les artefacts ignorés ne sont pas staged.

## Result

Rapport versionné: `docs/reverse/functions/savegame-level-data.md`.

Commandes exécutées:

```bash
python3 scripts/reverse/disasm_extract.py RestoreLevelData
python3 scripts/reverse/disasm_extract.py SaveLevelData
python3 scripts/reverse/compare_function.py \
  build/reverse/re007/original/SaveLevelData_80053f10.csv \
  build/reverse/re007/original/SaveLevelData_80053f10.csv \
  --name SaveLevelData_selftest
python3 scripts/reverse/compare_function.py \
  build/reverse/re007/original/RestoreLevelData_80054f6c.csv \
  build/reverse/re007/original/RestoreLevelData_80054f6c.csv \
  --name RestoreLevelData_selftest
```

Validation locale:

- `RestoreLevelData`: dump original complet `4080` bytes, `1020` instructions, self-test `exact_match=yes`.
- `SaveLevelData`: dump original complet `4188` bytes, `1047` instructions, self-test `exact_match=yes`.
- Artefacts contenant bytes/instructions originaux confinés à `build/reverse/re007/`, ignoré par git.

## Acceptance criteria

- [x] Les deux fonctions P0 sont dumpées depuis l'original.
- [x] Le rapport ne contient pas de bytes/instructions originales versionnées.
- [x] Le verdict explique pourquoi aucun marqueur `(**)`, `(F)` ou `(D)` ne doit encore être ajouté.
- [x] La prochaine étape d'implémentation est clairement identifiée.
