# Reverse engineering stories — Tomb Raider Chronicles / TOMB5

> Créé le 2026-06-14. Chaque story/ticket a obligatoirement un champ `Status` et une section de progression.

## Baseline vérifiée

- Repo : `/var/www/projects/TOMB5`
- Image disque préparée dans le repo : `TOMB5.BIN` + `TOMB5.CUE`
- Version de référence attendue par le repo : `PSX NTSC v1.0 SLUS_013.11`
- MD5 attendu repo pour `SLUS_013.11` : `4EF523E708D7A7D6571F39C6E47784F9`
- MD5 vérifié de l'exécutable extrait : `4ef523e708d7a7d6571f39c6e47784f9`
- `SYSTEM.CNF` vérifié : `BOOT=cdrom:\SLUS_013.11;1`
- Ghidra headless : import direct PS-X EXE non supporté ici, import du payload brut MIPS LE OK à `0x80010000`.

## Statuts utilisés

- `Todo` : pas commencé.
- `In progress` : travail commencé, livrable incomplet.
- `Blocked` : dépend d'un outil, d'une décision ou d'une info manquante.
- `Done` : terminé et vérifié.

## Milestones

- [Niveau 1 — Reverse exploitable](MILESTONE-level-1-reverse-exploitable.md) — Status: `Done`

## Tickets

- [RE-000 — Baseline disque, Ghidra et repo](RE-000-baseline-disque-ghidra-repo.md) — Status: `Done`
- [RE-001 — Rendre le workflow Ghidra reproductible](RE-001-ghidra-workflow-reproductible.md) — Status: `Done`
- [RE-002 — Exporter les fonctions Ghidra et les rapprocher du repo](RE-002-export-fonctions-ghidra-et-mapping-repo.md) — Status: `Done`
- [RE-003 — Cartographier la progression de décompilation par module](RE-003-cartographie-progression-decompilation.md) — Status: `Done`
- [RE-004 — Prioriser les fonctions non finalisées](RE-004-priorisation-fonctions-non-finalisees.md) — Status: `Done`
- [RE-005 — Valider le build PSXPC_N avec image disque](RE-005-build-psxpcn-disc-version.md) — Status: `Done`
- [RE-006 — Extraire et documenter GAMEWAD/CODEWAD/assets](RE-006-assets-gamewad-codewad.md) — Status: `Done`
- [RE-007 — Mettre en place comparaison binaire/désassemblage](RE-007-comparaison-binaire-disassembly.md) — Status: `Done`
- [RE-008 — Documenter conventions de reverse PS1/TR5](RE-008-conventions-reverse-ps1-tr5.md) — Status: `Done`
- [RE-009 — Auditer SaveLevelData / RestoreLevelData](RE-009-savegame-level-data-audit.md) — Status: `Done`
- [RE-010 — Préparer le schéma de reconstruction SaveLevelData / RestoreLevelData](RE-010-savegame-stream-schema.md) — Status: `Done`
- [RE-011 — Implémenter la branche PSX SaveLevelData depuis le schéma](RE-011-saveleveldata-psx-implementation.md) — Status: `Done`
- [RE-012 — Auditer SaveLevelData contre le dump original](RE-012-saveleveldata-original-audit.md) — Status: `Done`
- [RE-013 — Mapper les groupes d'appels WriteSG de SaveLevelData](RE-013-saveleveldata-write-call-map.md) — Status: `Done`
- [RE-014 — Auditer les flags item de SaveLevelData](RE-014-saveleveldata-item-flag-audit.md) — Status: `Done`
- [RE-015 — Reconstruire la sérialisation active item de SaveLevelData](RE-015-saveleveldata-active-item-serialization.md) — Status: `Done`
- [RE-016 — Prouver le contrôle-flow item de SaveLevelData](RE-016-saveleveldata-item-control-flow-proof.md) — Status: `Done`
- [RE-017 — Réconcilier les champs/largeurs item SaveLevelData](RE-017-saveleveldata-item-field-width-reconciliation.md) — Status: `Done`
- [RE-018 — Vérifier les hypothèses item SaveLevelData côté RestoreLevelData](RE-018-saveleveldata-restore-side-field-proof.md) — Status: `Done`
- [RE-019 — Mapper les appels ReadSG originaux de RestoreLevelData](RE-019-restoreleveldata-read-call-map.md) — Status: `Done`
- [RE-020 — Dériver une preuve RestoreLevelData field/control-flow](RE-020-restoreleveldata-field-control-flow-proof.md) — Status: `Done`
- [RE-021 — Mapper les prédicats/branches RestoreLevelData](RE-021-restoreleveldata-branch-predicate-map.md) — Status: `Done`
- [RE-022 — Réconcilier champs et prédicats RestoreLevelData](RE-022-restoreleveldata-field-predicate-reconciliation.md) — Status: `Done`
- [RE-023 — Planifier l'implémentation RestoreLevelData depuis les blockers RE-022](RE-023-restoreleveldata-implementation-plan.md) — Status: `Done`
- [RE-024 — Prouver les prédicats RestoreLevelData room/split](RE-024-restoreleveldata-room-split-predicate-proof.md) — Status: `Done`
- [RE-025 — Prouver les payload predicates RestoreLevelData du save group 5](RE-025-restoreleveldata-group5-payload-predicate-proof.md) — Status: `Done`
- [RE-026 — Prouver le fanout subtype/layout RestoreLevelData du save group 8](RE-026-restoreleveldata-group8-layout-fanout-proof.md) — Status: `Done`
- [RE-027 — Rafraîchir le plan de readiness RestoreLevelData](RE-027-restoreleveldata-readiness-refresh.md) — Status: `Done`
- [RE-028 — Checklist source-field identity RestoreLevelData group 5](RE-028-restoreleveldata-group5-source-field-identity-checklist.md) — Status: `Done`

## Snapshot assets disque / GAMEWAD

Source : `docs/reverse/assets-inventory.md`, `docs/reverse/generated/disc-files.txt`, `docs/reverse/generated/gamewad-files.txt`, générés par :

```bash
python3 scripts/reverse/assets_inventory.py
```

Résumé actuel :

- fichiers disque listés : `30`
- `GAMEWAD.OBJ` : `55355392` octets
- entrées GAMEWAD : `51` (`30` non vides, `21` réservées vides)
- entrées niveau avec segment `CODE.WAD` embarqué détecté : `15`
- assets lourds extraits uniquement sous `build/reverse/re006/` (non versionné)

## Snapshot de progression généré

Source : `docs/reverse/progress.md` et `docs/reverse/generated/progress.json`, générés par :

```bash
python3 scripts/reverse/progress_report.py
```

Résumé actuel depuis le mapping Ghidra ↔ repo :

- fonctions repo suivies : `1250`
- modules : `5`
- fichiers : `138`
- mappées Ghidra : `866` (`69.28%`)
- final/debug/binary-matched : `925` (`74.0%`)
- `(ND)` : `23`

## Snapshot de progression repo

Analyse rapide des commentaires de fonctions dans `GAME`, `SPEC_PSX`, `SPEC_PSXPC_N`, `EMULATOR`, `TOOLS` :

- fonctions/commentaires détectés : `1869`
- marquées `(F)` : `1082`
- marquées `(D)` : `83`
- marquées `(ND)` : `23`

Par dossier :

- `GAME` : total `1149`, `(F)` `736`, `(D)` `5`, `(ND)` `4`
- `SPEC_PSXPC_N` : total `313`, `(F)` `189`, `(D)` `41`, `(ND)` `12`
- `SPEC_PSX` : total `95`, `(F)` `68`, `(D)` `37`, `(ND)` `7`
- `EMULATOR` : total `97`, `(F)` `21`
- `SPEC_PSXPC` : total `213`, `(F)` `68`
- `TOOLS` : total `2`

Note : ce snapshot est un indicateur heuristique basé sur les marqueurs du repo, pas une preuve d'équivalence binaire.
