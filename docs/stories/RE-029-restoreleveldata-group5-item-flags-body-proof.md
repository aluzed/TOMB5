# RE-029 — Prouver item_flags[0..3] payload-body RestoreLevelData group 5

Status: Done
Owner: Hermes
Priority: P0
Type: Reverse payload-body proof

## Goal

Prouver metadata-only la famille payload-body `item_flags[0..3]` du save group `5` / restore group `6`, en partant de la checklist RE-028, et déterminer si elle peut devenir code-change-ready.

## Context

RE-028 a identifié `item_flags[0..3]` comme première famille payload-body à traiter : les header predicates sont visibles dans `GAME/SAVEGAME.C`, mais les quatre payload write bodies et les restore assignments restent non prouvés. RE-029 resserre donc la preuve à une ligne par flag, sans lire ni publier de données brutes originales.

## Scope

- Consommer uniquement les CSV metadata-only RE-017, RE-019, RE-021 et RE-028, plus le texte source `GAME/SAVEGAME.C` pour présence de predicates/writes.
- Cibler le save group `5`, restore group `6`, payload family `item_flags[0..3]`.
- Publier une ligne par `item_flags[0]`, `[1]`, `[2]`, `[3]`.
- Indiquer header predicate, source body evidence, save payload width, restore candidate width/context, body order status, proof status et safe next action.
- Garder `patch-ready rows = 0` tant qu'il n'existe pas de separate source write body ni de restore assignment identity versionable.
- Ne pas lire ni publier de dump brut, mot machine, coordonnée de payload, cible brute de branche/call ou adresse originale.
- Ne pas modifier `GAME/SAVEGAME.C`.
- Ne pas ajouter `(F)`, `(D)` ou `(**)`.

## Progress

- [x] Ajouter/faire échouer les tests RED du générateur RE-029.
- [x] Implémenter le générateur metadata-only RE-029.
- [x] Générer CSV/Markdown versionables.
- [x] Mettre à jour l'index stories et la documentation Save/Restore level data.
- [x] Valider les tests ciblés puis la suite reverse.
- [x] Valider le build `TombRaiderChronicles_PSXPC_N`.
- [x] Contrôler les fichiers staged contre assets/dumps originaux et fuites metadata.
- [x] Committer et pousser.

## Result

Fichiers ajoutés :

- `scripts/reverse/restoreleveldata_group5_item_flags_body_proof.py`
- `tests/reverse/test_restoreleveldata_group5_item_flags_body_proof.py`
- `docs/reverse/generated/restoreleveldata-group5-item-flags-body-proof.csv`
- `docs/reverse/functions/restoreleveldata-group5-item-flags-body-proof.md`

Fichiers modifiés :

- `docs/reverse/functions/savegame-level-data.md`
- `docs/stories/README.md`

Métriques produites :

- source inputs : `RE-017, RE-021, RE-028, GAME/SAVEGAME.C`
- target save group : `5`
- restore group : `6`
- payload family : `item_flags[0..3]`
- proof rows : `4`
- patch-ready rows : `0`
- status : `restoreleveldata-group5-item-flags-body-proof-blocked`

## Findings

RE-029 prouve la limite actuelle :

- Les quatre header predicates source existent : `item_flags[0]`, `[1]`, `[2]`, `[3]` alimentent des bits du control word.
- Les quatre payload widths save-side sont `2` bytes dans les métadonnées RE-017.
- Le restore group `6` fournit seulement un contexte candidat compact avec widths `2` disponibles.
- Aucun separate `Write` source pour les payload bodies n'existe dans le source courant.
- Aucune restore assignment identity versionable n'est disponible.

Donc le statut reste `candidate-width-only`, pas une preuve source-field identity.

## Commands

```bash
python3 -m pytest tests/reverse/test_restoreleveldata_group5_item_flags_body_proof.py -q
python3 scripts/reverse/restoreleveldata_group5_item_flags_body_proof.py
python3 -m py_compile scripts/reverse/restoreleveldata_group5_item_flags_body_proof.py
python3 -m pytest tests/reverse -q
cmake --build BUILD/re005-psxpcn-disc --target TombRaiderChronicles_PSXPC_N -j2
```

Validation metadata effectuée avant commit :

- generated CSV/Markdown guard : OK, aucun champ brut de dump/original n'est versionné.
- staged asset guard : OK, aucun asset lourd ou dump original n'est staged.

## Acceptance criteria

- [x] Le rapport cible explicitement `item_flags[0..3]` du save group `5` / restore group `6`.
- [x] Les quatre flags ont une ligne dédiée.
- [x] Chaque ligne indique predicate source, body evidence, width save/restore, status et safe next action.
- [x] Le verdict conserve `patch-ready rows = 0`.
- [x] Les sorties excluent mots machine, coordonnées payload, adresses brutes et cibles brutes.
- [x] Aucun patch `GAME/SAVEGAME.C`.
- [x] Aucun marqueur `(F)`, `(D)` ou `(**)` n'est ajouté.

## Verdict

RE-029 est une preuve bloquante : les widths et predicates headers sont utiles, mais ne prouvent pas les payload bodies ni les restore assignments. Aucun patch source n'est autorisé.

## Next step

RE-030 : récupérer une restore assignment identity map versionable pour les payload bodies du group `5`, ou exclure/defer explicitement le group `5` de tout scope de reconstruction source.
