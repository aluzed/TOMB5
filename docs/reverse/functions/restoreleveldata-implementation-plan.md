# RestoreLevelData implementation plan

Status: Generated
Story: `docs/stories/RE-023-restoreleveldata-implementation-plan.md`

## Progress tracker

- [x] Load RE-022 field/predicate reconciliation metadata.
- [x] Convert each priority save group into a restore implementation readiness row.
- [x] Preserve blocked status for all code changes until missing proofs are resolved.
- [x] Recommend proof-first follow-up tickets before touching `GAME/SAVEGAME.C`.
- [x] Keep raw opcode text, machine words, payload coordinates, addresses, and branch/call targets out of versioned outputs.

## Inputs

- RE-022 reconciliation CSV: `docs/reverse/generated/restoreleveldata-field-predicate-reconciliation.csv`

## Summary

- save groups covered: `4, 5, 8, 10`
- plan rows: `4`
- patch-ready groups: `0`
- code-change-ready groups: `0`
- status: `restoreleveldata-implementation-plan-blocked`

## Implementation readiness matrix

### Save group 4

- restore groups: `4;5`
- implementation phase: `prove-split-active-item-layout`
- missing proof: `anim-state byte-vs-word restore predicate;split restore groups 4+5`
- minimal safe action: `derive source-level split predicate checklist for active item header and animation payloads`
- code change readiness: `blocked`
- recommended next ticket: `RE-024`
- risk level: `high`
- proof source: `RE-022 field/predicate reconciliation`
- notes: RE-022 proof_status=field-identity-partial-predicate-blocked. Prioritize only after split restore groups are explained by source predicates; repeated 2-byte fields make blind coding unsafe.

### Save group 5

- restore groups: `6`
- implementation phase: `prove-object-extension-payloads`
- missing proof: `item_flags[0..3] payload;timer payload;trigger_flags payload;object-specific 24/20-byte payload blocks`
- minimal safe action: `derive source-level payload predicate checklist`
- code change readiness: `blocked`
- recommended next ticket: `RE-025`
- risk level: `high`
- proof source: `RE-022 field/predicate reconciliation`
- notes: RE-022 proof_status=payload-predicate-missing. Packed flags alone are insufficient; each optional item flag, timer, trigger, and object extension payload needs a source predicate before code changes.

### Save group 8

- restore groups: `8`
- implementation phase: `prove-object-subtype-layout-fanout`
- missing proof: `subtype byte;20-byte layout block;room/rotation ordering;item_flags payload predicates;extra restore bytes`
- minimal safe action: `separate subtype/layout alternatives and identify extra restore bytes as source fields or non-source state rebuild`
- code change readiness: `blocked`
- recommended next ticket: `RE-026`
- risk level: `high`
- proof source: `RE-022 field/predicate reconciliation`
- notes: RE-022 proof_status=layout-and-predicate-mismatch. Layout fanout and extra restore bytes are the riskiest blockers; keep this behind proof work, not serializer edits.

### Save group 10

- restore groups: `9`
- implementation phase: `prove-room-layout-window`
- missing proof: `room byte order/layout predicate`
- minimal safe action: `prove room byte order/layout predicate from source-level field model`
- code change readiness: `blocked`
- recommended next ticket: `RE-024`
- risk level: `medium`
- proof source: `RE-022 field/predicate reconciliation`
- notes: RE-022 proof_status=exact-window-field-partial. This is the smallest blocker set and a good next proof target, but exact window size alone is still not enough for a patch.

## Execution order

1. Start with RE-024 because save group `10` has the smallest blocker set and can also validate the split proof pattern needed by save group `4`.
2. Defer save group `5` until item flag, timer, trigger, and object extension payload predicates are source-backed.
3. Defer save group `8` until subtype/layout fanout and extra restore bytes are explained without guessing.
4. Only after a row becomes code-change-ready should a later ticket modify `GAME/SAVEGAME.C`.

## Verdict

RE-023 is a plan, not an implementation patch. All groups remain blocked for code changes.

Do not add `(F)`, `(D)`, or `(**)` markers. Do not patch `GAME/SAVEGAME.C` from this evidence alone.

Recommended next ticket: RE-024 — prove the room/layout predicate window for save group `10` and the active item split predicate path needed by save group `4`.
