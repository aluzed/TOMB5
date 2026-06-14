# RE-016 — Prouver le contrôle-flow item de SaveLevelData

Status: Done
Owner: Hermes
Priority: P0
Type: Reverse audit

## Goal

Auditer les groupes item `4` à `12` désormais représentables par count après RE-015 contre une preuve de contrôle-flow versionable: séquences de tailles `WriteSG` originales dérivées, séquences de tailles source possibles, et verdict exact-match / mismatch.

## Context

RE-015 a résolu les gaps de comptage source-level en ajoutant le header actif `Write(&word, 2)` et un write `save_flags`. Les groupes `4` et `6` sont maintenant représentables par count, mais RE-015 ne prouve pas que les chemins source et original ont les mêmes tailles et conditions de branche.

## Scope

- Lire le dump original ignoré uniquement pour dériver des métadonnées versionables: index/adresses d'appels `WriteSG` et tailles d'argument `a1`.
- Ne pas versionner d'instructions originales, mots machine, payload offsets, assets ou dumps.
- Générer une matrice item contrôle-flow en CSV/Markdown.
- Comparer les séquences de tailles originales par groupe aux séquences source possibles de la branche item active/full-save.
- Lister explicitement les groupes exact-match et mismatch.
- Ne pas corriger le serializer dans cette story: RE-016 est un audit et a trouvé des mismatches.
- Ne pas ajouter `(F)`, `(D)` ou `(**)`.

## Progress

- [x] Ajouter la story RE-016 avec tracker explicite.
- [x] Ajouter/faire échouer les tests RED pour l'audit contrôle-flow item.
- [x] Implémenter le générateur `saveleveldata_item_control_flow_audit.py`.
- [x] Générer CSV/Markdown versionables.
- [x] Mettre à jour l'index stories et la doc SaveLevelData.
- [x] Valider tests reverse.
- [x] Valider le build `TombRaiderChronicles_PSXPC_N`.
- [x] Contrôler les fichiers staged contre assets/dumps originaux.
- [x] Committer et pousser.

## Result

Fichiers ajoutés:

- `scripts/reverse/saveleveldata_item_control_flow_audit.py`
- `tests/reverse/test_saveleveldata_item_control_flow_audit.py`
- `docs/reverse/generated/saveleveldata-item-control-flow-audit.csv`
- `docs/reverse/functions/saveleveldata-item-control-flow-audit.md`

Fichiers modifiés:

- `scripts/reverse/saveleveldata_call_map.py`
- `docs/reverse/generated/saveleveldata-write-call-map.csv`
- `docs/reverse/functions/saveleveldata-write-call-map.md`
- `docs/reverse/generated/saveleveldata-item-flag-audit.csv`
- `docs/reverse/functions/saveleveldata-item-flag-audit.md`
- `docs/reverse/functions/savegame-level-data.md`
- `docs/stories/README.md`

Métriques produites:

- groupes item couverts: `9`
- exact size-sequence match groups: `12`
- mismatch groups: `4, 5, 6, 7, 8, 9, 10, 11`
- status: `control-flow-gaps-found`

## Findings

RE-016 invalide l'hypothèse forte "count représentable = contrôle-flow prouvé".

- Le groupe `12` a au moins une séquence de tailles source exacte: `active_header=1 + save_anim=lara + save_hitpoints=1`.
- Les groupes `4, 5, 6, 7, 8, 9, 10, 11` restent mismatch par séquence exacte.
- Plusieurs groupes contiennent des tailles originales qui ne sont pas expliquées par le modèle source actif actuel, notamment des writes `1`, `4`, `20` ou `24` dans des positions incompatibles avec les cas source énumérés.
- Les groupes avec des writes d'états anim en byte suggèrent une divergence de largeur source-vs-original à investiguer avant toute correction.

## Commands

```bash
python3 -m pytest tests/reverse/test_saveleveldata_item_control_flow_audit.py -q
python3 scripts/reverse/saveleveldata_call_map.py
python3 scripts/reverse/saveleveldata_item_flag_audit.py
python3 scripts/reverse/saveleveldata_item_control_flow_audit.py
python3 -m py_compile scripts/reverse/saveleveldata_call_map.py scripts/reverse/saveleveldata_item_control_flow_audit.py scripts/reverse/saveleveldata_item_flag_audit.py
python3 -m pytest tests/reverse -q
cmake --build BUILD/re005-psxpcn-disc --target TombRaiderChronicles_PSXPC_N -j2
git diff --cached --name-only | python3 -c 'import sys; bad=[p.strip() for p in sys.stdin if p.strip().startswith(("build/",)) or p.strip().endswith((".BIN", ".CUE", ".OBJ", ".WAD"))]; print("asset guard ok" if not bad else "blocked: "+", ".join(bad)); sys.exit(1 if bad else 0)'
```

Validation:

- `17 passed`
- `Built target TombRaiderChronicles_PSXPC_N`
- Asset/staging guard: `asset guard ok`

## Acceptance criteria

- [x] La matrice couvre les groupes item `4` à `12`.
- [x] Les sorties ne contiennent pas `instruction`, `word_le_hex`, `payload_offset` ni instruction originale.
- [x] Les tailles d'appel originales sont dérivées en métadonnées, pas copiées avec les instructions.
- [x] Les groupes exact-match et mismatch sont listés.
- [x] Le verdict indique clairement que RE-016 rejette l'équivalence de contrôle-flow item actuelle.
- [x] Aucun marqueur `(F)`, `(D)` ou `(**)` n'est ajouté.

## Verdict

RE-016 ne prouve pas l'équivalence de contrôle-flow item. Il trouve au contraire des gaps de séquence de tailles: seul le groupe `12` matche exactement un cas source, tandis que les groupes `4, 5, 6, 7, 8, 9, 10, 11` restent incompatibles par taille/ordre.

Aucun marqueur `(F)`, `(D)` ou `(**)` ne doit être ajouté à `SaveLevelData` sur cette base.

## Next step

RE-017: investiguer les mismatches de largeur/champs, en priorisant les writes originaux byte-sized des états anim et les writes originaux `4`, `20`, `24` non modélisés par la branche source actuelle. Produire une table source-vs-original de champs probables avant tout patch.
