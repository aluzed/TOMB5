# RestoreLevelData group 5 item_flags body proof

Status: Generated
Story: `docs/stories/RE-029-restoreleveldata-group5-item-flags-body-proof.md`

## Progress tracker

- [x] Select RE-028 payload family `item_flags[0..3]`.
- [x] Load RE-017 save-side field-width metadata for the four item flag payloads.
- [x] Load RE-021 restore group `6` branch context and RE-019 read-size context.
- [x] Inspect current source text for header predicates and separate payload write sites.
- [x] Publish per-flag body proof rows while keeping patch readiness blocked.
- [x] Keep raw opcode text, machine words, payload coordinates, addresses, and branch/call targets out of versioned outputs.

## Inputs

- RE-028 checklist CSV: `docs/reverse/generated/restoreleveldata-group5-source-field-identity-checklist.csv`
- RE-017 field-width CSV: `docs/reverse/generated/saveleveldata-item-field-width-audit.csv`
- RE-019 read map CSV: `docs/reverse/generated/restoreleveldata-read-call-map.csv`
- RE-021 branch map CSV: `docs/reverse/generated/restoreleveldata-branch-predicate-map.csv`
- Source file inspected: `GAME/SAVEGAME.C`

## Summary

- source inputs: `RE-017, RE-021, RE-028, GAME/SAVEGAME.C`
- target save group: `5`
- restore group: `6`
- payload family: `item_flags[0..3]`
- proof rows: `4`
- patch-ready rows: `0`
- status: `restoreleveldata-group5-item-flags-body-proof-blocked`

## Item flag body rows

### item_flags[0]

- payload field: `item->item_flags[0] payload`
- header predicate: `item->item_flags[0] -> word bit 0x80`
- source body evidence: `no separate Write site in current source`
- save payload width: `2`
- restore candidate width: `2`
- restore candidate context: `restore group 6 compact branch payload cluster`
- body order status: `candidate-width-only`
- proof status: `payload-body-identity-missing`
- code change readiness: `blocked`
- safe next action: `do not patch; recover source/restore assignment identity before serializer edit`
- recommended next ticket: `RE-030`

### item_flags[1]

- payload field: `item->item_flags[1] payload`
- header predicate: `item->item_flags[1] -> word bit 0x100`
- source body evidence: `no separate Write site in current source`
- save payload width: `2`
- restore candidate width: `2`
- restore candidate context: `restore group 6 compact branch payload cluster`
- body order status: `candidate-width-only`
- proof status: `payload-body-identity-missing`
- code change readiness: `blocked`
- safe next action: `do not patch; recover source/restore assignment identity before serializer edit`
- recommended next ticket: `RE-030`

### item_flags[2]

- payload field: `item->item_flags[2] payload`
- header predicate: `item->item_flags[2] -> word bit 0x200`
- source body evidence: `no separate Write site in current source`
- save payload width: `2`
- restore candidate width: `2`
- restore candidate context: `restore group 6 compact branch payload cluster`
- body order status: `candidate-width-only`
- proof status: `payload-body-identity-missing`
- code change readiness: `blocked`
- safe next action: `do not patch; recover source/restore assignment identity before serializer edit`
- recommended next ticket: `RE-030`

### item_flags[3]

- payload field: `item->item_flags[3] payload`
- header predicate: `item->item_flags[3] -> word bit 0x400`
- source body evidence: `no separate Write site in current source`
- save payload width: `2`
- restore candidate width: `2`
- restore candidate context: `restore group 6 compact branch payload cluster`
- body order status: `candidate-width-only`
- proof status: `payload-body-identity-missing`
- code change readiness: `blocked`
- safe next action: `do not patch; recover source/restore assignment identity before serializer edit`
- recommended next ticket: `RE-030`

## Verdict

RE-029 proves the current limit for the `item_flags[0..3]` payload family: all four header predicates are visible in source, and 2-byte payload widths are present in metadata, but there are no separate source write bodies or versioned restore assignment identities. The result is candidate-width-only, not source-field identity proof.

Do not add `(F)`, `(D)`, or `(**)` markers; do not patch `GAME/SAVEGAME.C` from this proof alone.

Recommended next ticket: RE-030 — recover a versionable restore assignment identity map for group `5` payload bodies, or defer group `5` from any source reconstruction scope.
