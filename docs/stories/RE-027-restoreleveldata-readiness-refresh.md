# RE-027 — Rafraîchir le plan de readiness RestoreLevelData

Status: Done
Owner: Hermes
Priority: P0
Type: Reverse readiness audit

## Goal

Consolider RE-024, RE-025 et RE-026 dans une matrice de readiness `RestoreLevelData` actualisée, metadata-only, avant toute décision de patch source ou de marker `(F)`, `(D)` ou `(**)`.

## Context

RE-023 avait produit le premier plan de readiness à partir des blockers RE-022. RE-024 a clarifié les blockers room/split des save groups `10` et `4`. RE-025 a clarifié les payload predicates du save group `5`. RE-026 a clarifié le fanout/layout du save group `8`. RE-027 rafraîchit la décision globale à partir de ces preuves récentes.

## Scope

- Consommer uniquement les CSV metadata-only versionnés RE-023, RE-024, RE-025 et RE-026.
- Couvrir les save groups prioritaires `4`, `5`, `8`, `10`.
- Publier latest evidence, summary, prior phase, remaining blockers, readiness phase, safe next action et next ticket.
- Garder `code-change-ready groups = 0` tant qu'aucun blocker source-field identity n'est levé.
- Ne pas lire ni publier de dump brut, mot machine, coordonnée de payload, cible brute de branche/call ou adresse originale.
- Ne pas modifier `GAME/SAVEGAME.C`.
- Ne pas ajouter `(F)`, `(D)` ou `(**)`.

## Progress

- [x] Ajouter/faire échouer les tests RED du générateur RE-027.
- [x] Implémenter le générateur metadata-only RE-027.
- [x] Générer CSV/Markdown versionables.
- [x] Mettre à jour l'index stories et la documentation SaveLevelData.
- [x] Valider les tests ciblés puis la suite reverse.
- [x] Valider le build `TombRaiderChronicles_PSXPC_N`.
- [x] Contrôler les fichiers staged contre assets/dumps originaux et fuites metadata.
- [x] Committer et pousser.

## Result

Fichiers ajoutés :

- `scripts/reverse/restoreleveldata_readiness_refresh.py`
- `tests/reverse/test_restoreleveldata_readiness_refresh.py`
- `docs/reverse/generated/restoreleveldata-readiness-refresh.csv`
- `docs/reverse/functions/restoreleveldata-readiness-refresh.md`

Fichiers modifiés :

- `docs/reverse/functions/savegame-level-data.md`
- `docs/stories/README.md`

Métriques produites :

- source proof inputs : `RE-024, RE-025, RE-026`
- target save groups : `4, 5, 8, 10`
- readiness rows : `4`
- code-change-ready groups : `0`
- status : `restoreleveldata-readiness-refresh-blocked`

## Findings

RE-027 confirme qu'aucun groupe prioritaire n'est prêt pour un patch source :

- save group `4` : split restore groups `4;5` et anim-state byte-vs-word restore predicate restent bloquants.
- save group `5` : payload bodies item_flags/timer/trigger et object-extension field identity restent bloquants.
- save group `8` : subtype/extra byte, layout block `20`, room/rotation ordering, item data word et item flag payload bodies restent bloquants.
- save group `10` : room byte order/layout predicate reste bloquant.

## Commands

```bash
python3 -m pytest tests/reverse/test_restoreleveldata_readiness_refresh.py -q
python3 scripts/reverse/restoreleveldata_readiness_refresh.py
python3 -m py_compile scripts/reverse/restoreleveldata_readiness_refresh.py
python3 -m pytest tests/reverse/test_restoreleveldata_readiness_refresh.py tests/reverse/test_restoreleveldata_group8_layout_fanout_proof.py -q
python3 -m pytest tests/reverse -q
cmake --build BUILD/re005-psxpcn-disc --target TombRaiderChronicles_PSXPC_N -j2
```

Validation metadata effectuée avant commit :

- generated CSV/Markdown guard : OK, aucun champ brut de dump/original n'est versionné.
- staged asset guard : OK, aucun asset lourd ou dump original n'est staged.

## Acceptance criteria

- [x] Le rapport consolide RE-024, RE-025 et RE-026.
- [x] Les save groups `4`, `5`, `8`, `10` sont couverts.
- [x] Chaque ligne indique latest evidence, summary, prior phase, remaining blockers, readiness phase et safe next action.
- [x] Le verdict conserve `code-change-ready groups = 0`.
- [x] Les sorties excluent mots machine, coordonnées payload, adresses brutes et cibles brutes.
- [x] Aucun patch `GAME/SAVEGAME.C`.
- [x] Aucun marqueur `(F)`, `(D)` ou `(**)` n'est ajouté.

## Verdict

RE-027 est un readiness refresh bloquant : il n'autorise pas de patch source. La suite sûre est soit une preuve source-field identity ciblée, soit un futur scope de reconstruction qui exclut explicitement toutes les familles encore bloquées.

## Next step

RE-028 : construire une checklist source-field identity pour la famille bloquée à plus forte valeur, ou définir un scope de reconstruction source volontairement limité qui exclut chaque predicate encore bloqué.
