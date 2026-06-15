# RestoreLevelData field/control-flow proof

Status: Generated
Story: `docs/stories/RE-020-restoreleveldata-field-control-flow-proof.md`

## Progress tracker

- [x] Load RE-017 field/width hypotheses.
- [x] Load RE-019 restore read-group size metadata.
- [x] Classify priority item groups by restore evidence strength.
- [x] Keep raw original rows, opcode text, machine words, and payload coordinates out of versioned outputs.
- [x] Preserve marker verdict limits.

## Inputs

- RE-017 field-width CSV: `docs/reverse/generated/saveleveldata-item-field-width-audit.csv`
- RE-019 restore call-map CSV: `docs/reverse/generated/restoreleveldata-read-call-map.csv`

## Summary

- priority groups covered: `4, 5, 8, 10`
- proof rows: `4`
- patch-ready groups: `0`
- status: `restore-field-control-flow-proof-partial`

## Priority group matrix

### Save original item group 4

- save call count: `17`
- save size sequence: `2,2,2,2,1,2,2,2,2,2,1,1,1,2,1,2,2`
- gap summary: `exact-field-width-match=14;source-width-mismatch=3`
- rare payload anchors: `none`
- restore group candidates: `4;5`
- restore size sequences: `restore_group=4:2,2,2,1,2,2,2,2,2; restore_group=5:1,1,1,2,1,2,2,4,2,2,2,2,2,2,2`
- proof status: `control-flow-split-candidate`
- patch readiness: `blocked`
- proof limit: restore read regions are split across candidate groups 4 and 5; repeated 2-byte fields prevent field/predicate proof.

### Save original item group 5

- save call count: `15`
- save size sequence: `4,2,2,2,2,2,2,2,24,2,2,2,2,2,20`
- gap summary: `source-missing-field=14;exact-field-width-match=1`
- rare payload anchors: `24,20`
- restore group candidates: `6`
- restore size sequences: `restore_group=6:24,2,2,2,2,2,20,1`
- proof status: `rare-payload-anchor`
- patch readiness: `blocked`
- proof limit: object payload anchors exist on restore side, but leading packed flags and separate item flag/timer/trigger payload predicates remain unproved.

### Save original item group 8

- save call count: `12`
- save size sequence: `1,20,2,2,2,4,2,2,2,2,2,2`
- gap summary: `source-missing-field=5;exact-field-width-match=5;source-layout-mismatch=2`
- rare payload anchors: `20,4`
- restore group candidates: `8`
- restore size sequences: `restore_group=8:1,1,20,2,2,2,2,4,2,2,2,2,2`
- proof status: `rare-payload-anchor`
- patch readiness: `blocked`
- proof limit: object payload anchors exist on restore side, but extra restore bytes and layout mismatches still block field equivalence.

### Save original item group 10

- save call count: `7`
- save size sequence: `2,2,2,2,2,2,1`
- gap summary: `exact-field-width-match=6;source-layout-mismatch=1`
- rare payload anchors: `none`
- restore group candidates: `9`
- restore size sequences: `restore_group=9:1,2,2,2,2,2,2,1`
- proof status: `exact-size-window`
- patch readiness: `blocked`
- proof limit: exact size window is not predicate proof; room/control-flow layout still needs restore-side field proof.

## Verdict

RE-020 improves the triage map by identifying candidate restore regions and rare payload anchors, but it still does not prove field predicates or full control-flow equivalence. Patch readiness remains `0`.

Do not add `(F)`, `(D)`, or `(**)` markers. Do not patch `GAME/SAVEGAME.C` from this evidence alone.

Next step: derive branch-predicate metadata around the candidate restore regions before any serializer source modification.
