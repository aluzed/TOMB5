# RE-008 — Documenter conventions de reverse PS1/TR5

Status: Done
Owner: Hermes
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

- [x] Documenter le layout `PS-X EXE` utilisé ici : header `0x800`, text base, entrypoint, stack.
- [x] Documenter les conventions d'adresses repo : beta vs final PSX dans les commentaires.
- [x] Reprendre les pièges bit-fields de `TIPS.md` avec exemples Ghidra/MIPS.
- [x] Documenter les overlays/modules à partir de `MODULE.md`.
- [x] Définir une convention de nommage pour fonctions Ghidra renommées.
- [x] Définir une checklist avant de marquer une fonction `(F)`, `(D)` ou `(**)`.

## Result

Deux documents centraux ont été ajoutés:

- `docs/reverse/conventions.md`: conventions de commentaires, marqueurs `(F)`, `(D)`, `(**)`, `(ND)`, nommage Ghidra, bit-fields, pièges 32-bit/64-bit et checklist de statut.
- `docs/reverse/psx-exe-layout.md`: header `PS-X EXE`, valeurs vérifiées de `SLUS_013.11`, conversions adresses/offsets, import Ghidra, overlays `.MOD`/`.BIN` et lien avec `RELOC`.

## Acceptance criteria

- [x] Un nouveau contributeur peut ouvrir Ghidra et comprendre les bases sans relire toute la conversation.
- [x] Les pièges PS1/Ghidra sont explicitement listés.
- [x] Les statuts de fonction sont définis et cohérents avec `CONTRIBUTING.md`.
- [x] La doc pointe vers les fichiers sources existants pertinents.
