# RE-011 — Implémenter la branche PSX SaveLevelData depuis le schéma

Status: Done
Owner: Hermes
Priority: P0
Type: Reverse implementation

## Goal

Retirer le fallback PSX `UNIMPLEMENTED()` de `SaveLevelData` et rendre le flux source-level `Write(...)` disponible pour le build PSX/PSXPC_N, en s'appuyant sur le schéma RE-010.

## Context

RE-009 a confirmé que `SaveLevelData` est une grande routine originale dominée par `WriteSG`. RE-010 a généré un schéma de `32` sites `Write(...)` depuis l'implémentation existante. Avant cette story, cette implémentation était confinée à `#if PC_VERSION`; le chemin PSX compilait uniquement le fallback `UNIMPLEMENTED()`.

## Scope

- Ne pas modifier `RestoreLevelData`.
- Ne pas ajouter de marqueur `(F)`, `(D)` ou `(**)`.
- Ne pas versionner de dumps originaux.
- Garder la validation limitée à: source statique, schéma généré, build PSXPC_N.

## Progress

- [x] Ajouter des tests statiques qui échouent tant que `SaveLevelData` reste caché derrière `#if PC_VERSION` ou contient le fallback PSX `UNIMPLEMENTED()`.
- [x] Retirer le guard `#if PC_VERSION` interne à `SaveLevelData`.
- [x] Retirer le fallback `// todo check for psx` / `UNIMPLEMENTED()`.
- [x] Adapter `scripts/reverse/savegame_schema.py` pour parser l'implémentation courante plutôt qu'une branche PC historique.
- [x] Régénérer le schéma `docs/reverse/generated/savegame-level-data-schema.*`.
- [x] Valider les tests Python.
- [x] Valider le build `TombRaiderChronicles_PSXPC_N`.
- [x] Contrôler que les artefacts originaux ignorés ne sont pas staged.

## Result

Fichiers modifiés/ajoutés:

- Modified: `GAME/SAVEGAME.C`
- Modified: `scripts/reverse/savegame_schema.py`
- Modified: `docs/reverse/generated/savegame-level-data-schema.csv`
- Modified: `docs/reverse/generated/savegame-level-data-schema.md`
- Added: `tests/reverse/test_savegame_source.py`

Commandes validées:

```bash
python3 -m pytest tests/reverse/test_savegame_source.py tests/reverse/test_savegame_schema.py -q
python3 scripts/reverse/savegame_schema.py
python3 -m py_compile scripts/reverse/savegame_schema.py
cmake --build BUILD/re005-psxpcn-disc --target TombRaiderChronicles_PSXPC_N -j2
```

Résultats:

- Tests Python: `4 passed`.
- Schéma régénéré: `32` sites `Write(...)`.
- Build PSXPC_N: OK.

Build note:

- Le build émet toujours le warning existant dans `sgSaveGame()` autour de `memcpy(&MGSaveGamePtr, &savegame, sizeof(struct savegame_info));`; RE-011 ne le modifie pas.

## Acceptance criteria

- [x] `SaveLevelData` ne contient plus `UNIMPLEMENTED()`.
- [x] `SaveLevelData` n'est plus limité à `#if PC_VERSION`.
- [x] Le schéma de stream reste générable et testé.
- [x] Le build PSXPC_N passe.
- [x] Aucun marqueur de complétude n'est ajouté sans preuve plus forte.

## Verification limits

Cette story prouve que la branche source est maintenant compilable pour PSXPC_N et structurée selon le schéma connu. Elle ne prouve pas encore:

- équivalence binaire `(**)`;
- équivalence fonctionnelle debugguée `(D)`;
- complétude reverse suffisante pour `(F)`.

## Next step

Créer `RE-012 — Auditer SaveLevelData contre le dump original`, pour comparer la structure source avec le dump original local et identifier les écarts restants avant d'envisager un marqueur `(F)`.
