# RE-002 — Exporter les fonctions Ghidra et les rapprocher du repo

Status: Done
Owner: Hermes
Priority: P0
Type: Analysis

## Goal

Exporter depuis Ghidra la liste des fonctions, adresses, tailles, références et noms proposés, puis les mapper aux fonctions déjà présentes dans le repo via les commentaires d'adresses.

## Context

Le repo utilise des commentaires de fonction contenant souvent des adresses PSX beta/final et des marqueurs `(F)`, `(D)`, `(ND)`. Ghidra fournit une vue binaire indépendante permettant d'identifier les trous, doublons et fonctions mal alignées.

Convention observée pour les commentaires du type `//61EE8(<), 625CC(<) (F) (D)` :

- première adresse : beta/source historique ;
- deuxième adresse : final PSX ;
- normalisation mapping : `0x80xxxxxx`.

## Files

- Created: `scripts/reverse/ExportGhidraFunctions.java`
- Created: `scripts/reverse/map_ghidra_to_repo.py`
- Generated snapshot: `docs/reverse/generated/ghidra-functions.csv`
- Generated snapshot: `docs/reverse/generated/repo-functions.csv`
- Generated snapshot: `docs/reverse/generated/repo-function-map.csv`
- Generated snapshot: `docs/reverse/generated/mapped-functions.md`
- Generated snapshot: `docs/reverse/generated/repo-only-functions.md`
- Generated snapshot: `docs/reverse/generated/unmapped-ghidra-functions.md`
- Generated snapshot: `docs/reverse/generated/function-map-summary.json`

Runtime artifacts are also written under `build/reverse/generated/`.

## Command

From repo root:

```bash
python3 scripts/reverse/map_ghidra_to_repo.py
```

Useful faster rerun when payload already exists:

```bash
python3 scripts/reverse/map_ghidra_to_repo.py --skip-prepare
```

The command:

1. prepares/reuses `SLUS_013.11.payload.bin`;
2. imports the raw PSX payload into Ghidra headless as `MIPS:LE:32:default` at `0x80010000`;
3. runs `ExportGhidraFunctions.java` as a post-script;
4. exports Ghidra functions with entry, body size, called functions and callers;
5. parses repo function comments;
6. maps Ghidra → repo by exact final PSX address;
7. mirrors reports into `docs/reverse/generated/`.

## Tasks

- [x] Écrire un post-script Ghidra qui exporte : name, entry, body size, called functions, callers.
- [x] Parser les commentaires du repo pour extraire : fichier, fonction, adresse final PSX, marqueurs.
- [x] Normaliser les adresses en `0x80xxxxxx`.
- [x] Mapper Ghidra → repo par adresse exacte.
- [x] Générer la liste des fonctions Ghidra sans équivalent repo.
- [x] Générer la liste des fonctions repo sans équivalent Ghidra.
- [x] Identifier les fonctions nommées automatiquement par Ghidra qui devraient recevoir un nom repo.

## Verification

Last verified command:

```bash
/usr/bin/time -f 'elapsed=%es' python3 scripts/reverse/map_ghidra_to_repo.py --skip-prepare
```

Result:

- elapsed: `20.63s`
- Ghidra functions: `1440`
- repo functions parsed: `1250`
- mapped functions: `866`
- repo-only functions: `384`
- Ghidra-only functions: `723`
- rename candidates: `866`

Syntax check:

```bash
python3 -m py_compile scripts/reverse/prepare_ghidra_psx.py scripts/reverse/map_ghidra_to_repo.py
```

## Acceptance criteria

- [x] Un CSV Ghidra est généré automatiquement.
- [x] Un CSV repo est généré automatiquement.
- [x] Au moins trois rapports existent : mapped, Ghidra-only, repo-only.
- [x] Les rapports permettent de choisir la prochaine fonction à reverse sans ouvrir Ghidra manuellement.
