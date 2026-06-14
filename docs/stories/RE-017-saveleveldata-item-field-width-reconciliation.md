# RE-017 — Réconcilier les champs/largeurs item SaveLevelData

Status: Done
Owner: Hermes
Priority: P0
Type: Reverse audit

## Goal

Investiguer les mismatches de séquences de tailles trouvés par RE-016 en produisant une table versionable source-vs-original des champs probables pour les groupes item `4` à `11`.

## Context

RE-016 a montré que les counts item sont représentables après RE-015, mais que la plupart des groupes ne matchent pas les séquences exactes de tailles:

- exact size-sequence match: groupe `12`
- mismatches: groupes `4, 5, 6, 7, 8, 9, 10, 11`

Ces gaps incluent des writes originaux byte-sized et des writes `4`, `20`, `24` qui ne sont pas expliqués par le modèle source actif actuel.

## Scope

- Lire le dump original ignoré seulement pour dériver des métadonnées sûres: groupe, position d'appel, adresse d'appel et taille `a1`.
- Ne pas versionner d'instructions originales, mots machine, payload offsets, assets ou dumps.
- Produire une table `original call -> source field probable/gap` avec statut explicite.
- Prioriser les byte-sized anim state writes et les tailles `4`, `20`, `24` non modélisées.
- Ne pas patcher `GAME/SAVEGAME.C` dans cette story.
- Ne pas ajouter `(F)`, `(D)` ou `(**)`.

## Progress

- [x] Ajouter la story RE-017 avec tracker explicite.
- [x] Ajouter/faire échouer les tests RED pour la table source-vs-original.
- [x] Implémenter le générateur d'audit champ/largeur.
- [x] Générer CSV/Markdown versionables.
- [x] Mettre à jour l'index stories et la documentation SaveLevelData.
- [x] Valider tests reverse.
- [x] Valider le build `TombRaiderChronicles_PSXPC_N`.
- [x] Contrôler les fichiers staged contre assets/dumps originaux.
- [x] Committer et pousser.

## Result

Fichiers ajoutés:

- `scripts/reverse/saveleveldata_item_field_width_audit.py`
- `tests/reverse/test_saveleveldata_item_field_width_audit.py`
- `docs/reverse/generated/saveleveldata-item-field-width-audit.csv`
- `docs/reverse/functions/saveleveldata-item-field-width-audit.md`

Fichiers modifiés:

- `docs/reverse/functions/savegame-level-data.md`
- `docs/stories/README.md`

Métriques produites:

- mismatch groups couverts: `4, 5, 6, 7, 8, 9, 10, 11`
- appels originaux classifiés: `57`
- exact field-width matches: `26`
- source width mismatches: `3`
- source missing fields: `21`
- source layout mismatches: `4`
- branch/sentinel groups: `3`
- status: `field-width-gaps-found`

## Findings

RE-017 transforme les mismatches RE-016 en hypothèses de champs testables:

- **Anim states byte-sized**: groupe `4`, appels `11..13`, les champs probables `item->current_anim_state`, `item->goal_anim_state`, `item->required_anim_state` sont byte-sized côté original metadata, alors que le source actuel écrit `2` octets.
- **Item flag payloads séparés**: plusieurs writes probables `item_flags[0..3]`, `timer`, `trigger_flags` existent comme payloads séparés côté original metadata, alors que le source actuel ne les représente que via bits de header ou flags packés.
- **Payloads object-specific non modélisés**: tailles originales `4`, `20`, `24` apparaissent dans des groupes mismatch et n'ont pas d'équivalent direct dans la branche source actuelle.
- **Layout/order gaps**: certains champs ont une largeur compatible mais un ordre/layout incompatible avec la séquence source actuelle, par exemple `item->room_number` dans le groupe `10`.

## Commands

```bash
python3 -m pytest tests/reverse/test_saveleveldata_item_field_width_audit.py -q
python3 scripts/reverse/saveleveldata_item_field_width_audit.py
python3 -m py_compile scripts/reverse/saveleveldata_item_field_width_audit.py scripts/reverse/saveleveldata_item_control_flow_audit.py
python3 -m pytest tests/reverse -q
cmake --build BUILD/re005-psxpcn-disc --target TombRaiderChronicles_PSXPC_N -j2
git diff --cached --name-only | python3 -c 'import sys; bad=[p.strip() for p in sys.stdin if p.strip().startswith(("build/",)) or p.strip().endswith((".BIN", ".CUE", ".OBJ", ".WAD"))]; print("asset guard ok" if not bad else "blocked: "+", ".join(bad)); sys.exit(1 if bad else 0)'
```

Validation:

- `21 passed`
- `Built target TombRaiderChronicles_PSXPC_N`
- Output metadata guard: no `instruction`, `word_le_hex`, `payload_offset`, or raw `jal` token in RE-017 outputs
- Asset/staging guard: `asset guard ok`

## Acceptance criteria

- [x] La table couvre les groupes mismatch `4` à `11`.
- [x] Les writes originaux `1`, `4`, `20`, `24` sont classés avec hypothèse et statut.
- [x] Les sorties restent metadata-only et ne contiennent pas `instruction`, `word_le_hex`, `payload_offset` ni instruction originale.
- [x] Le verdict liste les gaps source à investiguer avant tout patch.
- [x] Aucun marqueur `(F)`, `(D)` ou `(**)` n'est ajouté.

## Verdict

RE-017 ne patche pas le serializer. Il établit une table d'hypothèses source-vs-original et confirme des gaps de largeur/layout/champs manquants. Aucun marqueur `(F)`, `(D)` ou `(**)` ne doit être ajouté à `SaveLevelData` sur cette base.

## Next step

RE-018: vérifier ces hypothèses contre `RestoreLevelData` / restore-side stream reading et décider quels gaps sont de vrais manques source versus des artefacts de groupement statique. Priorité: les anim states byte-sized du groupe `4`, les payloads séparés `item_flags/timer/trigger_flags`, puis les payloads object-specific `4`, `20`, `24`.
