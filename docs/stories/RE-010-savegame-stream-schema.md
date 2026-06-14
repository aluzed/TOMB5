# RE-010 — Préparer le schéma de reconstruction SaveLevelData / RestoreLevelData

Status: Done
Owner: Hermes
Priority: P0
Type: Reverse tooling

## Goal

Transformer l'audit RE-009 en artefacts de reconstruction actionnables pour le flux `SaveLevelData` / `RestoreLevelData`, sans modifier encore le code runtime ni versionner de bytes/instructions originaux.

## Context

RE-009 a confirmé que les fonctions originales sont dumpables et comparables localement, mais que le code PSX source reste non implémenté. Avant d'écrire la reconstruction C, il faut un schéma versionnable du stream savegame existant et une validation build/test reproductible.

## Scope

- Générer un schéma source-level ordonné des appels `Write(expr, size)` de la branche `PC_VERSION` de `SaveLevelData`.
- Utiliser ce schéma comme hypothèse de départ pour reconstruire la branche PSX et l'inverse `RestoreLevelData`.
- Ajouter une couverture test minimale pour éviter de casser le parser de schéma.
- Documenter les limites: ce schéma n'est pas une preuve `(F)`, `(D)` ou `(**)`.

## Progress

- [x] Ajouter un test qui échoue tant que le parser de schéma n'existe pas.
- [x] Implémenter `scripts/reverse/savegame_schema.py`.
- [x] Générer `docs/reverse/generated/savegame-level-data-schema.csv`.
- [x] Générer `docs/reverse/generated/savegame-level-data-schema.md`.
- [x] Valider le build `TombRaiderChronicles_PSXPC_N` existant.
- [x] Exécuter les tests Python du parser.
- [x] Confirmer que les dumps originaux restent ignorés et non staged.

## Result

Nouveaux fichiers:

- `scripts/reverse/savegame_schema.py`
- `tests/reverse/test_savegame_schema.py`
- `docs/reverse/generated/savegame-level-data-schema.csv`
- `docs/reverse/generated/savegame-level-data-schema.md`

Commandes validées:

```bash
python3 -m pytest tests/reverse/test_savegame_schema.py -q
python3 scripts/reverse/savegame_schema.py
python3 -m py_compile scripts/reverse/savegame_schema.py
cmake --build BUILD/re005-psxpcn-disc --target TombRaiderChronicles_PSXPC_N -j2
```

Résultats:

- Tests parser: `2 passed`.
- Schéma généré: `32` sites `Write(...)` source-level.
- Build PSXPC_N existant: OK.

## Acceptance criteria

- [x] Le schéma de stream est régénérable par script.
- [x] Les artefacts générés ne contiennent pas d'instructions/bytes originaux.
- [x] Le parser a une couverture test minimale.
- [x] Les limites de preuve sont documentées.
- [x] La prochaine étape d'implémentation C est claire.

## Next step

Créer `RE-011 — Implémenter la branche PSX SaveLevelData à partir du schéma`, avec tests/build par petites étapes. `RestoreLevelData` devrait rester séparé ou suivre seulement après validation du stream écrit, car l'inversion du format peut masquer des erreurs d'ordre ou de taille.
