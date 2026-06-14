# RE-013 — Mapper les groupes d'appels WriteSG de SaveLevelData

Status: Done
Owner: Hermes
Priority: P0
Type: Reverse audit

## Goal

Produire une carte versionable qui rapproche les groupes d'appels originaux `WriteSG` de `SaveLevelData` des sites source `Write(...)` et de leurs contextes boucle/condition, sans committer d'instructions ni de mots machine originaux.

## Context

RE-012 a établi que le dump original contient `81` appels à `WriteSG`, alors que le source actuel expose `32` sites statiques `Write(...)`. L'écart est attendu parce que le source contient des boucles et des branches runtime. RE-013 transforme ce constat en carte de triage pour guider l'audit manuel de contrôle de flux.

## Scope

- Lire le dump original ignoré `build/reverse/re007/original/SaveLevelData_80053f10.csv`.
- Grouper les appels originaux à `WriteSG` par proximité d'indices d'instructions.
- Écrire uniquement des coordonnées/métadonnées versionables: nombres, indices, adresses, spans source candidats.
- Générer un CSV et un rapport Markdown versionnés.
- Ne pas committer les lignes d'instruction, `word_le_hex`, payload offsets ou bytes originaux.
- Ne pas ajouter `(F)`, `(D)` ou `(**)`.

## Progress

- [x] Ajouter des tests RED pour le groupement d'appels sans fuite de payload original.
- [x] Implémenter `scripts/reverse/saveleveldata_call_map.py`.
- [x] Générer `docs/reverse/generated/saveleveldata-write-call-map.csv`.
- [x] Générer `docs/reverse/functions/saveleveldata-write-call-map.md`.
- [x] Mettre à jour les docs de suivi.
- [x] Valider les tests Python reverse.
- [x] Valider le build `TombRaiderChronicles_PSXPC_N`.
- [x] Contrôler les fichiers staged contre assets/dumps originaux.

## Result

Fichiers ajoutés:

- `scripts/reverse/saveleveldata_call_map.py`
- `tests/reverse/test_saveleveldata_call_map.py`
- `docs/reverse/generated/saveleveldata-write-call-map.csv`
- `docs/reverse/functions/saveleveldata-write-call-map.md`

Fichiers modifiés:

- `docs/stories/README.md`
- `docs/reverse/functions/savegame-level-data.md`

Métriques produites:

- appels originaux `WriteSG`: `81`
- groupes originaux d'appels: `12`
- sites source statiques `Write(...)`: `32`
- statut: `candidate-map-needs-manual-audit`

## Commands

```bash
python3 -m pytest tests/reverse/test_saveleveldata_call_map.py -q
python3 scripts/reverse/saveleveldata_call_map.py
python3 -m py_compile scripts/reverse/saveleveldata_call_map.py scripts/reverse/saveleveldata_original_audit.py
python3 -m pytest tests/reverse -q
cmake --build BUILD/re005-psxpcn-disc --target TombRaiderChronicles_PSXPC_N -j2
```

## Acceptance criteria

- [x] Le CSV versionné ne contient pas `instruction` ni `word_le_hex`.
- [x] Le Markdown versionné ne contient pas les instructions originales.
- [x] Les `81` appels originaux sont représentés dans des groupes.
- [x] Chaque groupe reçoit un span source candidat ou une note explicite.
- [x] Le rapport indique que la carte est un artefact de triage, pas une preuve d'équivalence.
- [x] Aucun marqueur `(F)`, `(D)` ou `(**)` n'est ajouté.

## Verdict

La carte RE-013 réduit l'audit manuel à `12` groupes d'appels originaux. Les groupes 4 à 12 restent majoritairement liés aux variantes de sérialisation `item` et nécessitent une analyse manuelle des branches MIPS / flags objet avant toute revendication de complétude.

## Next step

RE-014: auditer manuellement les groupes `item` de `SaveLevelData` contre les flags `save_position`, `save_anim`, `save_hitpoints`, `save_flags` et `FullSave`, puis remplacer les candidats faibles par une table de correspondance contrôlée.
