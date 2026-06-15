# RE-023 — Planifier l'implémentation RestoreLevelData depuis les blockers RE-022

Status: Done
Owner: Hermes
Priority: P0
Type: Reverse planning

## Goal

Construire un plan d'implémentation `RestoreLevelData` strictement source-level à partir des blockers RE-022, sans modifier le serializer tant que les payload predicates et layout blockers ne sont pas prouvés.

## Context

RE-022 a réconcilié les champs et prédicats restore connus mais conserve `patch-ready groups = 0`. RE-023 transforme cette matrice en ordre d'exécution et en tickets de preuve, afin d'éviter de coder `RestoreLevelData` depuis des hypothèses encore faibles.

## Scope

- Consommer uniquement le CSV metadata-only RE-022 : `docs/reverse/generated/restoreleveldata-field-predicate-reconciliation.csv`.
- Couvrir les save groups prioritaires `4`, `5`, `8`, `10`.
- Produire un plan avec phase d'implémentation, preuve manquante, action sûre minimale, ticket recommandé, risque et readiness.
- Ne pas lire ni publier de dump brut, mot machine, coordonnée de payload, cible brute de branche/call ou adresse originale.
- Ne pas modifier `GAME/SAVEGAME.C`.
- Ne pas ajouter `(F)`, `(D)` ou `(**)`.

## Progress

- [x] Ajouter la story RE-023 avec tracker explicite.
- [x] Ajouter/faire échouer les tests RED du générateur de plan.
- [x] Implémenter le générateur metadata-only RE-023.
- [x] Générer CSV/Markdown versionables.
- [x] Mettre à jour l'index stories et la documentation SaveLevelData.
- [x] Valider les tests ciblés puis la suite reverse.
- [x] Valider le build `TombRaiderChronicles_PSXPC_N`.
- [x] Contrôler les fichiers staged contre assets/dumps originaux et fuites metadata.
- [x] Committer et pousser.

## Result

Fichiers ajoutés :

- `scripts/reverse/restoreleveldata_implementation_plan.py`
- `tests/reverse/test_restoreleveldata_implementation_plan.py`
- `docs/reverse/generated/restoreleveldata-implementation-plan.csv`
- `docs/reverse/functions/restoreleveldata-implementation-plan.md`

Fichiers modifiés :

- `docs/reverse/functions/savegame-level-data.md`
- `docs/stories/README.md`

Métriques produites :

- save groups couverts : `4, 5, 8, 10`
- lignes de plan : `4`
- patch-ready groups : `0`
- code-change-ready groups : `0`
- status : `restoreleveldata-implementation-plan-blocked`

## Findings

RE-023 confirme que l'étape suivante doit rester proof-first :

- Save group `10` → restore group `9` : plus petit blocker set ; candidat prioritaire RE-024 pour prouver le room/layout predicate.
- Save group `4` → restore groups `4;5` : à coupler avec RE-024 pour prouver le split active item / anim-state avant tout patch.
- Save group `5` → restore group `6` : reste bloqué sur les payloads item flags, timer, trigger et object extension ; candidat RE-025.
- Save group `8` → restore group `8` : reste bloqué sur subtype/layout fanout et extra restore bytes ; candidat RE-026.

## Commands

```bash
python3 -m pytest tests/reverse/test_restoreleveldata_implementation_plan.py -q
python3 scripts/reverse/restoreleveldata_implementation_plan.py
python3 -m py_compile scripts/reverse/restoreleveldata_implementation_plan.py
python3 -m pytest tests/reverse/test_restoreleveldata_implementation_plan.py tests/reverse/test_restoreleveldata_field_predicate_reconciliation.py -q
python3 -m pytest tests/reverse -q
cmake --build BUILD/re005-psxpcn-disc --target TombRaiderChronicles_PSXPC_N -j2
```

Validation metadata recommandée avant commit :

```bash
python3 - <<'PY'
from pathlib import Path
paths = [
    Path('docs/reverse/generated/restoreleveldata-implementation-plan.csv'),
    Path('docs/reverse/functions/restoreleveldata-implementation-plan.md'),
]
for p in paths:
    text = p.read_text(encoding='utf-8')
    bad = [tok for tok in ('word_le_hex', 'payload_offset', 'jal 0x', '0x800') if tok in text]
    print(f'{p}: metadata guard ' + ('ok' if not bad else 'bad ' + ','.join(bad)))
    if bad:
        raise SystemExit(1)
PY
git diff --cached --name-only | python3 -c 'import sys; bad=[p.strip() for p in sys.stdin if p.strip().startswith(("build/",)) or p.strip().endswith((".BIN", ".CUE", ".OBJ", ".WAD"))]; print("asset guard ok" if not bad else "blocked: "+", ".join(bad)); sys.exit(1 if bad else 0)'
```

## Acceptance criteria

- [x] Le rapport couvre les save groups `4`, `5`, `8`, `10`.
- [x] Chaque ligne indique restore groups, phase, preuve manquante, action sûre minimale, readiness, ticket recommandé et risque.
- [x] Le verdict conserve `patch-ready groups = 0` et `code-change-ready groups = 0`.
- [x] Les sorties excluent mots machine, coordonnées payload, adresses brutes et cibles brutes.
- [x] Aucun patch `GAME/SAVEGAME.C`.
- [x] Aucun marqueur `(F)`, `(D)` ou `(**)` n'est ajouté.

## Verdict

RE-023 est un plan, pas un patch d'implémentation. Tous les groupes restent bloqués pour changement de code.

## Next step

RE-024 : prouver le room/layout predicate du save group `10` et le split active item predicate du save group `4`, en restant metadata-only jusqu'à preuve suffisante.
