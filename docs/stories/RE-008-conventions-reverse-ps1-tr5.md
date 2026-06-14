# RE-008 — Documenter conventions de reverse PS1/TR5

Status: Todo
Owner: Unassigned
Priority: P2
Type: Documentation

## Goal

Centraliser les conventions utiles pour reverse TR5 PS1 : adresses, structures, bit-fields, overlays, modules, nommage et pièges Ghidra.

## Context

`TIPS.md` contient déjà des notes importantes sur les bit-fields. `MODULE.md` décrit des formats d'overlay/binaires. Ces informations doivent être reliées au workflow Ghidra pour éviter les erreurs répétées.

## Proposed files

- Create: `docs/reverse/conventions.md`
- Create: `docs/reverse/psx-exe-layout.md`
- Link: `TIPS.md`
- Link: `MODULE.md`

## Tasks

- [ ] Documenter le layout `PS-X EXE` utilisé ici : header `0x800`, text base, entrypoint, stack.
- [ ] Documenter les conventions d'adresses repo : beta vs final PSX dans les commentaires.
- [ ] Reprendre les pièges bit-fields de `TIPS.md` avec exemples Ghidra/MIPS.
- [ ] Documenter les overlays/modules à partir de `MODULE.md`.
- [ ] Définir une convention de nommage pour fonctions Ghidra renommées.
- [ ] Définir une checklist avant de marquer une fonction `(F)`, `(D)` ou `(**)`.

## Acceptance criteria

- [ ] Un nouveau contributeur peut ouvrir Ghidra et comprendre les bases sans relire toute la conversation.
- [ ] Les pièges PS1/Ghidra sont explicitement listés.
- [ ] Les statuts de fonction sont définis et cohérents avec `CONTRIBUTING.md`.
- [ ] La doc pointe vers les fichiers sources existants pertinents.
