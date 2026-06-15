# RestoreLevelData group 8 layout/fanout proof

Status: Generated
Story: `docs/stories/RE-026-restoreleveldata-group8-layout-fanout-proof.md`

## Progress tracker

- [x] Load RE-023 implementation plan metadata.
- [x] Load RE-022 save group `8` field/predicate blockers.
- [x] Load RE-017 field-width rows for subtype, layout block, room/rotation, item data, item flags, speed/fallspeed, and anim-state payloads.
- [x] Load RE-020/RE-021 restore group `8` payload anchor and branch-fanout summaries.
- [x] Carry forward the RE-025 group `5` item-flag payload dependency.
- [x] Keep code-change readiness blocked and raw original details out of versioned outputs.

## Inputs

- RE-023 plan CSV: `docs/reverse/generated/restoreleveldata-implementation-plan.csv`
- RE-022 reconciliation CSV: `docs/reverse/generated/restoreleveldata-field-predicate-reconciliation.csv`
- RE-017 field-width CSV: `docs/reverse/generated/saveleveldata-item-field-width-audit.csv`
- RE-020 control-flow CSV: `docs/reverse/generated/restoreleveldata-field-control-flow-proof.csv`
- RE-021 branch predicate CSV: `docs/reverse/generated/restoreleveldata-branch-predicate-map.csv`
- RE-025 group 5 payload CSV: `docs/reverse/generated/restoreleveldata-group5-payload-predicate-proof.csv`

## Summary

- target save group: `8`
- restore group: `8`
- fanout rows: `7`
- code-change-ready fanout families: `0`
- status: `restoreleveldata-group8-layout-fanout-proof-blocked`

## Layout/fanout predicate matrix

### subtype-extra-byte

- save original group: `8`
- restore group: `8`
- save payload profile: `source-missing-field=1;bytes=1`
- restore layout profile: `rare-payload-anchor;restore-size-sequence=1,1,20,2,2,2,2,4,2,2,2,2,2;extra-restore-byte-candidate=1`
- source predicate profile: `no current source predicate for subtype byte or the extra restore byte candidate`
- branch profile: `restore_group=8:object-subtype-layout-fanout/branch-fanout-candidate/branch_total=20`
- prior group 5 dependency: `none`
- blocking predicates: `subtype byte plus extra restore byte candidate are branch/fanout clues, not source field identity`
- proof verdict: `subtype-and-extra-byte-predicate-unproven`
- next action: `prove subtype dispatch and explain the extra restore byte as source field or rebuilt state before patching`
- code change readiness: `blocked`
- recommended next ticket: `RE-027`

### position-layout-block

- save original group: `8`
- restore group: `8`
- save payload profile: `source-layout-mismatch=1;bytes=20`
- restore layout profile: `rare-payload-anchor;restore-size-sequence=1,1,20,2,2,2,2,4,2,2,2,2,2;extra-restore-byte-candidate=1`
- source predicate profile: `current source uses split position writes, not a proved twenty-byte block`
- branch profile: `restore_group=8:object-subtype-layout-fanout/branch-fanout-candidate/branch_total=20`
- prior group 5 dependency: `none`
- blocking predicates: `twenty-byte layout block conflicts with current split position representation`
- proof verdict: `layout-block-predicate-unproven`
- next action: `split the twenty-byte block into source fields or prove it is an object-specific payload body`
- code change readiness: `blocked`
- recommended next ticket: `RE-027`

### room-rotation-ordering

- save original group: `8`
- restore group: `8`
- save payload profile: `source-layout-mismatch=1;bytes=2`
- restore layout profile: `rare-payload-anchor;restore-size-sequence=1,1,20,2,2,2,2,4,2,2,2,2,2;extra-restore-byte-candidate=1`
- source predicate profile: `current source room byte and rotation ordering does not match this compact payload shape`
- branch profile: `restore_group=8:object-subtype-layout-fanout/branch-fanout-candidate/branch_total=20`
- prior group 5 dependency: `none`
- blocking predicates: `room/rotation payload ordering remains unresolved inside the fanout branch`
- proof verdict: `room-rotation-ordering-unproven`
- next action: `prove room/rotation field order for this subtype branch before source edits`
- code change readiness: `blocked`
- recommended next ticket: `RE-027`

### speed-fallspeed

- save original group: `8`
- restore group: `8`
- save payload profile: `exact-field-width-match=2;bytes=4`
- restore layout profile: `rare-payload-anchor;restore-size-sequence=1,1,20,2,2,2,2,4,2,2,2,2,2;extra-restore-byte-candidate=1`
- source predicate profile: `speed and fallspeed widths are source-visible`
- branch profile: `restore_group=8:object-subtype-layout-fanout/branch-fanout-candidate/branch_total=20`
- prior group 5 dependency: `none`
- blocking predicates: `field widths match but subtype fanout and surrounding layout are still not predicate proof`
- proof verdict: `field-width-match-fanout-still-blocked`
- next action: `keep as matched subfields while proving the enclosing fanout/layout predicate`
- code change readiness: `blocked`
- recommended next ticket: `RE-027`

### item-data-word

- save original group: `8`
- restore group: `8`
- save payload profile: `source-missing-field=1;bytes=4`
- restore layout profile: `rare-payload-anchor;restore-size-sequence=1,1,20,2,2,2,2,4,2,2,2,2,2;extra-restore-byte-candidate=1`
- source predicate profile: `no current source predicate for item data pointer/word payload`
- branch profile: `restore_group=8:object-subtype-layout-fanout/branch-fanout-candidate/branch_total=20`
- prior group 5 dependency: `none`
- blocking predicates: `item data pointer/word payload has no source field identity`
- proof verdict: `item-data-pointer-predicate-unproven`
- next action: `identify the item data word as a concrete source field or non-source rebuilt state`
- code change readiness: `blocked`
- recommended next ticket: `RE-027`

### item_flags[3,0,1]

- save original group: `8`
- restore group: `8`
- save payload profile: `source-missing-field=3;bytes=6`
- restore layout profile: `rare-payload-anchor;restore-size-sequence=1,1,20,2,2,2,2,4,2,2,2,2,2;extra-restore-byte-candidate=1`
- source predicate profile: `item flag payload bodies remain absent from current source`
- branch profile: `restore_group=8:object-subtype-layout-fanout/branch-fanout-candidate/branch_total=20`
- prior group 5 dependency: `group5-item-flag-payloads-blocked`
- blocking predicates: `group 8 repeats item flag payload blockers already visible in group 5`
- proof verdict: `item-flag-payload-predicate-unproven`
- next action: `reuse the group 5 item-flag payload proof blocker before attempting group 8 source edits`
- code change readiness: `blocked`
- recommended next ticket: `RE-027`

### anim-state-payload

- save original group: `8`
- restore group: `8`
- save payload profile: `exact-field-width-match=3;bytes=6`
- restore layout profile: `rare-payload-anchor;restore-size-sequence=1,1,20,2,2,2,2,4,2,2,2,2,2;extra-restore-byte-candidate=1`
- source predicate profile: `anim-state widths are source-visible in this branch`
- branch profile: `restore_group=8:object-subtype-layout-fanout/branch-fanout-candidate/branch_total=20`
- prior group 5 dependency: `none`
- blocking predicates: `field widths match but branch fanout/layout identity remains unresolved`
- proof verdict: `field-width-match-fanout-still-blocked`
- next action: `keep anim-state fields as matched subfields while proving the enclosing object subtype fanout`
- code change readiness: `blocked`
- recommended next ticket: `RE-027`

## Verdict

RE-026 shows that save group `8` contains some source-visible width matches, but the subtype byte, extra restore byte candidate, layout block, room/rotation ordering, item data word, and item-flag payload bodies remain unresolved inside an object subtype fanout.

Do not add `(F)`, `(D)`, or `(**)` markers. Do not patch `GAME/SAVEGAME.C` from this evidence alone.

Recommended next ticket: RE-027 — derive a source-level RestoreLevelData implementation readiness refresh from RE-024, RE-025, and RE-026, keeping all blocked predicates explicit before any source patch.
