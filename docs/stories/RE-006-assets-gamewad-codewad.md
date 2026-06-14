# RE-006 — Extraire et documenter GAMEWAD/CODEWAD/assets

Status: Todo
Owner: Unassigned
Priority: P1
Type: Assets

## Goal

Extraire, inventorier et documenter les assets disque nécessaires au runtime et à la reverse engineering : `GAMEWAD.OBJ`, `CODE.WAD` si disponible, niveaux, FMV, XA et scripts.

## Context

Le disque contient `GAMEWAD.OBJ`. Le repo fournit des outils `GAMEWAD_Unpack`, `GAMEWAD_Pack`, `CODEWAD_Unpack`, `CODEWAD_Pack` et un script `scripts/gamewad.py`.

## Proposed files

- Create: `docs/reverse/assets-inventory.md`
- Create: `docs/reverse/generated/disc-files.txt`
- Create: `docs/reverse/generated/gamewad-files.txt`

## Tasks

- [ ] Lister le contenu racine du disque avec tailles et dates.
- [ ] Compiler ou utiliser l'outil d'extraction `GAMEWAD_Unpack`.
- [ ] Extraire `GAMEWAD.OBJ` dans une zone non versionnée.
- [ ] Comparer la liste extraite à `scripts/gamewad.py`.
- [ ] Documenter quels fichiers sont nécessaires pour `DISC_VERSION=0` versus `DISC_VERSION=1`.
- [ ] Ne pas committer les assets lourds, seulement les inventaires.

## Acceptance criteria

- [ ] Inventaire disque disponible.
- [ ] Inventaire `GAMEWAD.OBJ` disponible ou blocage outil documenté.
- [ ] Les chemins runtime attendus sont documentés.
- [ ] Aucun asset copyrighted lourd n'est ajouté au repo par erreur.
