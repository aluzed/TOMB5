# RE-026 — Prouver le fanout subtype/layout RestoreLevelData du save group 8

Status: Done
Owner: Hermes
Priority: P0
Type: Reverse proof audit

## Goal

Prouver ou bloquer explicitement les predicates du save group `8` issus de RE-023/RE-025 : subtype byte, layout block `20`, room/rotation ordering, item data word, item_flags payloads, anim-state payloads et extra restore byte, tout en restant metadata-only et sans patcher `GAME/SAVEGAME.C`.

## Context

RE-023 avait identifié le save group `8` comme le fanout/layout blocker le plus risqué. RE-025 a confirmé que les item flag payload bodies restent bloqués pour le save group `5`; RE-026 transporte ce blocker vers le save group `8`, où les item flag payloads réapparaissent dans un fanout object/subtype plus large.

## Scope

- Consommer uniquement les CSV metadata-only déjà versionnés : RE-017, RE-020, RE-021, RE-022, RE-023 et RE-025.
- Cibler le save group `8` et le restore group `8`.
- Produire une matrice par famille : subtype/extra byte, position layout block, room/rotation ordering, speed/fallspeed, item data word, item_flags, anim-state payload.
- Publier profils save/restore, source predicate profile, branch profile, dépendance RE-025, blockers, verdict et next action.
- Ne pas lire ni publier de dump brut, mot machine, coordonnée de payload, cible brute de branche/call ou adresse originale.
- Ne pas modifier `GAME/SAVEGAME.C`.
- Ne pas ajouter `(F)`, `(D)` ou `(**)`.

## Progress

- [x] Ajouter/faire échouer les tests RED du générateur RE-026.
- [x] Implémenter le générateur metadata-only RE-026.
- [x] Générer CSV/Markdown versionables.
- [x] Mettre à jour l'index stories et la documentation SaveLevelData.
- [x] Valider les tests ciblés puis la suite reverse.
- [x] Valider le build `TombRaiderChronicles_PSXPC_N`.
- [x] Contrôler les fichiers staged contre assets/dumps originaux et fuites metadata.
- [x] Committer et pousser.

## Result

Fichiers ajoutés :

- `scripts/reverse/restoreleveldata_group8_layout_fanout_proof.py`
- `tests/reverse/test_restoreleveldata_group8_layout_fanout_proof.py`
- `docs/reverse/generated/restoreleveldata-group8-layout-fanout-proof.csv`
- `docs/reverse/functions/restoreleveldata-group8-layout-fanout-proof.md`

Fichiers modifiés :

- `docs/reverse/functions/savegame-level-data.md`
- `docs/stories/README.md`

Métriques produites :

- target save group : `8`
- restore group : `8`
- fanout rows : `7`
- code-change-ready fanout families : `0`
- status : `restoreleveldata-group8-layout-fanout-proof-blocked`

## Findings

RE-026 clarifie le fanout/layout du save group `8`, mais ne débloque aucun patch source :

- `subtype-extra-byte` : subtype byte et extra restore byte candidate restent sans source predicate.
- `position-layout-block` : layout block `20` incompatible avec les split position writes actuels.
- `room-rotation-ordering` : payload `2` bytes non aligné avec l'ordre room/rotation source actuel.
- `speed-fallspeed` : widths source-visibles, mais le fanout/layout englobant reste non prouvé.
- `item-data-word` : payload word `4` bytes sans source field identity.
- `item_flags[3,0,1]` : payload bodies non prouvés, dépendance explicite au blocker RE-025 `group5-item-flag-payloads-blocked`.
- `anim-state-payload` : widths source-visibles, mais la branch fanout identity reste non prouvée.

## Commands

```bash
python3 -m pytest tests/reverse/test_restoreleveldata_group8_layout_fanout_proof.py -q
python3 scripts/reverse/restoreleveldata_group8_layout_fanout_proof.py
python3 -m py_compile scripts/reverse/restoreleveldata_group8_layout_fanout_proof.py
python3 -m pytest tests/reverse/test_restoreleveldata_group8_layout_fanout_proof.py tests/reverse/test_restoreleveldata_group5_payload_predicate_proof.py -q
python3 -m pytest tests/reverse -q
cmake --build BUILD/re005-psxpcn-disc --target TombRaiderChronicles_PSXPC_N -j2
```

Validation metadata effectuée avant commit :

- generated CSV/Markdown guard : OK, aucun champ brut de dump/original n'est versionné.
- staged asset guard : OK, aucun asset lourd ou dump original n'est staged.

## Acceptance criteria

- [x] Le rapport cible le save group `8` et le restore group `8`.
- [x] Les familles subtype/extra byte, layout block `20`, room/rotation ordering, item data word, item_flags payloads et anim-state payloads sont explicitement couvertes.
- [x] Le blocker RE-025 sur item flag payload bodies est conservé.
- [x] Le verdict conserve `code-change-ready fanout families = 0`.
- [x] Les sorties excluent mots machine, coordonnées payload, adresses brutes et cibles brutes.
- [x] Aucun patch `GAME/SAVEGAME.C`.
- [x] Aucun marqueur `(F)`, `(D)` ou `(**)` n'est ajouté.

## Verdict

RE-026 est une preuve bloquante : le save group `8` contient quelques width matches, mais pas de predicate source-level suffisant pour le subtype fanout, les extra bytes ou les payload bodies.

## Next step

RE-027 : rafraîchir le plan de readiness `RestoreLevelData` à partir de RE-024, RE-025 et RE-026, puis décider s'il faut poursuivre la preuve source-field identity ou ouvrir un ticket de reconstruction source limité aux familles réellement prouvées.
