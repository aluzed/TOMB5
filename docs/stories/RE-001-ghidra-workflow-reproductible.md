# RE-001 — Rendre le workflow Ghidra reproductible

Status: Done
Owner: Unassigned
Priority: P0
Type: Tooling

## Goal

Créer un workflow scriptable qui reconstruit l'environnement Ghidra à partir de `TOMB5.BIN/TOMB5.CUE`, extrait l'exécutable PS1, prépare le payload et lance l'analyse headless.

## Context

Ghidra ne charge pas directement `SLUS_013.11` comme PS-X EXE dans cette installation headless. Le workflow validé est : extraire `SLUS_013.11`, retirer le header `0x800`, importer le payload en `MIPS:LE:32:default` avec base `0x80010000`.

## Proposed files

- Create: `docs/reverse/ghidra-workflow.md`
- Create: `scripts/reverse/prepare_ghidra_psx.py` or `scripts/reverse/prepare_ghidra_psx.sh`
- Create: `scripts/ghidra/ExportFunctions.java` or `scripts/ghidra/ExportFunctions.py`

## Tasks

- [x] Décrire les entrées/sorties du workflow.
- [x] Automatiser l'extraction/listing de l'image disque.
- [x] Lire `SYSTEM.CNF` pour détecter le boot executable.
- [x] Vérifier MD5 de `SLUS_013.11` contre la valeur repo.
- [x] Extraire le payload en supprimant les `2048` octets du header PS-X EXE.
- [x] Lancer `analyzeHeadless` avec `MIPS:LE:32:default` et `-loader-baseAddr 0x80010000`.
- [x] Écrire un log reproductible dans `build/reverse/` ou `docs/reverse/generated/`.

## Implementation notes

- Script: `scripts/reverse/prepare_ghidra_psx.py`
- Documentation: `docs/reverse/ghidra-workflow.md`
- Generated artifacts: `build/reverse/` (ignored by `.gitignore`)
- Verified command: `python3 scripts/reverse/prepare_ghidra_psx.py`
- Last measured runtime: `19.91s` on this machine.
- Verified output summary: `build/reverse/generated/prepare_ghidra_psx_summary.json`

## Acceptance criteria

- [x] Une seule commande reconstruit le projet Ghidra ou l'analyse headless.
- [x] Le script échoue clairement si le MD5 ne correspond pas.
- [x] Le résultat inclut l'adresse d'entrée `0x8007663c`, la base `0x80010000` et la taille texte.
- [x] La doc explique pourquoi l'import direct PS-X EXE ne suffit pas.
