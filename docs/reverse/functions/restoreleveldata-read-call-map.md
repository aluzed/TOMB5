# RestoreLevelData ReadSG call-map audit

Status: Generated
Story: `docs/stories/RE-019-restoreleveldata-read-call-map.md`

## Progress tracker

- [x] Extract original `ReadSG` call coordinates and size metadata.
- [x] Group restore-side read calls by row-index gaps.
- [x] Compare RE-017 item size sequences against restore read size subsequences.
- [x] Keep original opcode rows and machine words out of versioned outputs.
- [x] Preserve marker verdict limits.

## Inputs

- Original dump CSV: `build/reverse/re007/original/RestoreLevelData_80054f6c.csv` (ignored; not versioned)
- RE-017 field-width CSV: `docs/reverse/generated/saveleveldata-item-field-width-audit.csv`
- ReadSG final PSX address: metadata target configured in the generator; raw call opcodes are not emitted.
- Grouping gap threshold: `24` row indices

## Summary

- original `ReadSG` calls: `79`
- restore read groups: `10`
- RE-017 item groups compared: `8`
- groups with size-only restore match: `4`
- patch-ready groups: `0`
- status: `restore-size-proof-partial`

## Restore ReadSG groups

The call indices, addresses, and sizes below are metadata coordinates only. This report does not include original opcode text, machine words, payload offsets, or dump rows.

### Restore read group 1

- read call count: `9`
- call index range: `14` → `65`
- call address range: `0x80054fa4` → `0x80055070`
- size sequence: `4,4,2,2,4,4,4,136,1`

### Restore read group 2

- read call count: `1`
- call index range: `93` → `93`
- call address range: `0x800550e0` → `0x800550e0`
- size sequence: `2`

### Restore read group 3

- read call count: `6`
- call index range: `151` → `223`
- call address range: `0x800551c8` → `0x800552e8`
- size sequence: `1,1,3,2,2,2`

### Restore read group 4

- read call count: `9`
- call index range: `250` → `321`
- call address range: `0x80055354` → `0x80055470`
- size sequence: `2,2,2,1,2,2,2,2,2`

### Restore read group 5

- read call count: `15`
- call index range: `358` → `477`
- call address range: `0x80055504` → `0x800556e0`
- size sequence: `1,1,1,2,1,2,2,4,2,2,2,2,2,2,2`

### Restore read group 6

- read call count: `8`
- call index range: `564` → `595`
- call address range: `0x8005583c` → `0x800558b8`
- size sequence: `24,2,2,2,2,2,20,1`

### Restore read group 7

- read call count: `2`
- call index range: `645` → `648`
- call address range: `0x80055980` → `0x8005598c`
- size sequence: `4,4`

### Restore read group 8

- read call count: `13`
- call index range: `734` → `830`
- call address range: `0x80055ae4` → `0x80055c64`
- size sequence: `1,1,20,2,2,2,2,4,2,2,2,2,2`

### Restore read group 9

- read call count: `8`
- call index range: `856` → `906`
- call address range: `0x80055ccc` → `0x80055d94`
- size sequence: `1,2,2,2,2,2,2,1`

### Restore read group 10

- read call count: `8`
- call index range: `931` → `981`
- call address range: `0x80055df8` → `0x80055ec0`
- size sequence: `1,2,2,2,2,2,2,2`

## RE-017 / RE-018 comparison

### Save original item group 4

- save call count: `17`
- save size sequence: `2,2,2,2,1,2,2,2,2,2,1,1,1,2,1,2,2`
- restore match status: `no-exact-restore-size-sequence`
- restore match locations: `none`
- patch readiness: `blocked`
- notes: No exact contiguous restore ReadSG size subsequence matches this RE-017 item group.

### Save original item group 5

- save call count: `15`
- save size sequence: `4,2,2,2,2,2,2,2,24,2,2,2,2,2,20`
- restore match status: `no-exact-restore-size-sequence`
- restore match locations: `none`
- patch readiness: `blocked`
- notes: No exact contiguous restore ReadSG size subsequence matches this RE-017 item group.

### Save original item group 6

- save call count: `3`
- save size sequence: `1,4,4`
- restore match status: `no-exact-restore-size-sequence`
- restore match locations: `none`
- patch readiness: `blocked`
- notes: No exact contiguous restore ReadSG size subsequence matches this RE-017 item group.

### Save original item group 7

- save call count: `1`
- save size sequence: `1`
- restore match status: `ambiguous-single-byte-restore-matches`
- restore match locations: `restore_group=1:call_ordinal=9; restore_group=3:call_ordinal=1; restore_group=3:call_ordinal=2; restore_group=4:call_ordinal=4; restore_group=5:call_ordinal=1; restore_group=5:call_ordinal=2; restore_group=5:call_ordinal=3; restore_group=5:call_ordinal=5; restore_group=6:call_ordinal=8; restore_group=8:call_ordinal=1; restore_group=8:call_ordinal=2; restore_group=9:call_ordinal=1; restore_group=9:call_ordinal=8; restore_group=10:call_ordinal=1`
- patch readiness: `blocked`
- notes: Single-byte groups match many restore locations and do not identify a field or branch by themselves.

### Save original item group 8

- save call count: `12`
- save size sequence: `1,20,2,2,2,4,2,2,2,2,2,2`
- restore match status: `no-exact-restore-size-sequence`
- restore match locations: `none`
- patch readiness: `blocked`
- notes: No exact contiguous restore ReadSG size subsequence matches this RE-017 item group.

### Save original item group 9

- save call count: `1`
- save size sequence: `1`
- restore match status: `ambiguous-single-byte-restore-matches`
- restore match locations: `restore_group=1:call_ordinal=9; restore_group=3:call_ordinal=1; restore_group=3:call_ordinal=2; restore_group=4:call_ordinal=4; restore_group=5:call_ordinal=1; restore_group=5:call_ordinal=2; restore_group=5:call_ordinal=3; restore_group=5:call_ordinal=5; restore_group=6:call_ordinal=8; restore_group=8:call_ordinal=1; restore_group=8:call_ordinal=2; restore_group=9:call_ordinal=1; restore_group=9:call_ordinal=8; restore_group=10:call_ordinal=1`
- patch readiness: `blocked`
- notes: Single-byte groups match many restore locations and do not identify a field or branch by themselves.

### Save original item group 10

- save call count: `7`
- save size sequence: `2,2,2,2,2,2,1`
- restore match status: `exact-restore-size-subsequence-match`
- restore match locations: `restore_group=9:call_ordinal=2`
- patch readiness: `blocked`
- notes: Size sequence exists on restore side, but this is not field/predicate proof and does not unlock a patch alone.

### Save original item group 11

- save call count: `1`
- save size sequence: `1`
- restore match status: `ambiguous-single-byte-restore-matches`
- restore match locations: `restore_group=1:call_ordinal=9; restore_group=3:call_ordinal=1; restore_group=3:call_ordinal=2; restore_group=4:call_ordinal=4; restore_group=5:call_ordinal=1; restore_group=5:call_ordinal=2; restore_group=5:call_ordinal=3; restore_group=5:call_ordinal=5; restore_group=6:call_ordinal=8; restore_group=8:call_ordinal=1; restore_group=8:call_ordinal=2; restore_group=9:call_ordinal=1; restore_group=9:call_ordinal=8; restore_group=10:call_ordinal=1`
- patch readiness: `blocked`
- notes: Single-byte groups match many restore locations and do not identify a field or branch by themselves.

## Verdict

RE-019 finds only size-sequence evidence. Most RE-017 item groups do not have an exact contiguous restore-size match; the matching single-byte groups are ambiguous, and the group 10 size subsequence is not field/predicate proof. Patch readiness remains `0`.

Do not add `(F)`, `(D)`, or `(**)` markers. Do not patch `GAME/SAVEGAME.C` from this evidence alone.

Next step: derive stronger restore-side field/control-flow proof for the matched and mismatched regions, especially branch predicates around item groups 4, 5, 8, and 10.
