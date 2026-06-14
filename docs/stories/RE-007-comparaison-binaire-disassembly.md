# RE-007 — Mettre en place comparaison binaire/désassemblage

Status: Todo
Owner: Unassigned
Priority: P1
Type: Verification

## Goal

Mettre en place une méthode fiable pour comparer le code recompilé/décompilé aux instructions MIPS originales et valider les marqueurs `(**)`, `(F)` et `(D)`.

## Context

`CONTRIBUTING.md` indique que `(**)` signifie code compilé identique à l'original, `(F)` signifie fully decompiled, `(D)` signifie debugged/functionally same, `(ND)` signifie non debugged. Le repo insiste sur la comparaison au MIPS disassemblé original.

## Proposed files

- Create: `docs/reverse/binary-comparison.md`
- Create: `scripts/reverse/disasm_extract.py`
- Create: `scripts/reverse/compare_function.py`

## Tasks

- [ ] Définir le format de dump de désassemblage Ghidra par fonction.
- [ ] Exporter les bytes/instructions originales par adresse.
- [ ] Identifier comment produire le binaire recompilé comparable.
- [ ] Créer un outil de diff par fonction ou plage d'adresse.
- [ ] Documenter les différences acceptables : registres temporaires, scheduling, padding, relocation.
- [ ] Lier les résultats au rapport de progression.

## Acceptance criteria

- [ ] Une fonction peut être sélectionnée par nom/adresse et dumpée depuis l'original.
- [ ] Le workflow explique comment comparer au code recompilé.
- [ ] Les résultats peuvent justifier un passage à `(**)` ou `(D)`.
- [ ] Les limitations sont explicitement documentées.
