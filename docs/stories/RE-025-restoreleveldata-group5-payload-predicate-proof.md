# RE-025 — Prouver les payload predicates RestoreLevelData du save group 5

Status: Done
Owner: Hermes
Priority: P0
Type: Reverse proof audit

## Goal

Prouver ou bloquer explicitement les payload predicates du save group `5` issus de RE-023 : `item_flags[0..3]`, `timer`, `trigger_flags`, et payloads object-specific, tout en restant metadata-only et sans patcher `GAME/SAVEGAME.C`.

## Context

RE-023 a identifié le save group `5` comme prochaine étape proof-first après RE-024. RE-022/RE-023 indiquaient que seul le packed status-flags word est source-backed ; les payloads séparés item flags / timer / trigger / object-extension restaient sans preuve source-level.

## Scope

- Consommer uniquement les CSV metadata-only déjà versionnés : RE-017, RE-020, RE-021, RE-022 et RE-023.
- Cibler le save group `5` et le restore group `6`.
- Produire une matrice par famille de payload : packed flags, item flags, timer, trigger flags, object extension.
- Publier profils save/restore, source predicate profile, branch profile, blockers, verdict et next action.
- Ne pas lire ni publier de dump brut, mot machine, coordonnée de payload, cible brute de branche/call ou adresse originale.
- Ne pas modifier `GAME/SAVEGAME.C`.
- Ne pas ajouter `(F)`, `(D)` ou `(**)`.

## Progress

- [x] Ajouter/faire échouer les tests RED du générateur RE-025.
- [x] Implémenter le générateur metadata-only RE-025.
- [x] Générer CSV/Markdown versionables.
- [x] Mettre à jour l'index stories et la documentation SaveLevelData.
- [x] Valider les tests ciblés puis la suite reverse.
- [x] Valider le build `TombRaiderChronicles_PSXPC_N`.
- [x] Contrôler les fichiers staged contre assets/dumps originaux et fuites metadata.
- [x] Committer et pousser.

## Result

Fichiers ajoutés :

- `scripts/reverse/restoreleveldata_group5_payload_predicate_proof.py`
- `tests/reverse/test_restoreleveldata_group5_payload_predicate_proof.py`
- `docs/reverse/generated/restoreleveldata-group5-payload-predicate-proof.csv`
- `docs/reverse/functions/restoreleveldata-group5-payload-predicate-proof.md`

Fichiers modifiés :

- `docs/reverse/functions/savegame-level-data.md`
- `docs/stories/README.md`

Métriques produites :

- target save group : `5`
- restore group : `6`
- payload rows : `5`
- code-change-ready payload families : `0`
- status : `restoreleveldata-group5-payload-proof-blocked`

## Findings

RE-025 clarifie les payload predicates sans débloquer de patch source :

- `packed-status-flags` : anchor source-backed (`4` bytes), mais seulement comme point d'ancrage du cluster.
- `item_flags[0..3]` : header-bit predicates visibles, mais les `4` payload words séparés restent absents du source actuel.
- `timer` : header-bit predicate visible, mais payload body / restore assignment non prouvés.
- `trigger_flags` : header-bit predicate visible, mais payload body / restore assignment non prouvés.
- `object-extension` : `8` payload rows, `56` bytes dont rare blocks `24,20`, sans source predicate ni field identity.

## Commands

```bash
python3 -m pytest tests/reverse/test_restoreleveldata_group5_payload_predicate_proof.py -q
python3 scripts/reverse/restoreleveldata_group5_payload_predicate_proof.py
python3 -m py_compile scripts/reverse/restoreleveldata_group5_payload_predicate_proof.py
python3 -m pytest tests/reverse/test_restoreleveldata_group5_payload_predicate_proof.py tests/reverse/test_restoreleveldata_room_split_predicate_proof.py -q
python3 -m pytest tests/reverse -q
cmake --build BUILD/re005-psxpcn-disc --target TombRaiderChronicles_PSXPC_N -j2
```

Validation metadata effectuée avant commit :

- generated CSV/Markdown guard : OK, aucun champ brut de dump/original n'est versionné.
- staged asset guard : OK, aucun asset lourd ou dump original n'est staged.

## Acceptance criteria

- [x] Le rapport cible le save group `5` et le restore group `6`.
- [x] Les familles `item_flags[0..3]`, `timer`, `trigger_flags` et object-extension sont explicitement couvertes.
- [x] Le verdict conserve `code-change-ready payload families = 0`.
- [x] Les sorties excluent mots machine, coordonnées payload, adresses brutes et cibles brutes.
- [x] Aucun patch `GAME/SAVEGAME.C`.
- [x] Aucun marqueur `(F)`, `(D)` ou `(**)` n'est ajouté.

## Verdict

RE-025 est une preuve bloquante : elle montre quels predicates sont source-visibles comme bits de header, mais les payload bodies et object-extension predicates ne sont pas source-backed.

## Next step

RE-026 : prouver le fanout subtype/layout object du save group `8`, tout en gardant les payload-body blockers du save group `5` visibles pour un ticket ultérieur source-field identity.
