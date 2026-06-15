# RE-020 — Dériver une preuve RestoreLevelData field/control-flow

Status: Done
Owner: Hermes
Priority: P0
Type: Reverse audit

## Goal

Produire une preuve metadata-only plus forte que RE-019 pour rapprocher les groupes item SaveLevelData RE-017 des régions originales RestoreLevelData, en distinguant les ancres payload rares, les splits de control-flow et les limites de patch.

## Context

RE-019 a montré que la comparaison size-only exacte ne débloque aucun patch serializer. Les groupes item `4`, `5`, `8` et `10` restent prioritaires : `10` a une sous-séquence restore exacte mais sans preuve de prédicat/champ, tandis que `4`, `5` et `8` ont des correspondances non exactes ou fragmentées. RE-020 transforme cette carte en table d'hypothèses restore-side plus exploitable, sans publier d'instructions originales ni modifier `GAME/SAVEGAME.C`.

## Scope

- Lire les artefacts metadata-only RE-017/RE-019.
- Produire un CSV/Markdown versionable sans instruction originale, mot machine, payload offset, dump row brute ou call opcode/target brut.
- Couvrir explicitement les groupes item prioritaires `4`, `5`, `8`, `10`.
- Classifier les preuves en `rare-payload-anchor`, `exact-size-window`, `control-flow-split-candidate`, `ambiguous-size-only` ou `missing-restore-proof`.
- Ne pas modifier `GAME/SAVEGAME.C`.
- Ne pas ajouter `(F)`, `(D)` ou `(**)`.

## Progress

- [x] Ajouter la story RE-020 avec tracker explicite.
- [x] Ajouter/faire échouer les tests RED pour l'audit restore field/control-flow.
- [x] Implémenter le générateur metadata-only RE-020.
- [x] Générer CSV/Markdown versionables.
- [x] Mettre à jour l'index stories et la documentation SaveLevelData.
- [x] Valider tests reverse.
- [x] Valider le build `TombRaiderChronicles_PSXPC_N`.
- [x] Contrôler les fichiers staged contre assets/dumps originaux et fuites metadata.
- [x] Committer et pousser.

## Result

Fichiers ajoutés :

- `scripts/reverse/restoreleveldata_field_control_flow_proof.py`
- `tests/reverse/test_restoreleveldata_field_control_flow_proof.py`
- `docs/reverse/generated/restoreleveldata-field-control-flow-proof.csv`
- `docs/reverse/functions/restoreleveldata-field-control-flow-proof.md`

Fichiers modifiés :

- `docs/reverse/functions/savegame-level-data.md`
- `docs/stories/README.md`

Métriques produites :

- groupes prioritaires couverts : `4, 5, 8, 10`
- lignes de preuve : `4`
- groupes patch-ready : `0`
- status : `restore-field-control-flow-proof-partial`

## Findings

RE-020 améliore la triage map mais ne débloque toujours aucun patch :

- Groupe `4` : régions restore candidates `4;5`; split control-flow probable, mais les champs répétés 2-byte empêchent une preuve champ/prédicat.
- Groupe `5` : ancres payload rares `24,20` retrouvées dans restore group `6`; les flags/timer/trigger séparés et les prédicats restent non prouvés.
- Groupe `8` : ancres payload rares `20,4` retrouvées dans restore group `8`; les bytes restore supplémentaires et mismatches layout bloquent l'équivalence.
- Groupe `10` : fenêtre exacte dans restore group `9`; preuve size-only exacte mais pas preuve de prédicat ni de champ.

## Commands

```bash
python3 -m pytest tests/reverse/test_restoreleveldata_field_control_flow_proof.py -q
python3 scripts/reverse/restoreleveldata_field_control_flow_proof.py
python3 -m py_compile scripts/reverse/restoreleveldata_field_control_flow_proof.py
python3 -m pytest tests/reverse/test_restoreleveldata_field_control_flow_proof.py tests/reverse/test_restoreleveldata_read_call_map.py tests/reverse/test_saveleveldata_item_field_width_audit.py -q
python3 -m pytest tests/reverse -q
cmake --build BUILD/re005-psxpcn-disc --target TombRaiderChronicles_PSXPC_N -j2
python3 - <<'PY'
from pathlib import Path
paths = [
    Path('docs/reverse/generated/restoreleveldata-field-control-flow-proof.csv'),
    Path('docs/reverse/functions/restoreleveldata-field-control-flow-proof.md'),
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
- `30 passed`
- `Built target TombRaiderChronicles_PSXPC_N`
- Output metadata guard : no `instruction`, `word_le_hex`, `payload_offset`, or raw `jal`
- Asset/staging guard : `asset guard ok`

## Acceptance criteria

- [x] Le rapport couvre les groupes `4`, `5`, `8`, `10` avec un statut de preuve restore-side explicite.
- [x] Les groupes avec payloads rares (`20`, `24`, `4`) indiquent les régions restore candidates et les limites restantes.
- [x] Le groupe `10` reste bloqué malgré la fenêtre exacte, faute de preuve champ/prédicat.
- [x] Le verdict indique explicitement `patch-ready groups = 0` sauf preuve plus forte trouvée.
- [x] Les sorties excluent `instruction`, `word_le_hex`, `payload_offset`, `jal 0x` et dump rows brutes.
- [x] Aucun marqueur `(F)`, `(D)` ou `(**)` n'est ajouté.

## Verdict

RE-020 ne débloque aucun patch serializer : `patch-ready groups = 0`. Les ancres payload rares rendent les régions restore candidates plus utiles, mais les prédicats de branche et les champs exacts restent à prouver avant toute modification de `GAME/SAVEGAME.C`.

## Next step

RE-021 : dériver une carte metadata-only des prédicats/branches autour des restore groups `4`, `5`, `6`, `8` et `9`, pour relier les fenêtres de lecture aux conditions source probables sans exposer d'instructions originales.
