# RE-019 — Mapper les appels ReadSG originaux de RestoreLevelData

Status: Done
Owner: Hermes
Priority: P0
Type: Reverse audit

## Goal

Extraire une call-map metadata-only de l'original `RestoreLevelData`, puis comparer les tailles/ordre de lecture restore aux hypothèses RE-017/RE-018 avant toute modification source.

## Context

RE-018 a confirmé que le source `RestoreLevelData` est `UNIMPLEMENTED()`. Les hypothèses RE-017 ne peuvent donc pas devenir des patchs serializer sans preuve restore-side originale. RE-019 lit uniquement le dump original ignoré pour dériver des métadonnées versionables: coordonnées d'appels `ReadSG`, tailles `a1`, groupes par proximité et correspondances de séquences avec les groupes item RE-017.

## Scope

- Lire `build/reverse/re007/original/RestoreLevelData_80054f6c.csv` localement, sans le versionner.
- Produire un CSV/Markdown versionable sans instruction originale, mot machine, payload offset, dump ou asset.
- Comparer les séquences de tailles restore à RE-017/RE-018 pour les groupes item prioritaires.
- Ne pas modifier `GAME/SAVEGAME.C`.
- Ne pas ajouter `(F)`, `(D)` ou `(**)`.

## Progress

- [x] Ajouter la story RE-019 avec tracker explicite.
- [x] Ajouter/faire échouer les tests RED pour la call-map restore originale.
- [x] Implémenter le générateur de call-map/comparaison restore metadata-only.
- [x] Générer CSV/Markdown versionables.
- [x] Mettre à jour l'index stories et la documentation SaveLevelData.
- [x] Valider tests reverse.
- [x] Valider le build `TombRaiderChronicles_PSXPC_N`.
- [x] Contrôler les fichiers staged contre assets/dumps originaux.
- [x] Committer et pousser.

## Result

Fichiers ajoutés:

- `scripts/reverse/restoreleveldata_read_call_map.py`
- `tests/reverse/test_restoreleveldata_read_call_map.py`
- `docs/reverse/generated/restoreleveldata-read-call-map.csv`
- `docs/reverse/functions/restoreleveldata-read-call-map.md`

Fichiers modifiés:

- `docs/reverse/functions/savegame-level-data.md`
- `docs/stories/README.md`

Métriques produites:

- appels originaux `ReadSG`: `79`
- restore read groups: `10`
- groupes item RE-017 comparés: `8`
- groupes avec match restore size-only: `4`
- groupes prêts pour patch: `0`
- status: `restore-size-proof-partial`

## Findings

RE-019 produit une preuve restore-side partielle mais insuffisante pour patcher:

- Les groupes item RE-017 `4`, `5`, `6` et `8` n'ont pas de sous-séquence restore exacte par tailles.
- Les groupes `7`, `9` et `11` ne sont que des groupes single-byte; ils correspondent à trop d'emplacements restore pour identifier un champ ou un prédicat.
- Le groupe `10` a une sous-séquence exacte dans le groupe restore `9`, mais la taille seule ne prouve ni les champs ni les branches.
- Aucun groupe n'est `patch-ready`; `GAME/SAVEGAME.C` reste inchangé.

## Commands

```bash
python3 -m pytest tests/reverse/test_restoreleveldata_read_call_map.py -q
python3 scripts/reverse/restoreleveldata_read_call_map.py
python3 -m py_compile scripts/reverse/restoreleveldata_read_call_map.py
python3 -m pytest tests/reverse/test_restoreleveldata_read_call_map.py tests/reverse/test_saveleveldata_restore_side_audit.py -q
python3 -m pytest tests/reverse -q
cmake --build BUILD/re005-psxpcn-disc --target TombRaiderChronicles_PSXPC_N -j2
python3 - <<'PY'
from pathlib import Path
for p in [Path('docs/reverse/generated/restoreleveldata-read-call-map.csv'), Path('docs/reverse/functions/restoreleveldata-read-call-map.md')]:
    text = p.read_text(encoding='utf-8')
    bad = [tok for tok in ('instruction', 'word_le_hex', 'payload_offset', 'jal 0x') if tok in text]
    print(f'{p}: metadata guard ' + ('ok' if not bad else 'bad ' + ','.join(bad)))
    if bad:
        raise SystemExit(1)
PY
git diff --cached --name-only | python3 -c 'import sys; bad=[p.strip() for p in sys.stdin if p.strip().startswith(("build/",)) or p.strip().endswith((".BIN", ".CUE", ".OBJ", ".WAD"))]; print("asset guard ok" if not bad else "blocked: "+", ".join(bad)); sys.exit(1 if bad else 0)'
```

Validation:

- `27 passed`
- `Built target TombRaiderChronicles_PSXPC_N`
- Output metadata guard: no `instruction`, `word_le_hex`, `payload_offset`, or raw `jal`
- Asset/staging guard: `asset guard ok`

## Acceptance criteria

- [x] Les appels originaux `ReadSG` de `RestoreLevelData` sont groupés en métadonnées versionables.
- [x] Les sorties incluent les séquences de tailles et excluent `instruction`, `word_le_hex`, `payload_offset` et instruction originale.
- [x] Les groupes item RE-017/RE-018 ont un statut de correspondance restore explicite.
- [x] Le verdict indique si un patch serializer est débloqué ou non.
- [x] Aucun marqueur `(F)`, `(D)` ou `(**)` n'est ajouté.

## Verdict

RE-019 ne débloque aucun patch serializer: `patch-ready groups = 0`. La call-map restore originale apporte une triage map utile, mais les correspondances par tailles restent insuffisantes pour prouver les champs ou les prédicats de branche.

## Next step

RE-020: dériver une preuve restore-side field/control-flow plus forte pour les régions matchées et mismatched, notamment les prédicats autour des groupes item `4`, `5`, `8` et `10`, sans modifier `GAME/SAVEGAME.C` tant que la preuve reste size-only.
