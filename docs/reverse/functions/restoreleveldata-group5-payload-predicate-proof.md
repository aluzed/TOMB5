# RestoreLevelData group 5 payload predicate proof

Status: Generated
Story: `docs/stories/RE-025-restoreleveldata-group5-payload-predicate-proof.md`

## Progress tracker

- [x] Load RE-023 implementation plan metadata.
- [x] Load RE-022 save group `5` field/predicate blockers.
- [x] Load RE-017 field-width rows for packed flags, item flags, timer, trigger flags, and object payload blocks.
- [x] Load RE-020/RE-021 restore group `6` payload anchor and branch summaries.
- [x] Build payload-family proof rows while keeping code-change readiness blocked.
- [x] Keep raw opcode text, machine words, payload coordinates, addresses, and branch/call targets out of versioned outputs.

## Inputs

- RE-023 plan CSV: `docs/reverse/generated/restoreleveldata-implementation-plan.csv`
- RE-022 reconciliation CSV: `docs/reverse/generated/restoreleveldata-field-predicate-reconciliation.csv`
- RE-017 field-width CSV: `docs/reverse/generated/saveleveldata-item-field-width-audit.csv`
- RE-020 control-flow CSV: `docs/reverse/generated/restoreleveldata-field-control-flow-proof.csv`
- RE-021 branch predicate CSV: `docs/reverse/generated/restoreleveldata-branch-predicate-map.csv`

## Summary

- target save group: `5`
- restore group: `6`
- payload rows: `5`
- code-change-ready payload families: `0`
- status: `restoreleveldata-group5-payload-proof-blocked`

## Payload predicate matrix

### packed-status-flags

- save original group: `5`
- restore group: `6`
- save payload profile: `exact-field-width-match=1;bytes=4`
- restore payload profile: `rare-payload-anchor;restore-size-sequence=24,2,2,2,2,2,20,1`
- source predicate profile: `obj->save_flags guarded packed status word`
- branch profile: `restore_group=6:object-payload-anchor-compact-branch/rare-anchor-branch-candidate/branch_total=3`
- blocking predicates: `packed status word exists, but it is only an anchor for this payload cluster`
- proof verdict: `source-backed-anchor-only`
- next action: `keep packed status word as the group anchor and prove following payload predicates separately`
- code change readiness: `blocked`
- recommended next ticket: `RE-026`

### item_flags[0..3]

- save original group: `5`
- restore group: `6`
- save payload profile: `source-missing-field=4;bytes=8`
- restore payload profile: `rare-payload-anchor;restore-size-sequence=24,2,2,2,2,2,20,1`
- source predicate profile: `header-bit predicates visible; separate payload writes absent`
- branch profile: `restore_group=6:object-payload-anchor-compact-branch/rare-anchor-branch-candidate/branch_total=3`
- blocking predicates: `item flag header bits do not prove the four item flag payload words or restore body order`
- proof verdict: `payload-body-predicate-unproven`
- next action: `derive source-backed predicates and restore reads for four item flag payload words`
- code change readiness: `blocked`
- recommended next ticket: `RE-026`

### timer

- save original group: `5`
- restore group: `6`
- save payload profile: `source-missing-field=1;bytes=2`
- restore payload profile: `rare-payload-anchor;restore-size-sequence=24,2,2,2,2,2,20,1`
- source predicate profile: `header-bit predicate visible; separate timer payload write absent`
- branch profile: `restore_group=6:object-payload-anchor-compact-branch/rare-anchor-branch-candidate/branch_total=3`
- blocking predicates: `timer header bit does not prove a separate timer payload body or restore assignment`
- proof verdict: `payload-body-predicate-unproven`
- next action: `derive a source-backed timer payload predicate and restore assignment before serializer edits`
- code change readiness: `blocked`
- recommended next ticket: `RE-026`

### trigger_flags

- save original group: `5`
- restore group: `6`
- save payload profile: `source-missing-field=1;bytes=2`
- restore payload profile: `rare-payload-anchor;restore-size-sequence=24,2,2,2,2,2,20,1`
- source predicate profile: `header-bit predicate visible; separate trigger_flags payload write absent`
- branch profile: `restore_group=6:object-payload-anchor-compact-branch/rare-anchor-branch-candidate/branch_total=3`
- blocking predicates: `trigger_flags header bit does not prove a separate trigger_flags payload body or restore assignment`
- proof verdict: `payload-body-predicate-unproven`
- next action: `derive a source-backed trigger_flags payload predicate and restore assignment before serializer edits`
- code change readiness: `blocked`
- recommended next ticket: `RE-026`

### object-extension

- save original group: `5`
- restore group: `6`
- save payload profile: `source-missing-field=8;bytes=56;rare-blocks=24,20`
- restore payload profile: `rare-payload-anchor;restore-size-sequence=24,2,2,2,2,2,20,1`
- source predicate profile: `no current source predicate for object-specific short and block payloads`
- branch profile: `restore_group=6:object-payload-anchor-compact-branch/rare-anchor-branch-candidate/branch_total=3`
- blocking predicates: `object-specific short and block payloads lack source field identity and object predicate mapping`
- proof verdict: `object-extension-predicate-unproven`
- next action: `map object-specific short, twenty-four-byte, and twenty-byte payload predicates before any source patch`
- code change readiness: `blocked`
- recommended next ticket: `RE-026`

## Verdict

RE-025 proves only that save group `5` has a packed status-flags anchor plus source-visible header-bit predicates for item flags, timer, and trigger flags. It does not prove the separate payload bodies, restore assignment order, or object-extension predicates.

Do not add `(F)`, `(D)`, or `(**)` markers. Do not patch `GAME/SAVEGAME.C` from this evidence alone.

Recommended next ticket: RE-026 — prove object subtype/layout fanout and extra restore bytes for save group `8`, while keeping save group `5` payload-body predicates blocked until source-backed field identities exist.
