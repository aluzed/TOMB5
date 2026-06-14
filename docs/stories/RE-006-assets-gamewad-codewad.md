# RE-006 — Extraire et documenter GAMEWAD/CODEWAD/assets

Status: Done
Owner: Hermes
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
- Create: `docs/reverse/generated/assets-summary.json`
- Create: `scripts/reverse/assets_inventory.py`

## Tasks

- [x] Lister le contenu racine du disque avec tailles et dates.
- [x] Compiler ou utiliser l'outil d'extraction `GAMEWAD_Unpack`.
- [x] Extraire `GAMEWAD.OBJ` dans une zone non versionnée.
- [x] Comparer la liste extraite à `scripts/gamewad.py`.
- [x] Documenter quels fichiers sont nécessaires pour `DISC_VERSION=0` versus `DISC_VERSION=1`.
- [x] Ne pas committer les assets lourds, seulement les inventaires.

## Acceptance criteria

- [x] Inventaire disque disponible.
- [x] Inventaire `GAMEWAD.OBJ` disponible ou blocage outil documenté.
- [x] Les chemins runtime attendus sont documentés.
- [x] Aucun asset copyrighted lourd n'est ajouté au repo par erreur.

## Result

- Inventaire disque: `docs/reverse/generated/disc-files.txt` (`30` fichiers listés: `GAMEWAD.OBJ`, `SLUS_013.11`, metadata, `8` FMV, `17` XA).
- Inventaire GAMEWAD: `docs/reverse/generated/gamewad-files.txt` (`51` entrées, `30` non vides, `21` réservées vides).
- Synthèse machine-readable: `docs/reverse/generated/assets-summary.json`.
- Documentation: `docs/reverse/assets-inventory.md`.
- Script reproductible: `python3 scripts/reverse/assets_inventory.py`.
- Zone d'extraction non versionnée: `build/reverse/re006/`.
- `CODE.WAD`: pas autonome à la racine du disque; détecté comme segment embarqué dans `15` entrées niveau de `GAMEWAD.OBJ` (`430108` octets par segment détecté).
