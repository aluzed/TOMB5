# SaveLevelData item control-flow audit

Status: Generated
Story: `docs/stories/RE-016-saveleveldata-item-control-flow-proof.md`

## Progress tracker

- [x] Derive original `WriteSG` call size metadata from the ignored dump.
- [x] Enumerate current-source item active/full-save size sequences.
- [x] Compare item groups `4` to `12` by exact size sequence.
- [x] Keep original rows and binary words out of versioned outputs.
- [x] Preserve marker verdict limits.

## Inputs

- Original dump CSV: `build/reverse/re007/original/SaveLevelData_80053f10.csv` (ignored; not versioned)
- Item count audit CSV: `docs/reverse/generated/saveleveldata-item-flag-audit.csv`
- `WriteSG` final PSX address: `0x80053b04`

## Summary

- item candidate groups: `9`
- exact-match groups: `12`
- mismatch groups: `4, 5, 6, 7, 8, 9, 10, 11`
- status: `control-flow-gaps-found`

## Method

This report records only call coordinates and size arguments. The original dump remains ignored and no original row text or machine word is emitted here.

A match means the whole grouped size sequence is exactly reproducible by at least one current-source item branch case. It is still weaker than semantic equivalence because predicate identity and field provenance are not proven.

## Item group comparison

### Original item group 4

- original call count: `17`
- call index range: `338` → `441`
- call address range: `0x80054458` → `0x800545f4`
- original size sequence: `2,2,2,2,1,2,2,2,2,2,1,1,1,2,1,2,2`
- count-level source cases: `active_header=1 + save_position=9 + save_anim=5 + save_hitpoints=1 + save_flags=1`
- exact matching source cases: `none`
- control-flow status: `size-sequence-mismatch`
- notes: Count is representable, but no exact source size sequence matches the original group; inspect field widths and branch boundaries before any marker claim.

### Original item group 5

- original call count: `15`
- call index range: `501` → `600`
- call address range: `0x800546e4` → `0x80054870`
- original size sequence: `4,2,2,2,2,2,2,2,24,2,2,2,2,2,20`
- count-level source cases: `active_header=1 + save_position=7 + save_anim=5 + save_hitpoints=1 + save_flags=1; active_header=1 + save_position=8 + save_anim=5 + save_flags=1; active_header=1 + save_position=8 + save_anim=5 + save_hitpoints=1; active_header=1 + save_position=9 + save_anim=5`
- exact matching source cases: `none`
- control-flow status: `size-sequence-mismatch`
- notes: Count is representable, but no exact source size sequence matches the original group; inspect field widths and branch boundaries before any marker claim.

### Original item group 6

- original call count: `3`
- call index range: `635` → `645`
- call address range: `0x800548fc` → `0x80054924`
- original size sequence: `1,4,4`
- count-level source cases: `active_header=1 + save_hitpoints=1 + save_flags=1`
- exact matching source cases: `none`
- control-flow status: `size-sequence-mismatch`
- notes: Count is representable, but no exact source size sequence matches the original group; inspect field widths and branch boundaries before any marker claim.

### Original item group 7

- original call count: `1`
- call index range: `698` → `698`
- call address range: `0x800549f8` → `0x800549f8`
- original size sequence: `1`
- count-level source cases: `active_header=1`
- exact matching source cases: `none`
- control-flow status: `size-sequence-mismatch`
- notes: Count is representable, but no exact source size sequence matches the original group; inspect field widths and branch boundaries before any marker claim.

### Original item group 8

- original call count: `12`
- call index range: `750` → `800`
- call address range: `0x80054ac8` → `0x80054b90`
- original size sequence: `1,20,2,2,2,4,2,2,2,2,2,2`
- count-level source cases: `active_header=1 + save_position=5 + save_anim=5 + save_flags=1; active_header=1 + save_position=5 + save_anim=5 + save_hitpoints=1; active_header=1 + save_position=6 + save_anim=5; active_header=1 + save_position=9 + save_hitpoints=1 + save_flags=1`
- exact matching source cases: `none`
- control-flow status: `size-sequence-mismatch`
- notes: Count is representable, but no exact source size sequence matches the original group; inspect field widths and branch boundaries before any marker claim.

### Original item group 9

- original call count: `1`
- call index range: `841` → `841`
- call address range: `0x80054c34` → `0x80054c34`
- original size sequence: `1`
- count-level source cases: `active_header=1`
- exact matching source cases: `none`
- control-flow status: `size-sequence-mismatch`
- notes: Count is representable, but no exact source size sequence matches the original group; inspect field widths and branch boundaries before any marker claim.

### Original item group 10

- original call count: `7`
- call index range: `885` → `916`
- call address range: `0x80054ce4` → `0x80054d60`
- original size sequence: `2,2,2,2,2,2,1`
- count-level source cases: `active_header=1 + save_anim=5 + save_flags=1; active_header=1 + save_anim=5 + save_hitpoints=1; active_header=1 + save_position=5 + save_flags=1; active_header=1 + save_position=5 + save_hitpoints=1; active_header=1 + save_position=6`
- exact matching source cases: `none`
- control-flow status: `size-sequence-mismatch`
- notes: Count is representable, but no exact source size sequence matches the original group; inspect field widths and branch boundaries before any marker claim.

### Original item group 11

- original call count: `1`
- call index range: `946` → `946`
- call address range: `0x80054dd8` → `0x80054dd8`
- original size sequence: `1`
- count-level source cases: `active_header=1`
- exact matching source cases: `none`
- control-flow status: `size-sequence-mismatch`
- notes: Count is representable, but no exact source size sequence matches the original group; inspect field widths and branch boundaries before any marker claim.

### Original item group 12

- original call count: `7`
- call index range: `988` → `1019`
- call address range: `0x80054e80` → `0x80054efc`
- original size sequence: `2,2,2,2,2,2,2`
- count-level source cases: `active_header=1 + save_anim=5 + save_flags=1; active_header=1 + save_anim=5 + save_hitpoints=1; active_header=1 + save_position=5 + save_flags=1; active_header=1 + save_position=5 + save_hitpoints=1; active_header=1 + save_position=6`
- exact matching source cases: `active_header=1 + save_anim=lara + save_hitpoints=1`
- control-flow status: `exact-size-sequence-match`
- notes: Original size sequence has at least one exact current-source branch case; semantic branch predicates still need review.

## Verdict

RE-016 does not prove item control-flow equivalence. It finds exact size-sequence coverage only for group `12`; groups `4, 5, 6, 7, 8, 9, 10, 11` remain mismatched even though their call counts became representable in RE-015. Do not add `(F)`, `(D)`, or `(**)` markers from this evidence.
