# RestoreLevelData branch/predicate map

Status: Generated
Story: `docs/stories/RE-021-restoreleveldata-branch-predicate-map.md`

## Progress tracker

- [x] Load RE-019 restore read-group metadata.
- [x] Load RE-020 candidate restore/save links.
- [x] Count nearby branch classes in relative zones only.
- [x] Assign conservative predicate hypotheses and proof limits.
- [x] Keep raw opcode text, machine words, payload coordinates, and branch/call targets out of versioned outputs.
- [x] Preserve marker verdict limits.

## Inputs

- Original dump CSV: `build/reverse/re007/original/RestoreLevelData_80054f6c.csv` (ignored; not versioned)
- RE-019 restore call-map CSV: `docs/reverse/generated/restoreleveldata-read-call-map.csv`
- RE-020 field/control-flow CSV: `docs/reverse/generated/restoreleveldata-field-control-flow-proof.csv`
- Branch scan window: `16` rows around each read-call range

## Summary

- restore groups covered: `4, 5, 6, 8, 9`
- proof rows: `5`
- patch-ready groups: `0`
- status: `restore-branch-predicate-map-partial`

## Branch/predicate matrix

### Restore group 4

- linked save groups: `4`
- read call count: `9`
- size sequence: `2,2,2,1,2,2,2,2,2`
- branch window: `call-range±16`
- branch summary: `before:conditional-compare=2;before:unconditional-jump=1;inside:conditional-compare=4;inside:unconditional-jump=3;after:conditional-compare=2;after:unconditional-jump=1`
- branch total: `13`
- nearest branch zone: `inside`
- predicate hypothesis: `active-item-header-and-animation-split`
- confidence: `medium`
- proof status: `split-branch-candidate`
- patch readiness: `blocked`
- proof limit: branch-rich region aligns with save group 4 but repeated small fields prevent predicate identity.

### Restore group 5

- linked save groups: `4`
- read call count: `15`
- size sequence: `1,1,1,2,1,2,2,4,2,2,2,2,2,2,2`
- branch window: `call-range±16`
- branch summary: `before:conditional-compare=1;inside:conditional-compare=11;inside:unconditional-jump=7;after:conditional-compare=2`
- branch total: `21`
- nearest branch zone: `inside`
- predicate hypothesis: `active-item-optional-payload-fanout`
- confidence: `medium`
- proof status: `branch-fanout-candidate`
- patch readiness: `blocked`
- proof limit: branch fanout suggests optional active-item payloads but field predicates are not individually proven.

### Restore group 6

- linked save groups: `5`
- read call count: `8`
- size sequence: `24,2,2,2,2,2,20,1`
- branch window: `call-range±16`
- branch summary: `before:conditional-compare=1;before:conditional-sign=1;inside:conditional-sign=1`
- branch total: `3`
- nearest branch zone: `inside`
- predicate hypothesis: `object-payload-anchor-compact-branch`
- confidence: `medium`
- proof status: `rare-anchor-branch-candidate`
- patch readiness: `blocked`
- proof limit: rare object payload anchors sit in a compact branch envelope but source predicates are still unknown.

### Restore group 8

- linked save groups: `8`
- read call count: `13`
- size sequence: `1,1,20,2,2,2,2,4,2,2,2,2,2`
- branch window: `call-range±16`
- branch summary: `before:conditional-compare=3;inside:conditional-compare=9;inside:unconditional-jump=5;after:conditional-compare=2;after:unconditional-jump=1`
- branch total: `20`
- nearest branch zone: `inside`
- predicate hypothesis: `object-subtype-layout-fanout`
- confidence: `medium`
- proof status: `branch-fanout-candidate`
- patch readiness: `blocked`
- proof limit: object/layout payload anchors sit inside branch fanout with extra restore bytes and unresolved field identity.

### Restore group 9

- linked save groups: `10`
- read call count: `8`
- size sequence: `1,2,2,2,2,2,2,1`
- branch window: `call-range±16`
- branch summary: `before:conditional-compare=1;before:unconditional-jump=1;inside:conditional-compare=2;after:conditional-compare=2`
- branch total: `6`
- nearest branch zone: `inside`
- predicate hypothesis: `exact-window-room-sentinel-candidate`
- confidence: `low`
- proof status: `exact-window-needs-predicate-proof`
- patch readiness: `blocked`
- proof limit: exact read-size window still lacks field predicate identity.

## Verdict

RE-021 identifies branch-rich candidate regions and compact rare-anchor regions, but it still does not prove exact field predicates. Patch readiness remains `0`.

Do not add `(F)`, `(D)`, or `(**)` markers. Do not patch `GAME/SAVEGAME.C` from this evidence alone.

Next step: reconcile branch-region hypotheses with source field identities and optional payload predicates before any serializer modification.
