# RE-000 — Baseline disque, Ghidra et repo

Status: Done
Owner: Unassigned
Priority: P0
Type: Foundation

## Goal

Établir que l'image disque disponible correspond bien à la version de référence du repo et qu'elle peut servir de base à la reverse engineering.

## Evidence

- Repo : `/var/www/projects/TOMB5`
- Disque préparé : `TOMB5.BIN` + `TOMB5.CUE`
- `SLUS_013.11` extrait depuis l'image Archive.org.
- MD5 `SLUS_013.11` vérifié : `4ef523e708d7a7d6571f39c6e47784f9`
- MD5 attendu par `CONTRIBUTING.md` : `4EF523E708D7A7D6571F39C6E47784F9`
- `SYSTEM.CNF` pointe vers `BOOT=cdrom:\SLUS_013.11;1`
- Ghidra headless analyse correctement le payload brut `SLUS_013.11.payload.bin` en `MIPS:LE:32` à `0x80010000`.

## Progress

- [x] Télécharger l'image BIN/CUE USA.
- [x] Extraire `SLUS_013.11`.
- [x] Vérifier le MD5 de l'exécutable principal.
- [x] Préparer `TOMB5.BIN` et `TOMB5.CUE` dans le repo.
- [x] Vérifier l'import Ghidra du payload brut.

## Acceptance criteria

- [x] La version disque est prouvée compatible avec le repo.
- [x] Les fichiers attendus par le repo existent à la racine.
- [x] Les contraintes Ghidra PS-X EXE sont documentées.
