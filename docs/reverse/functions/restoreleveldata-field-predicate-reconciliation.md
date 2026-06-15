# RestoreLevelData field/predicate reconciliation

Status: Generated
Story: `docs/stories/RE-022-restoreleveldata-field-predicate-reconciliation.md`

## Progress tracker

- [x] Load RE-017 source/original field-width metadata.
- [x] Load RE-020 restore candidate field/control-flow links.
- [x] Load RE-021 branch/predicate hypotheses.
- [x] Reconcile matched versus unresolved field counts per priority save group.
- [x] Record source predicate families and unresolved predicate blockers.
- [x] Keep raw opcode text, machine words, payload coordinates, addresses, and branch/call targets out of versioned outputs.
- [x] Preserve marker verdict limits.

## Inputs

- RE-017 field-width CSV: `docs/reverse/generated/saveleveldata-item-field-width-audit.csv`
- RE-020 field/control-flow CSV: `docs/reverse/generated/restoreleveldata-field-control-flow-proof.csv`
- RE-021 branch/predicate CSV: `docs/reverse/generated/restoreleveldata-branch-predicate-map.csv`

## Summary

- save groups covered: `4, 5, 8, 10`
- proof rows: `4`
- patch-ready groups: `0`
- status: `restore-field-predicate-reconciliation-partial`

## Field/predicate matrix

### Save group 4

- restore groups: `4;5`
- branch predicate hypotheses: `restore_group=4:active-item-header-and-animation-split/split-branch-candidate; restore_group=5:active-item-optional-payload-fanout/branch-fanout-candidate`
- branch summary: `restore_group=4:before:conditional-compare=2;before:unconditional-jump=1;inside:conditional-compare=4;inside:unconditional-jump=3;after:conditional-compare=2;after:unconditional-jump=1; restore_group=5:before:conditional-compare=1;inside:conditional-compare=11;inside:unconditional-jump=7;after:conditional-compare=2`
- matched field count: `14`
- unresolved field count: `3`
- unresolved gap summary: `source-width-mismatch=3`
- source predicate summary: `obj->save_position;obj->save_anim;word-bit optional x_rot/z_rot/speed/fallspeed;lara anim variant;obj->save_hitpoints`
- unresolved predicates: `anim-state byte-vs-word restore predicate;split restore groups 4+5`
- proof status: `field-identity-partial-predicate-blocked`
- patch readiness: `blocked`
- proof limit: Most position/rotation/speed/anim fields have width matches, but anim-state byte-vs-word differences and split restore branch predicates still block a safe source patch. RE-020 limit: restore read regions are split across candidate groups 4 and 5; repeated 2-byte fields prevent field/predicate proof.

### Save group 5

- restore groups: `6`
- branch predicate hypotheses: `restore_group=6:object-payload-anchor-compact-branch/rare-anchor-branch-candidate`
- branch summary: `restore_group=6:before:conditional-compare=1;before:conditional-sign=1;inside:conditional-sign=1`
- matched field count: `1`
- unresolved field count: `14`
- unresolved gap summary: `source-missing-field=14`
- source predicate summary: `obj->save_flags;word-bit item_flags/timer/trigger_flags;object extension payload`
- unresolved predicates: `item_flags[0..3] payload;timer payload;trigger_flags payload;object-specific 24/20-byte payload blocks`
- proof status: `payload-predicate-missing`
- patch readiness: `blocked`
- proof limit: Only the packed flags word is source-backed; separate flag/timer/trigger and object payload predicates remain missing on the source side. RE-020 limit: object payload anchors exist on restore side, but leading packed flags and separate item flag/timer/trigger payload predicates remain unproved.

### Save group 8

- restore groups: `8`
- branch predicate hypotheses: `restore_group=8:object-subtype-layout-fanout/branch-fanout-candidate`
- branch summary: `restore_group=8:before:conditional-compare=3;inside:conditional-compare=9;inside:unconditional-jump=5;after:conditional-compare=2;after:unconditional-jump=1`
- matched field count: `5`
- unresolved field count: `7`
- unresolved gap summary: `source-missing-field=5;source-layout-mismatch=2`
- source predicate summary: `object subtype/layout fanout;item_flags payload;anim-state payload;speed/fallspeed payload`
- unresolved predicates: `subtype byte;20-byte layout block;room/rotation ordering;item_flags payload predicates;extra restore bytes`
- proof status: `layout-and-predicate-mismatch`
- patch readiness: `blocked`
- proof limit: Field identity is mixed: speed/fallspeed/anim states match, but extra restore bytes, layout blocks, and item_flags predicates remain unresolved. RE-020 limit: object payload anchors exist on restore side, but extra restore bytes and layout mismatches still block field equivalence.

### Save group 10

- restore groups: `9`
- branch predicate hypotheses: `restore_group=9:exact-window-room-sentinel-candidate/exact-window-needs-predicate-proof`
- branch summary: `restore_group=9:before:conditional-compare=1;before:unconditional-jump=1;inside:conditional-compare=2;after:conditional-compare=2`
- matched field count: `6`
- unresolved field count: `1`
- unresolved gap summary: `source-layout-mismatch=1`
- source predicate summary: `position/rotation room layout window;optional x_rot predicate`
- unresolved predicates: `room byte order/layout predicate`
- proof status: `exact-window-field-partial`
- patch readiness: `blocked`
- proof limit: The size window and most field widths match, but exact size does not prove the room byte order/layout predicate. RE-020 limit: exact size window is not predicate proof; room/control-flow layout still needs restore-side field proof.

## Verdict

RE-022 makes the blockers more actionable, but it still does not prove exact restore-side field predicates. Patch readiness remains `0`.

Do not add `(F)`, `(D)`, or `(**)` markers. Do not patch `GAME/SAVEGAME.C` from this evidence alone.

Next step: build a restore implementation plan only after the missing payload predicates and layout blockers have source-level proof.
