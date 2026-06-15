# RE-021 — Mapper les prédicats/branches RestoreLevelData

Status: Done
Owner: Hermes
Priority: P0
Type: Reverse audit

## Goal

Dériver une carte metadata-only des prédicats et branches autour des restore groups candidats identifiés par RE-020, afin de relier les fenêtres `ReadSG` à des hypothèses de control-flow sans exposer d'instructions originales.

## Context

RE-020 a amélioré la triage map mais `patch-ready groups = 0`. Les restore groups `4`, `5`, `6`, `8` et `9` sont les prochaines zones utiles : ils contiennent soit les régions split candidates du groupe save `4`, soit les ancres rares des groupes save `5`/`8`, soit la fenêtre exacte du groupe save `10`.

## Scope

- Lire localement le dump original ignoré `RestoreLevelData_80054f6c.csv` uniquement pour dériver des métriques de branches.
- Publier seulement des métadonnées sûres : counts de branches, zones relatives, classes de branches, hypothèses de prédicat, confiance et limites.
- Ne pas publier d'instruction originale, mot machine, payload offset, dump row brute ou cible brute de branche/call.
- Couvrir les restore groups `4`, `5`, `6`, `8`, `9`.
- Ne pas modifier `GAME/SAVEGAME.C`.
- Ne pas ajouter `(F)`, `(D)` ou `(**)`.

## Progress

- [x] Ajouter la story RE-021 avec tracker explicite.
- [x] Ajouter/faire échouer les tests RED pour la branch/predicate map.
- [x] Implémenter le générateur metadata-only RE-021.
- [x] Générer CSV/Markdown versionables.
- [x] Mettre à jour l'index stories et la documentation SaveLevelData.
- [x] Valider tests reverse.
- [x] Valider le build `TombRaiderChronicles_PSXPC_N`.
- [x] Contrôler les fichiers staged contre assets/dumps originaux et fuites metadata.
- [x] Committer et pousser.

## Result

Fichiers ajoutés :

- `scripts/reverse/restoreleveldata_branch_predicate_map.py`
- `tests/reverse/test_restoreleveldata_branch_predicate_map.py`
- `docs/reverse/generated/restoreleveldata-branch-predicate-map.csv`
- `docs/reverse/functions/restoreleveldata-branch-predicate-map.md`

Fichiers modifiés :

- `docs/reverse/functions/savegame-level-data.md`
- `docs/stories/README.md`

Métriques produites :

- restore groups couverts : `4, 5, 6, 8, 9`
- lignes de preuve : `5`
- groupes patch-ready : `0`
- status : `restore-branch-predicate-map-partial`

## Findings

RE-021 améliore la carte des prédicats mais ne débloque toujours aucun patch :

- Restore group `4` → save group `4` : région branch-rich liée au header/animation split actif, mais les petits champs répétés empêchent une identité de prédicat.
- Restore group `5` → save group `4` : fanout de payload optionnel actif, mais les prédicats de champs ne sont pas individuellement prouvés.
- Restore group `6` → save group `5` : ancres object payload rares dans une enveloppe de branches compacte, mais prédicats source inconnus.
- Restore group `8` → save group `8` : fanout object subtype/layout, avec bytes restore supplémentaires et identité champ non résolue.
- Restore group `9` → save group `10` : fenêtre exacte, mais toujours sans preuve de prédicat/champ.

## Commands

```bash
python3 -m pytest tests/reverse/test_restoreleveldata_branch_predicate_map.py -q
python3 scripts/reverse/restoreleveldata_branch_predicate_map.py
python3 -m py_compile scripts/reverse/restoreleveldata_branch_predicate_map.py
python3 -m pytest tests/reverse/test_restoreleveldata_branch_predicate_map.py tests/reverse/test_restoreleveldata_field_control_flow_proof.py tests/reverse/test_restoreleveldata_read_call_map.py -q
python3 -m pytest tests/reverse -q
cmake --build BUILD/re005-psxpcn-disc --target TombRaiderChronicles_PSXPC_N -j2
python3 - <<'PY'
from pathlib import Path
paths = [
    Path('docs/reverse/generated/restoreleveldata-branch-predicate-map.csv'),
    Path('docs/reverse/functions/restoreleveldata-branch-predicate-map.md'),
]
for p in paths:
    text = p.read_text(encoding='utf-8')
    bad = [tok for tok in ('instruction', 'word_le_hex', 'payload_offset', 'jal 0x') if tok in text]
    print(f'{p}: metadata guard ' + ('ok' if not bad else 'bad ' + ','.join(bad)))
    if bad:
        raise SystemExit(1)
PY
git diff --cached --name-only | python3 -c 'import sys; bad=[p.strip() for p in sys.stdin if p.strip().startswith(("build/",)) or p.strip().endswith((".BIN", ".CUE", ".OBJ", ".WAD"))]; print("asset guard ok" if not bad else "blocked: "+", ".join(bad)); sys.exit(1 if bad else 0)'
```

Validation :

- RED observé : import manquant du nouveau générateur avant implémentation.
- `33 passed`
- `Built target TombRaiderChronicles_PSXPC_N`
- Output metadata guard : no `instruction`, `word_le_hex`, `payload_offset`, or raw `jal`
- Asset/staging guard : `asset guard ok`

## Acceptance criteria

- [x] Le rapport couvre les restore groups `4`, `5`, `6`, `8`, `9`.
- [x] Chaque ligne indique les save groups liés, la séquence de tailles restore, un résumé de branches par zone relative, une hypothèse de prédicat, un niveau de confiance et une limite de preuve.
- [x] Le verdict conserve `patch-ready groups = 0` sauf preuve champ+prédicat plus forte.
- [x] Les sorties excluent `instruction`, `word_le_hex`, `payload_offset`, `jal 0x` et les cibles brutes.
- [x] Aucun marqueur `(F)`, `(D)` ou `(**)` n'est ajouté.

## Verdict

RE-021 ne débloque aucun patch serializer : `patch-ready groups = 0`. Les formes de branches rendent les zones candidates plus lisibles, mais elles ne prouvent pas encore l'identité exacte des champs ni les prédicats optionnels.

## Next step

RE-022 : réconcilier les hypothèses de régions de branches avec les identités de champs source et les prédicats de payload optionnels, notamment flags/timer/trigger/object payload et room/layout.
