# RestoreLevelData readiness refresh

Status: Generated
Story: `docs/stories/RE-027-restoreleveldata-readiness-refresh.md`

## Progress tracker

- [x] Load RE-023 implementation plan metadata.
- [x] Load RE-024 room/split predicate proof.
- [x] Load RE-025 group 5 payload predicate proof.
- [x] Load RE-026 group 8 layout/fanout proof.
- [x] Refresh readiness rows for save groups `4`, `5`, `8`, and `10`.
- [x] Keep source patch readiness blocked while blockers remain.
- [x] Keep raw opcode text, machine words, payload coordinates, addresses, and branch/call targets out of versioned outputs.

## Inputs

- RE-023 plan CSV: `docs/reverse/generated/restoreleveldata-implementation-plan.csv`
- RE-024 room/split CSV: `docs/reverse/generated/restoreleveldata-room-split-predicate-proof.csv`
- RE-025 group 5 payload CSV: `docs/reverse/generated/restoreleveldata-group5-payload-predicate-proof.csv`
- RE-026 group 8 fanout CSV: `docs/reverse/generated/restoreleveldata-group8-layout-fanout-proof.csv`

## Summary

- source proof inputs: `RE-024, RE-025, RE-026`
- target save groups: `4, 5, 8, 10`
- readiness rows: `4`
- code-change-ready groups: `0`
- status: `restoreleveldata-readiness-refresh-blocked`

## Readiness matrix

### Save group 4

- restore groups: `4;5`
- latest evidence: `RE-024 room/split predicate proof`
- evidence summary: `proof-focus=active-item-split-predicate;verdict=split-predicate-and-anim-width-unproven`
- prior plan phase: `prove-split-active-item-layout`
- remaining blockers: `anim-state byte-vs-word restore predicate;split restore groups 4+5`
- readiness phase: `continue-source-field-proof`
- safe next action: `prove split active-item restore predicates before source reconstruction`
- code change readiness: `blocked`
- recommended next ticket: `RE-028`

### Save group 5

- restore groups: `6`
- latest evidence: `RE-025 group 5 payload predicate proof`
- evidence summary: `payload-families=5;blocked=5;source-backed-anchor-only=1`
- prior plan phase: `prove-object-extension-payloads`
- remaining blockers: `item_flags[0..3] payload bodies;timer payload body;trigger_flags payload body;object-extension field identity`
- readiness phase: `continue-source-field-proof`
- safe next action: `prove payload body field identities or keep group out of source patch scope`
- code change readiness: `blocked`
- recommended next ticket: `RE-028`

### Save group 8

- restore groups: `8`
- latest evidence: `RE-026 group 8 layout/fanout proof`
- evidence summary: `fanout-families=7;blocked=7;group5-dependency=group5-item-flag-payloads-blocked`
- prior plan phase: `prove-object-subtype-layout-fanout`
- remaining blockers: `subtype/extra byte predicate;layout block 20;room/rotation ordering;item data word;item flag payload bodies`
- readiness phase: `continue-source-field-proof`
- safe next action: `prove subtype/layout fanout field identities or keep group out of source patch scope`
- code change readiness: `blocked`
- recommended next ticket: `RE-028`

### Save group 10

- restore groups: `9`
- latest evidence: `RE-024 room/split predicate proof`
- evidence summary: `proof-focus=room-layout-window;verdict=room-layout-predicate-unproven`
- prior plan phase: `prove-room-layout-window`
- remaining blockers: `room byte order/layout predicate`
- readiness phase: `continue-source-field-proof`
- safe next action: `prove room byte placement before source reconstruction`
- code change readiness: `blocked`
- recommended next ticket: `RE-028`

## Verdict

RE-027 confirms that all priority `RestoreLevelData` groups remain blocked after RE-024, RE-025, and RE-026. The safe path is additional source-field identity proof or a later patch scope that explicitly excludes blocked families.

Do not add `(F)`, `(D)`, or `(**)` markers. Do not patch `GAME/SAVEGAME.C` from this evidence alone.

Recommended next ticket: RE-028 — build a source-field identity checklist for the highest-value blocked family, or define a deliberately limited reconstruction scope that excludes every still-blocked predicate.
