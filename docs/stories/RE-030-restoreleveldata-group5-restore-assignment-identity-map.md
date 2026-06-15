# RE-030 — Restore assignment identity map RestoreLevelData group 5

Status: Done
Owner: Hermes
Priority: P0
Type: Reverse restore-assignment identity audit

## Goal

Récupérer ou formaliser une map versionable des restore assignments pour les payload bodies du save group `5` / restore group `6`, puis décider si le group `5` peut entrer dans un scope de reconstruction source.

## Context

RE-029 a montré que `item_flags[0..3]` reste `candidate-width-only` : les header predicates et widths existent, mais pas les payload bodies ni les restore assignments. RE-030 élargit cette vérification aux cinq payload families du group `5` et formalise la décision de scope.

## Scope

- Consommer uniquement les CSV metadata-only RE-019, RE-022, RE-025, RE-028 et RE-029, plus le texte source `GAME/SAVEGAME.C` pour disponibilité du body `RestoreLevelData`.
- Cibler le save group `5`, restore group `6`.
- Publier une ligne par payload family : `packed-status-flags`, `item_flags[0..3]`, `timer`, `trigger_flags`, `object-extension`.
- Indiquer prior body proof, restore candidate profile, restore assignment evidence, assignment identity state, required evidence, readiness et safe next action.
- Garder `assignment-identity-ready rows = 0` et `patch-ready rows = 0` tant qu'aucune identité d'assignation restore versionable n'existe.
- Ne pas lire ni publier de dump brut, mot machine, coordonnée de payload, cible brute de branche/call ou adresse originale.
- Ne pas modifier `GAME/SAVEGAME.C`.
- Ne pas ajouter `(F)`, `(D)` ou `(**)`.

## Progress

- [x] Ajouter/faire échouer les tests RED du générateur RE-030.
- [x] Implémenter le générateur metadata-only RE-030.
- [x] Générer CSV/Markdown versionables.
- [x] Mettre à jour l'index stories et la documentation Save/Restore level data.
- [x] Valider les tests ciblés puis la suite reverse.
- [x] Valider le build `TombRaiderChronicles_PSXPC_N`.
- [x] Contrôler les fichiers staged contre assets/dumps originaux et fuites metadata.
- [x] Committer et pousser.

## Result

Fichiers ajoutés :

- `scripts/reverse/restoreleveldata_group5_restore_assignment_identity_map.py`
- `tests/reverse/test_restoreleveldata_group5_restore_assignment_identity_map.py`
- `docs/reverse/generated/restoreleveldata-group5-restore-assignment-identity-map.csv`
- `docs/reverse/functions/restoreleveldata-group5-restore-assignment-identity-map.md`

Fichiers modifiés :

- `docs/reverse/functions/savegame-level-data.md`
- `docs/stories/README.md`

Métriques produites :

- source inputs : `RE-019, RE-022, RE-025, RE-028, RE-029, GAME/SAVEGAME.C`
- target save group : `5`
- restore group : `6`
- restore source state : `RestoreLevelData source body is UNIMPLEMENTED`
- group 5 decision : `defer-group5-from-source-reconstruction`
- map rows : `5`
- assignment-identity-ready rows : `0`
- patch-ready rows : `0`
- status : `restoreleveldata-group5-restore-assignment-identity-map-blocked`

## Findings

RE-030 ne récupère pas de restore assignment identity map versionable :

- Le restore group `6` reste un candidate payload cluster metadata-only.
- Le source courant `RestoreLevelData` est toujours absent / `UNIMPLEMENTED`.
- `packed-status-flags` nécessite une assignment restore nommée du packed word et une preuve d'indépendance des payload bodies suivants.
- `item_flags[0..3]` nécessite quatre restore assignments nommées, leur ordre body, et une identité source/restore.
- `timer` et `trigger_flags` nécessitent chacun une assignment restore nommée et une identité de predicate.
- `object-extension` nécessite les target fields restore, object predicate map et block assignment order.

Donc la décision sûre est de déférer/exclure le group `5` de tout scope de reconstruction source tant que ces identités ne sont pas disponibles.

## Commands

```bash
python3 -m pytest tests/reverse/test_restoreleveldata_group5_restore_assignment_identity_map.py -q
python3 scripts/reverse/restoreleveldata_group5_restore_assignment_identity_map.py
python3 -m py_compile scripts/reverse/restoreleveldata_group5_restore_assignment_identity_map.py
python3 -m pytest tests/reverse -q
cmake --build BUILD/re005-psxpcn-disc --target TombRaiderChronicles_PSXPC_N -j2
```

Validation metadata effectuée avant commit :

- generated CSV/Markdown guard : OK, aucun champ brut de dump/original n'est versionné.
- staged asset guard : OK, aucun asset lourd ou dump original n'est staged.

## Acceptance criteria

- [x] Le rapport cible explicitement le save group `5` / restore group `6`.
- [x] Les cinq payload families group `5` sont couvertes.
- [x] Chaque ligne indique restore assignment evidence, identity state, required evidence, readiness et safe next action.
- [x] Le verdict conserve `assignment-identity-ready rows = 0` et `patch-ready rows = 0`.
- [x] La décision `defer-group5-from-source-reconstruction` est explicite.
- [x] Les sorties excluent mots machine, coordonnées payload, adresses brutes et cibles brutes.
- [x] Aucun patch `GAME/SAVEGAME.C`.
- [x] Aucun marqueur `(F)`, `(D)` ou `(**)` n'est ajouté.

## Verdict

RE-030 est une map bloquante : les restore assignments du group `5` ne sont pas versionablement identifiées. Group `5` doit être déféré/exclu d'un scope de reconstruction source tant qu'un futur proof ne peut pas nommer les target fields restore sans publier de données brutes.

## Next step

RE-031 : définir un scope limité de reconstruction `RestoreLevelData` qui exclut explicitement le group `5`, ou produire une méthode non-raw d'extraction d'assignments capable de débloquer group `5` en sécurité.
