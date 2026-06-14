# RE-015 — Reconstruire la sérialisation active item de SaveLevelData

Status: Done
Owner: Hermes
Priority: P0
Type: Reverse implementation

## Goal

Corriger le modèle source `SaveLevelData` pour que la branche item active/full-save sérialise le mot de contrôle actif et les flags item sauvegardables, puis régénérer l'audit RE-014 afin de vérifier si les groupes originaux `4` et `6` deviennent représentables par le modèle source.

## Context

RE-014 a montré deux gaps source-level concrets dans la branche item active/full-save:

- `word = 0x8000` était assemblé mais n'était pas écrit avant les champs optionnels.
- `if (obj->save_flags)` ne contenait aucun `Write(...)` malgré le commentaire de packing `item->flags` + bits d'activation.

Ces gaps empêchaient les groupes item originaux `4` (`17` appels) et `6` (`3` appels) d'être représentés par le modèle source.

## Scope

- Ajouter des tests RED qui imposent un `Write(&word, 2)` dans la branche active item.
- Ajouter des tests RED qui imposent un site d'écriture pour `obj->save_flags`.
- Implémenter la correction minimale dans `GAME/SAVEGAME.C`.
- Mettre à jour `scripts/reverse/saveleveldata_item_flag_audit.py` pour modéliser le header actif et `save_flags`.
- Régénérer les artefacts versionables RE-014/RE-015.
- Mettre à jour la documentation SaveLevelData et l'index des stories.
- Ne pas committer de dumps originaux, assets, instructions ou mots machine.
- Ne pas ajouter `(F)`, `(D)` ou `(**)` sans preuve de contrôle-flow complète.

## Progress

- [x] Ajouter la story RE-015 avec tracker explicite.
- [x] Ajouter/faire échouer les tests RED pour le header actif et `save_flags`.
- [x] Implémenter la sérialisation active item minimale.
- [x] Adapter et régénérer l'audit item flag.
- [x] Valider les tests reverse.
- [x] Valider le build `TombRaiderChronicles_PSXPC_N`.
- [x] Contrôler les fichiers staged contre assets/dumps originaux.
- [x] Committer et pousser.

## Implementation

`GAME/SAVEGAME.C` sérialise désormais la branche item active/full-save comme suit:

- Le mot de contrôle `word` est écrit avec `Write(&word, 2)` après l'assemblage des bits et avant les payloads optionnels.
- `obj->save_flags` écrit un mot 32-bit packé:
  - bits bas: `(unsigned short)item->flags`
  - bits hauts: bits `active/status/gravity_status/hit_status/collidable/looked_at/dynamic_light/poisoned/ai_bits/really_active` limités au modèle commenté par le source existant.

## Result

Fichiers principaux modifiés/ajoutés:

- `GAME/SAVEGAME.C`
- `scripts/reverse/saveleveldata_item_flag_audit.py`
- `scripts/reverse/savegame_schema.py`
- `tests/reverse/test_savegame_source.py`
- `tests/reverse/test_saveleveldata_item_flag_audit.py`
- `tests/reverse/test_saveleveldata_call_map.py`
- `docs/reverse/generated/savegame-level-data-schema.csv`
- `docs/reverse/generated/savegame-level-data-schema.md`
- `docs/reverse/generated/saveleveldata-item-flag-audit.csv`
- `docs/reverse/functions/saveleveldata-item-flag-audit.md`
- `docs/reverse/functions/saveleveldata-original-audit.md`
- `docs/reverse/functions/saveleveldata-write-call-map.md`
- `docs/reverse/functions/savegame-level-data.md`
- `docs/stories/README.md`

Métriques après régénération:

- source-level static `Write(...)` sites: `34`
- groupes item candidats: `9`
- appels originaux `WriteSG` dans ces groupes: `64`
- counts représentables par le modèle source actif: `1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17`
- active control word écrit: `yes`
- sites `save_flags` écrits: `1`
- groupes item non représentables par count: `none`
- statut item audit: `counts-representable-needs-proof`

## Commands

```bash
python3 -m pytest tests/reverse/test_saveleveldata_item_flag_audit.py -q
python3 scripts/reverse/savegame_schema.py
python3 scripts/reverse/saveleveldata_original_audit.py
python3 scripts/reverse/saveleveldata_call_map.py
python3 scripts/reverse/saveleveldata_item_flag_audit.py
python3 -m py_compile scripts/reverse/savegame_schema.py scripts/reverse/saveleveldata_call_map.py scripts/reverse/saveleveldata_item_flag_audit.py scripts/reverse/saveleveldata_original_audit.py
python3 -m pytest tests/reverse -q
cmake --build BUILD/re005-psxpcn-disc --target TombRaiderChronicles_PSXPC_N -j2
git diff --cached --name-only | python3 -c 'import sys; bad=[p.strip() for p in sys.stdin if p.strip().startswith(("build/", "GAMEWAD", "CODE.WAD")) or p.strip().endswith((".BIN", ".CUE", ".OBJ"))]; print("asset guard ok" if not bad else "blocked: "+", ".join(bad)); sys.exit(1 if bad else 0)'
```

Validation:

- `14 passed`
- `Built target TombRaiderChronicles_PSXPC_N`
- Asset/staging guard: `asset guard ok`

## Acceptance criteria

- [x] La branche active/full-save écrit le mot de contrôle `word` avant les champs optionnels.
- [x] `obj->save_flags` produit un site `Write(...)` versionable.
- [x] Les counts représentables incluent `3` et `17`.
- [x] L'audit généré ne liste plus les groupes `4` et `6` comme non représentables par count.
- [x] Les artefacts générés ne contiennent pas d'instructions originales ni de mots machine.
- [x] Aucun marqueur `(F)`, `(D)` ou `(**)` n'est ajouté.

## Verdict

RE-015 résout les gaps de count source-level identifiés par RE-014. Les groupes item `4` et `6` deviennent représentables par le modèle source après ajout du header actif et du write `save_flags`.

Ce résultat reste un audit de comptage et de structure source. Il ne prouve pas encore l'équivalence de contrôle-flow avec l'original, et ne justifie donc aucun marqueur `(F)`, `(D)` ou `(**)`.

## Next step

RE-016: prouver les conditions de branche/flags des groupes item désormais représentables (`4` à `12`) contre une preuve de contrôle-flow versionable, puis seulement ensuite réévaluer les marqueurs de complétude.
