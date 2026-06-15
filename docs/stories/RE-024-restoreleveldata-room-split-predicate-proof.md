# RE-024 — Prouver les prédicats RestoreLevelData room/split

Status: Done
Owner: Hermes
Priority: P0
Type: Reverse proof audit

## Goal

Prouver ou bloquer explicitement les deux axes RE-024 issus de RE-023 : le room/layout predicate du save group `10` et le split active item predicate du save group `4`, en restant metadata-only et sans patcher `GAME/SAVEGAME.C`.

## Context

RE-023 a identifié RE-024 comme première étape proof-first avant toute implémentation `RestoreLevelData`. Les groupes ciblés sont :

- save group `10` → restore group `9`, plus petit blocker set mais room/layout predicate non prouvé ;
- save group `4` → restore groups `4;5`, split active-item et anim-state width predicate non prouvés.

## Scope

- Consommer uniquement des CSV metadata-only déjà versionnés : RE-017, RE-020, RE-021, RE-022 et RE-023.
- Produire une matrice de preuve pour les save groups `10` et `4`.
- Publier field-width profile, restore shape, branch profile, blocking predicates, hypothèse source-safe, verdict et next action.
- Ne pas lire ni publier de dump brut, mot machine, coordonnée de payload, cible brute de branche/call ou adresse originale.
- Ne pas modifier `GAME/SAVEGAME.C`.
- Ne pas ajouter `(F)`, `(D)` ou `(**)`.

## Progress

- [x] Ajouter la story RE-024 avec tracker explicite.
- [x] Ajouter/faire échouer les tests RED du générateur RE-024.
- [x] Implémenter le générateur metadata-only RE-024.
- [x] Générer CSV/Markdown versionables.
- [x] Mettre à jour l'index stories et la documentation SaveLevelData.
- [x] Valider les tests ciblés puis la suite reverse.
- [x] Valider le build `TombRaiderChronicles_PSXPC_N`.
- [x] Contrôler les fichiers staged contre assets/dumps originaux et fuites metadata.
- [x] Committer et pousser.

## Result

Fichiers ajoutés :

- `scripts/reverse/restoreleveldata_room_split_predicate_proof.py`
- `tests/reverse/test_restoreleveldata_room_split_predicate_proof.py`
- `docs/reverse/generated/restoreleveldata-room-split-predicate-proof.csv`
- `docs/reverse/functions/restoreleveldata-room-split-predicate-proof.md`

Fichiers modifiés :

- `docs/reverse/functions/savegame-level-data.md`
- `docs/stories/README.md`

Métriques produites :

- target save groups : `10, 4`
- proof rows : `2`
- code-change-ready groups : `0`
- status : `restoreleveldata-room-split-proof-partial`

## Findings

RE-024 a resserré les blockers mais ne débloque toujours aucun patch source :

- Save group `10` : `6` exact field-width matches et `1` source-layout mismatch ; restore shape `exact-size-window`, mais le room byte order/layout predicate reste non prouvé.
- Save group `4` : `14` exact field-width matches et `3` source-width mismatches ; restore shape `control-flow-split-candidate`, mais le split restore groups `4;5` et les anim-state byte-vs-word predicates restent non prouvés.

## Commands

```bash
python3 -m pytest tests/reverse/test_restoreleveldata_room_split_predicate_proof.py -q
python3 scripts/reverse/restoreleveldata_room_split_predicate_proof.py
python3 -m py_compile scripts/reverse/restoreleveldata_room_split_predicate_proof.py
python3 -m pytest tests/reverse/test_restoreleveldata_room_split_predicate_proof.py tests/reverse/test_restoreleveldata_implementation_plan.py -q
python3 -m pytest tests/reverse -q
cmake --build BUILD/re005-psxpcn-disc --target TombRaiderChronicles_PSXPC_N -j2
```

Validation metadata recommandée avant commit :

```bash
python3 - <<'PY'
from pathlib import Path
paths = [
    Path('docs/reverse/generated/restoreleveldata-room-split-predicate-proof.csv'),
    Path('docs/reverse/functions/restoreleveldata-room-split-predicate-proof.md'),
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

- [x] Le rapport couvre les save groups `10` et `4`.
- [x] Chaque ligne indique restore groups, proof focus, field-width profile, restore shape, branch profile, blockers, verdict et action suivante.
- [x] Le verdict conserve `code-change-ready groups = 0`.
- [x] Les sorties excluent mots machine, coordonnées payload, adresses brutes et cibles brutes.
- [x] Aucun patch `GAME/SAVEGAME.C`.
- [x] Aucun marqueur `(F)`, `(D)` ou `(**)` n'est ajouté.

## Verdict

RE-024 est une preuve partielle : les blockers sont plus nets, mais aucun groupe n'est prêt pour une modification source.

## Next step

RE-025 : prouver les payload predicates du save group `5` — item flags, timer, trigger et object extension — tout en conservant les blockers RE-024 visibles.
