# RestoreLevelData room/split predicate proof

Status: Generated
Story: `docs/stories/RE-024-restoreleveldata-room-split-predicate-proof.md`

## Progress tracker

- [x] Load RE-023 implementation plan metadata.
- [x] Load RE-022 field/predicate blockers.
- [x] Load field-width, restore control-flow, and branch predicate summaries.
- [x] Build proof rows for save groups `10` and `4`.
- [x] Keep code-change readiness blocked until predicates are proved more strongly.
- [x] Keep raw opcode text, machine words, payload coordinates, addresses, and branch/call targets out of versioned outputs.

## Inputs

- RE-023 plan CSV: `docs/reverse/generated/restoreleveldata-implementation-plan.csv`
- RE-022 reconciliation CSV: `docs/reverse/generated/restoreleveldata-field-predicate-reconciliation.csv`
- RE-017 field-width CSV: `docs/reverse/generated/saveleveldata-item-field-width-audit.csv`
- RE-020 control-flow CSV: `docs/reverse/generated/restoreleveldata-field-control-flow-proof.csv`
- RE-021 branch predicate CSV: `docs/reverse/generated/restoreleveldata-branch-predicate-map.csv`

## Summary

- target save groups: `10, 4`
- proof rows: `2`
- code-change-ready groups: `0`
- status: `restoreleveldata-room-split-proof-partial`

## Proof matrix

### Save group 10

- restore groups: `9`
- proof focus: `room-layout-window`
- field-width profile: `exact-field-width-match=6;source-layout-mismatch=1`
- restore shape: `exact-size-window`
- branch profile: `restore_group=9:exact-window-room-sentinel-candidate/exact-window-needs-predicate-proof/branch_total=6`
- blocking predicates: `room byte order/layout predicate`
- source-safe hypothesis: `room byte is source-visible but its restore placement/order is still not predicate proof`
- proof verdict: `room-layout-predicate-unproven`
- next action: `model room byte placement and optional rotation predicate before source patch`
- code change readiness: `blocked`
- recommended next ticket: `RE-025`

### Save group 4

- restore groups: `4;5`
- proof focus: `active-item-split-predicate`
- field-width profile: `exact-field-width-match=14;source-width-mismatch=3`
- restore shape: `control-flow-split-candidate`
- branch profile: `restore_group=4:active-item-header-and-animation-split/split-branch-candidate/branch_total=13; restore_group=5:active-item-optional-payload-fanout/branch-fanout-candidate/branch_total=21`
- blocking predicates: `anim-state byte-vs-word restore predicate;split restore groups 4+5`
- source-safe hypothesis: `active item fields are source-visible but split restore regions and anim-state width differences remain unproved`
- proof verdict: `split-predicate-and-anim-width-unproven`
- next action: `derive split active-item predicate checklist and anim-state width decision`
- code change readiness: `blocked`
- recommended next ticket: `RE-025`

## Verdict

RE-024 narrows the proof work but still does not make any restore group safe to implement in source.

Do not add `(F)`, `(D)`, or `(**)` markers. Do not patch `GAME/SAVEGAME.C` from this evidence alone.

Recommended next ticket: RE-025 — prove the payload predicates for save group `5` while keeping the group `10` and group `4` predicate blockers visible.
