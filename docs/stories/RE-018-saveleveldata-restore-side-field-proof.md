# RE-018 — Vérifier les hypothèses item SaveLevelData côté RestoreLevelData

Status: Done
Owner: Hermes
Priority: P0
Type: Reverse audit

## Goal

Vérifier les hypothèses RE-017 contre le restore-side stream reading avant tout patch serializer: déterminer quels gaps sont supportés par le source restore actuel, absents côté restore, ou nécessitent une preuve originale supplémentaire.

## Context

RE-017 a produit une table source-vs-original des champs/largeurs probables pour les groupes item mismatch `4` à `11`:

- anim states byte-sized côté original metadata vs `2` bytes source actuel
- payloads séparés probables `item_flags/timer/trigger_flags`
- payloads object-specific `4`, `20`, `24`
- layout/order gaps, notamment `room_number`

RE-018 doit confronter ces hypothèses au restore-side, pas patcher `GAME/SAVEGAME.C` directement.

## Scope

- Parser/inspecter le source `RestoreLevelData` / fonctions restore liées dans `GAME/SAVEGAME.C`.
- Produire un audit metadata-only des hypothèses RE-017 avec statut restore-side explicite.
- Ne pas versionner d'instructions originales, mots machine, payload offsets, dumps ou assets.
- Ne pas patcher le serializer tant que les hypothèses ne sont pas confirmées.
- Ne pas ajouter `(F)`, `(D)` ou `(**)`.

## Progress

- [x] Ajouter la story RE-018 avec tracker explicite.
- [x] Ajouter/faire échouer les tests RED pour l'audit restore-side.
- [x] Implémenter le générateur d'audit restore-side.
- [x] Générer CSV/Markdown versionables.
- [x] Mettre à jour l'index stories et la documentation SaveLevelData.
- [x] Valider tests reverse.
- [x] Valider le build `TombRaiderChronicles_PSXPC_N`.
- [x] Contrôler les fichiers staged contre assets/dumps originaux.
- [x] Committer et pousser.

## Result

Fichiers ajoutés:

- `scripts/reverse/saveleveldata_restore_side_audit.py`
- `tests/reverse/test_saveleveldata_restore_side_audit.py`
- `docs/reverse/generated/saveleveldata-restore-side-audit.csv`
- `docs/reverse/functions/saveleveldata-restore-side-audit.md`

Fichiers modifiés:

- `docs/reverse/functions/savegame-level-data.md`
- `docs/stories/README.md`

Métriques produites:

- `RestoreLevelData` source status: `source-unimplemented`
- hypothèses auditées: `57`
- hypothèses prioritaires: `34`
- hypothèses prêtes pour patch: `0`
- status: `restore-side-proof-missing`
- restore-side status counts:
  - `restore-source-absent`: `37`
  - `needs-original-restore-proof`: `14`
  - `restore-layout-unverifiable`: `3`
  - `restore-width-unverifiable`: `3`

## Findings

RE-018 bloque explicitement le patch serializer basé sur RE-017 seul:

- `RestoreLevelData` est actuellement `UNIMPLEMENTED()` côté source, donc aucune séquence de `Read(...)` source ne peut confirmer les hypothèses.
- Les anim states byte-sized du groupe `4` restent `restore-width-unverifiable`: il faut dériver la largeur de lecture originale avant de changer le source.
- Les payloads object-specific `4`, `20`, `24` et les sentinelles/bytes de contrôle restent `needs-original-restore-proof`.
- Les gaps de layout, dont `room_number` ordre/layout, restent `restore-layout-unverifiable`.
- Les champs exact-width côté save restent `restore-source-absent`: une largeur de save plausible ne suffit pas sans inverse restore.

## Commands

```bash
python3 -m pytest tests/reverse/test_saveleveldata_restore_side_audit.py -q
python3 scripts/reverse/saveleveldata_restore_side_audit.py
python3 -m py_compile scripts/reverse/saveleveldata_restore_side_audit.py
python3 -m pytest tests/reverse -q
cmake --build BUILD/re005-psxpcn-disc --target TombRaiderChronicles_PSXPC_N -j2
git diff --cached --name-only | python3 -c 'import sys; bad=[p.strip() for p in sys.stdin if p.strip().startswith(("build/",)) or p.strip().endswith((".BIN", ".CUE", ".OBJ", ".WAD"))]; print("asset guard ok" if not bad else "blocked: "+", ".join(bad)); sys.exit(1 if bad else 0)'
```

Validation:

- `24 passed`
- `Built target TombRaiderChronicles_PSXPC_N`
- Output metadata guard: no `instruction`, `word_le_hex`, `payload_offset`, or raw `jal` token in RE-018 outputs
- Asset/staging guard: `asset guard ok`

## Acceptance criteria

- [x] Les priority findings RE-017 sont couverts côté restore-side.
- [x] Chaque hypothèse est classée avec un statut explicite: source absent, width/layout unverifiable, needs original restore proof.
- [x] Les sorties restent metadata-only et ne contiennent pas `instruction`, `word_le_hex`, `payload_offset` ni instruction originale.
- [x] Le verdict distingue les gaps prêts pour une story de patch de ceux qui nécessitent une preuve originale restore.
- [x] Aucun marqueur `(F)`, `(D)` ou `(**)` n'est ajouté.

## Verdict

RE-018 ne trouve aucune hypothèse prête pour patch: `patch-ready hypotheses = 0`. Le restore-side source est absent/unimplemented, donc RE-017 reste une matrice d'hypothèses et ne justifie aucune correction serializer ni marqueur de complétude.

## Next step

RE-019: extraire ou reconstruire une call-map metadata-only de l'original `RestoreLevelData`, puis comparer les tailles/ordre de lecture restore aux hypothèses RE-017/RE-018 avant toute modification source.
