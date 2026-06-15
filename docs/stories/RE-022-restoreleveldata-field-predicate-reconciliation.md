# RE-022 — Réconcilier champs et prédicats RestoreLevelData

Status: Done
Owner: Hermes
Priority: P0
Type: Reverse audit

## Goal

Réconcilier les hypothèses RE-020/RE-021 avec les identités de champs source et les prédicats optionnels connus côté `SaveLevelData`, afin de distinguer les champs partiellement prouvés des payloads/prédicats encore bloquants sans modifier le serializer.

## Context

RE-021 a mappé les régions de branches RestoreLevelData mais `patch-ready groups = 0`. RE-022 relie ces régions aux champs probables de RE-017/RE-020 et aux prédicats source (`obj->save_position`, `obj->save_anim`, bits `word`, `obj->save_flags`, etc.) pour produire une matrice de blocage plus actionnable.

## Scope

- Utiliser seulement des CSV metadata-only déjà versionnés : RE-017, RE-020 et RE-021.
- Couvrir les save groups prioritaires `4`, `5`, `8`, `10` et leurs restore groups candidats `4`, `5`, `6`, `8`, `9`.
- Publier les counts de champs matchés/non résolus, les familles de prédicats source, les prédicats non prouvés, le statut de preuve et la limite restante.
- Ne pas lire ni publier de dump brut, instruction originale, mot machine, payload offset, cible brute de branche/call ou adresse originale.
- Ne pas modifier `GAME/SAVEGAME.C`.
- Ne pas ajouter `(F)`, `(D)` ou `(**)`.

## Progress

- [x] Ajouter la story RE-022 avec tracker explicite.
- [x] Ajouter/faire échouer les tests RED pour la reconciliation field/predicate.
- [x] Implémenter le générateur metadata-only RE-022.
- [x] Générer CSV/Markdown versionables.
- [x] Mettre à jour l'index stories et la documentation SaveLevelData.
- [x] Valider tests reverse.
- [x] Valider le build `TombRaiderChronicles_PSXPC_N`.
- [x] Contrôler les fichiers staged contre assets/dumps originaux et fuites metadata.
- [x] Committer et pousser.

## Result

Fichiers ajoutés :

- `scripts/reverse/restoreleveldata_field_predicate_reconciliation.py`
- `tests/reverse/test_restoreleveldata_field_predicate_reconciliation.py`
- `docs/reverse/generated/restoreleveldata-field-predicate-reconciliation.csv`
- `docs/reverse/functions/restoreleveldata-field-predicate-reconciliation.md`

Fichiers modifiés :

- `docs/reverse/functions/savegame-level-data.md`
- `docs/stories/README.md`

Métriques produites :

- save groups couverts : `4, 5, 8, 10`
- restore groups liés : `4, 5, 6, 8, 9`
- lignes de preuve : `4`
- groupes patch-ready : `0`
- status : `restore-field-predicate-reconciliation-partial`

## Findings

RE-022 rend les blocages plus actionnables mais ne débloque toujours aucun patch :

- Save group `4` → restore groups `4;5` : `14` champs matchés, `3` width mismatches ; les prédicats split et anim-state restent non prouvés.
- Save group `5` → restore group `6` : seul le packed flags word est source-backed ; `14` payloads flag/timer/trigger/object restent sans preuve source.
- Save group `8` → restore group `8` : `5` champs matchés, `7` champs layout/payload non résolus ; extra restore bytes et item flag predicates bloquent l'équivalence.
- Save group `10` → restore group `9` : `6` champs matchés, `1` room/layout mismatch ; la fenêtre exacte reste plus faible qu'une preuve de prédicat.

## Commands

```bash
python3 -m pytest tests/reverse/test_restoreleveldata_field_predicate_reconciliation.py -q
python3 scripts/reverse/restoreleveldata_field_predicate_reconciliation.py
python3 -m py_compile scripts/reverse/restoreleveldata_field_predicate_reconciliation.py
python3 -m pytest tests/reverse/test_restoreleveldata_field_predicate_reconciliation.py tests/reverse/test_restoreleveldata_branch_predicate_map.py tests/reverse/test_restoreleveldata_field_control_flow_proof.py -q
python3 -m pytest tests/reverse -q
cmake --build BUILD/re005-psxpcn-disc --target TombRaiderChronicles_PSXPC_N -j2
python3 - <<'PY'
from pathlib import Path
paths = [
    Path('docs/reverse/generated/restoreleveldata-field-predicate-reconciliation.csv'),
    Path('docs/reverse/functions/restoreleveldata-field-predicate-reconciliation.md'),
]
for p in paths:
    text = p.read_text(encoding='utf-8')
    bad = [tok for tok in ('instruction', 'word_le_hex', 'payload_offset', 'jal 0x', '0x800') if tok in text]
    print(f'{p}: metadata guard ' + ('ok' if not bad else 'bad ' + ','.join(bad)))
    if bad:
        raise SystemExit(1)
PY
git diff --cached --name-only | python3 -c 'import sys; bad=[p.strip() for p in sys.stdin if p.strip().startswith(("build/",)) or p.strip().endswith((".BIN", ".CUE", ".OBJ", ".WAD"))]; print("asset guard ok" if not bad else "blocked: "+", ".join(bad)); sys.exit(1 if bad else 0)'
```

Validation :

- RED observé : import manquant du nouveau générateur avant implémentation.
- Tests ciblés : `9 passed`
- Suite reverse complète : `36 passed`
- Build : `Built target TombRaiderChronicles_PSXPC_N`
- Output metadata guard : no `instruction`, `word_le_hex`, `payload_offset`, `jal 0x`, or raw address token
- Asset/staging guard : `asset guard ok`

## Acceptance criteria

- [x] Le rapport couvre les save groups `4`, `5`, `8`, `10`.
- [x] Chaque ligne indique les restore groups liés, le résumé de branches RE-021, les counts de champs matchés/non résolus, les familles de prédicats source, les prédicats non prouvés et la limite de preuve.
- [x] Le verdict conserve `patch-ready groups = 0` sauf preuve champ+prédicat plus forte.
- [x] Les sorties excluent `instruction`, `word_le_hex`, `payload_offset`, `jal 0x`, adresses brutes et cibles brutes.
- [x] Aucun patch `GAME/SAVEGAME.C`.
- [x] Aucun marqueur `(F)`, `(D)` ou `(**)` n'est ajouté.

## Verdict

RE-022 ne débloque aucun patch serializer : `patch-ready groups = 0`. Les champs et prédicats bloquants sont mieux isolés, mais il manque encore une preuve source-level des payloads optionnels et des layouts restore.

## Next step

RE-023 : construire un plan d'implémentation RestoreLevelData strictement source-level à partir des blockers RE-022, sans modifier le code tant que les payload predicates et layout blockers ne sont pas prouvés.
