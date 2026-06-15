# RE-028 — Checklist source-field identity RestoreLevelData group 5

Status: Done
Owner: Hermes
Priority: P0
Type: Reverse source-field identity audit

## Goal

Construire une checklist source-field identity, metadata-only, pour la famille bloquée à plus forte valeur issue de RE-027 : le save group `5` / restore group `6` de `RestoreLevelData`.

## Context

RE-027 a confirmé que les groupes prioritaires `4`, `5`, `8` et `10` restent tous bloqués pour un patch source. Le group `5` concentre un cluster compact autour du packed status word, avec des header predicates visibles dans `GAME/SAVEGAME.C` mais sans payload bodies source-backed pour `item_flags[0..3]`, `timer`, `trigger_flags` ni object-extension. RE-028 formalise donc les preuves minimales requises avant toute reconstruction source.

## Scope

- Consommer uniquement les CSV metadata-only RE-017 et RE-025, plus le texte source `GAME/SAVEGAME.C` pour présence de noms/champs.
- Cibler le save group `5` et restore group `6`.
- Publier une ligne de checklist par payload family : `packed-status-flags`, `item_flags[0..3]`, `timer`, `trigger_flags`, `object-extension`.
- Indiquer current source identity state, restore identity state, required evidence, blocker, checklist status, safe next action et next ticket.
- Garder `patch-ready checklist rows = 0` tant que les source write bodies et restore assignments ne sont pas prouvés.
- Ne pas lire ni publier de dump brut, mot machine, coordonnée de payload, cible brute de branche/call ou adresse originale.
- Ne pas modifier `GAME/SAVEGAME.C`.
- Ne pas ajouter `(F)`, `(D)` ou `(**)`.

## Progress

- [x] Ajouter/faire échouer les tests RED du générateur RE-028.
- [x] Implémenter le générateur metadata-only RE-028.
- [x] Générer CSV/Markdown versionables.
- [x] Mettre à jour l'index stories et la documentation Save/Restore level data.
- [x] Valider les tests ciblés puis la suite reverse.
- [x] Valider le build `TombRaiderChronicles_PSXPC_N`.
- [x] Contrôler les fichiers staged contre assets/dumps originaux et fuites metadata.
- [x] Committer et pousser.

## Result

Fichiers ajoutés :

- `scripts/reverse/restoreleveldata_group5_source_field_identity_checklist.py`
- `tests/reverse/test_restoreleveldata_group5_source_field_identity_checklist.py`
- `docs/reverse/generated/restoreleveldata-group5-source-field-identity-checklist.csv`
- `docs/reverse/functions/restoreleveldata-group5-source-field-identity-checklist.md`

Fichiers modifiés :

- `docs/reverse/functions/savegame-level-data.md`
- `docs/stories/README.md`

Métriques produites :

- source inputs : `RE-017, RE-025, GAME/SAVEGAME.C`
- target save group : `5`
- restore group : `6`
- checklist rows : `5`
- patch-ready checklist rows : `0`
- status : `restoreleveldata-group5-source-field-identity-checklist-blocked`

## Findings

RE-028 confirme que le group `5` n'est pas prêt pour patch source :

- `packed-status-flags` : le packed status word existe en source mais reste seulement un anchor du payload cluster.
- `item_flags[0..3]` : les header predicates sont visibles, mais les quatre payload write bodies et restore assignments restent absents/non prouvés.
- `timer` : header predicate visible, mais payload body et restore assignment restent non prouvés.
- `trigger_flags` : header predicate visible, mais payload body et restore assignment restent non prouvés.
- `object-extension` : huit payload rows / 56 bytes restent sans source field identity ni object predicate map.

## Commands

```bash
python3 -m pytest tests/reverse/test_restoreleveldata_group5_source_field_identity_checklist.py -q
python3 scripts/reverse/restoreleveldata_group5_source_field_identity_checklist.py
python3 -m py_compile scripts/reverse/restoreleveldata_group5_source_field_identity_checklist.py
python3 -m pytest tests/reverse -q
cmake --build BUILD/re005-psxpcn-disc --target TombRaiderChronicles_PSXPC_N -j2
```

Validation metadata effectuée avant commit :

- generated CSV/Markdown guard : OK, aucun champ brut de dump/original n'est versionné.
- staged asset guard : OK, aucun asset lourd ou dump original n'est staged.

## Acceptance criteria

- [x] Le rapport cible explicitement le save group `5` / restore group `6`.
- [x] Les cinq payload families RE-025 sont couvertes.
- [x] Chaque ligne indique source identity state, restore identity state, required evidence, blocker, status et safe next action.
- [x] Le verdict conserve `patch-ready checklist rows = 0`.
- [x] Les sorties excluent mots machine, coordonnées payload, adresses brutes et cibles brutes.
- [x] Aucun patch `GAME/SAVEGAME.C`.
- [x] Aucun marqueur `(F)`, `(D)` ou `(**)` n'est ajouté.

## Verdict

RE-028 est une checklist bloquante : elle définit les preuves requises mais n'autorise aucun patch source. La suite sûre est de prouver une famille payload-body group `5` de bout en bout, sans publier de données brutes originales.

## Next step

RE-029 : prouver une famille payload-body group `5` end-to-end, en commençant par `item_flags[0..3]` si les source identities peuvent être récupérées sans publier de payload brut.
