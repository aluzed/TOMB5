# RE-014 — Auditer les flags item de SaveLevelData

Status: Done
Owner: Hermes
Priority: P0
Type: Reverse audit

## Goal

Auditer les groupes `item` identifiés par RE-013 contre le modèle source actuel de sérialisation `SaveLevelData`: `save_position`, `save_anim`, `save_hitpoints`, `save_flags` et `FullSave`, sans committer de dump original ni d'instructions.

## Context

RE-013 a réduit les `81` appels originaux `WriteSG` à `12` groupes de triage. Les groupes `4` à `12` sont majoritairement des variantes de sérialisation `item`. RE-014 vérifie si les nombres d'appels de ces groupes sont représentables par les combinaisons de writes actuellement présentes dans le source.

## Scope

- Utiliser la carte versionable RE-013: `docs/reverse/generated/saveleveldata-write-call-map.csv`.
- Lire le source `GAME/SAVEGAME.C` pour modéliser les combinaisons de writes du bloc `item`.
- Ne pas lire ni versionner les lignes d'instructions originales.
- Identifier les groupes originaux non représentables par le modèle source actuel.
- Identifier les gaps source évidents sans corriger le code dans cette story.
- Ne pas ajouter `(F)`, `(D)` ou `(**)`.

## Progress

- [x] Ajouter des tests RED pour imposer une matrice item versionable.
- [x] Implémenter `scripts/reverse/saveleveldata_item_flag_audit.py`.
- [x] Générer `docs/reverse/generated/saveleveldata-item-flag-audit.csv`.
- [x] Générer `docs/reverse/functions/saveleveldata-item-flag-audit.md`.
- [x] Mettre à jour l'index des stories et la doc SaveLevelData.
- [x] Valider les tests Python reverse.
- [x] Valider le build `TombRaiderChronicles_PSXPC_N`.
- [x] Contrôler les fichiers staged contre assets/dumps originaux.

## Result

Fichiers ajoutés:

- `scripts/reverse/saveleveldata_item_flag_audit.py`
- `tests/reverse/test_saveleveldata_item_flag_audit.py`
- `docs/reverse/generated/saveleveldata-item-flag-audit.csv`
- `docs/reverse/functions/saveleveldata-item-flag-audit.md`

Fichiers modifiés:

- `docs/stories/README.md`
- `docs/reverse/functions/savegame-level-data.md`

Métriques produites:

- groupes item candidats: `9`
- appels originaux `WriteSG` dans ces groupes: `64`
- counts représentables par le modèle source actuel: `0, 1, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15`
- active control word écrit: `no`
- sites `save_flags` écrits: `0`
- groupes originaux non représentables: `4, 6`
- statut: `source-gaps-found`

## Findings

Le source actuel assemble `word = 0x8000` dans la branche active/full-save, mais ne sérialise pas ce mot de contrôle avant les champs optionnels. Le bloc `if (obj->save_flags)` est également un corps TODO/comment-only sans `Write(...)`.

Conséquences:

- Le groupe original `4` avec `17` appels dépasse le maximum représentable actuel (`15`).
- Le groupe original `6` avec `3` appels tombe dans un trou du modèle de combinaisons source.
- Les groupes représentables par count restent non prouvés: il faut encore vérifier les conditions de branche et les flags objet.

## Commands

```bash
python3 -m pytest tests/reverse/test_saveleveldata_item_flag_audit.py -q
python3 scripts/reverse/saveleveldata_item_flag_audit.py
python3 -m py_compile scripts/reverse/saveleveldata_call_map.py scripts/reverse/saveleveldata_item_flag_audit.py scripts/reverse/saveleveldata_original_audit.py
python3 -m pytest tests/reverse -q
cmake --build BUILD/re005-psxpcn-disc --target TombRaiderChronicles_PSXPC_N -j2
```

## Acceptance criteria

- [x] La matrice versionnée ne contient pas d'instructions originales.
- [x] La matrice versionnée ne contient pas de mots machine originaux.
- [x] Les groupes item `4` à `12` sont couverts.
- [x] Les groupes non représentables sont explicitement listés.
- [x] Les gaps source sont documentés sans patch spéculatif.
- [x] Aucun marqueur `(F)`, `(D)` ou `(**)` n'est ajouté.

## Verdict

`SaveLevelData` ne doit toujours pas recevoir `(F)`, `(D)` ou `(**)`. RE-014 a trouvé des gaps source-level concrets qu'il faut résoudre ou expliquer contre l'original avant toute revendication de complétude.

## Next step

RE-015: reconstruire et tester la sérialisation active item manquante (`Write(&word, 2)` et/ou `save_flags`) à partir d'une preuve de contrôle-flow plus fine, puis régénérer RE-014 pour vérifier que les groupes `4` et `6` sont expliqués ou que l'hypothèse est rejetée.
