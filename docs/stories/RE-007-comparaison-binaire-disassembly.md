# RE-007 — Mettre en place comparaison binaire/désassemblage

Status: Done
Owner: Hermes
Priority: P1
Type: Verification

## Goal

Mettre en place une méthode fiable pour comparer le code recompilé/décompilé aux instructions MIPS originales et valider les marqueurs `(**)`, `(F)` et `(D)`.

## Context

`CONTRIBUTING.md` indique que `(**)` signifie code compilé identique à l'original, `(F)` signifie fully decompiled, `(D)` signifie debugged/functionally same, `(ND)` signifie non debugged. Le repo insiste sur la comparaison au MIPS disassemblé original.

## Proposed files

- Created: `docs/reverse/binary-comparison.md`
- Created: `scripts/reverse/disasm_extract.py`
- Created: `scripts/reverse/compare_function.py`

## Tasks

- [x] Définir le format de dump de désassemblage par fonction.
- [x] Exporter les bytes/instructions originales par adresse sous `build/reverse/re007/` ignoré.
- [x] Identifier comment produire le binaire recompilé comparable.
- [x] Créer un outil de diff par fonction ou plage d'adresse.
- [x] Documenter les différences acceptables : registres temporaires, scheduling, padding, relocation.
- [x] Lier les résultats aux marqueurs `(**)`, `(F)`, `(D)` et `(ND)`.

## Result

Workflow documenté dans `docs/reverse/binary-comparison.md`.

Validation locale effectuée:

```bash
python3 -m py_compile scripts/reverse/disasm_extract.py scripts/reverse/compare_function.py
python3 scripts/reverse/disasm_extract.py SaveLevelData --max-bytes 64
python3 scripts/reverse/compare_function.py \
  build/reverse/re007/original/SaveLevelData_80053f10.csv \
  build/reverse/re007/original/SaveLevelData_80053f10.csv \
  --name SaveLevelData_selftest
```

Le self-test retourne `exact_match=yes`. Les dumps générés restent sous `build/reverse/re007/` et ne sont pas versionnés.

## Acceptance criteria

- [x] Une fonction peut être sélectionnée par nom/adresse et dumpée depuis l'original.
- [x] Le workflow explique comment comparer au code recompilé.
- [x] Les résultats peuvent justifier un passage à `(**)` ou `(D)`.
- [x] Les limitations sont explicitement documentées.
