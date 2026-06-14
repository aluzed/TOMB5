# RE-012 — Auditer SaveLevelData contre le dump original

Status: Done
Owner: Hermes
Priority: P0
Type: Reverse audit

## Goal

Comparer la structure source actuelle de `SaveLevelData` avec le dump original local sans versionner d'instructions ou de bytes originaux, et produire un verdict exploitable avant toute tentative de marqueur `(F)`.

## Context

RE-011 a rendu le flux source-level `Write(...)` compilable pour PSX/PSXPC_N. Cette étape ne prouvait pas l'équivalence avec la fonction PSX originale `0x80053f10`; elle prouvait seulement que le fallback vide avait disparu. RE-012 reprend donc le dump original ignoré et en extrait uniquement des métriques versionables.

## Scope

- Lire le dump original local sous `build/reverse/re007/original/`.
- Ne pas committer le dump, les instructions, les mots machine ou les bytes originaux.
- Compter les appels originaux à `WriteSG` (`0x80053b04`).
- Compter les sites source `Write(...)` via le schéma existant.
- Documenter les limites de preuve.
- Ne pas ajouter `(F)`, `(D)` ou `(**)`.

## Progress

- [x] Régénérer/valider le dump local `SaveLevelData_80053f10.csv` sous un chemin ignoré.
- [x] Ajouter un test RED pour imposer un audit reproductible sans fuite de bytes/instructions originaux.
- [x] Implémenter `scripts/reverse/saveleveldata_original_audit.py`.
- [x] Générer `docs/reverse/functions/saveleveldata-original-audit.md`.
- [x] Mettre à jour l'index des stories.
- [x] Valider les tests Python ciblés et reverse.
- [x] Valider le build `TombRaiderChronicles_PSXPC_N`.
- [x] Contrôler les fichiers staged contre les assets lourds/originaux.

## Result

Fichiers ajoutés:

- `scripts/reverse/saveleveldata_original_audit.py`
- `tests/reverse/test_saveleveldata_original_audit.py`
- `docs/reverse/functions/saveleveldata-original-audit.md`

Fichiers modifiés:

- `docs/stories/README.md`

Métriques produites:

- instructions originales dumpées: `1047`
- appels originaux à `WriteSG`: `81`
- sites source statiques `Write(...)`: `32`
- sites source top-level: `10`
- sites source avec contexte boucle/condition: `22`
- verdict outil: `needs-control-flow-audit`

## Commands

```bash
python3 scripts/reverse/disasm_extract.py SaveLevelData
python3 -m pytest tests/reverse/test_saveleveldata_original_audit.py -q
python3 scripts/reverse/saveleveldata_original_audit.py
python3 -m pytest tests/reverse -q
cmake --build BUILD/re005-psxpcn-disc --target TombRaiderChronicles_PSXPC_N -j2
```

## Acceptance criteria

- [x] Le rapport versionné ne contient pas les instructions originales.
- [x] Le rapport versionné ne contient pas les mots machine originaux.
- [x] Le rapport donne un compteur original `WriteSG` et un compteur source `Write(...)`.
- [x] Le rapport explique pourquoi l'écart `81` vs `32` n'est pas une preuve d'échec mais impose un audit de contrôle de flux.
- [x] Aucun marqueur `(F)`, `(D)` ou `(**)` n'est ajouté.

## Verdict

`SaveLevelData` reste **non marquable** en `(F)`, `(D)` ou `(**)` à ce stade.

La source actuelle est une hypothèse structurée et compilable, mais il faut encore associer les `81` appels originaux à `WriteSG` aux `32` sites source statiques en tenant compte des boucles, conditions et chemins `FullSave`.

## Next step

Créer une story de contrôle-flow mapping pour `SaveLevelData`: produire une table versionable qui rapproche chaque groupe d'appels originaux `WriteSG` d'un site source ou d'une boucle source, sans committer les instructions originales.
