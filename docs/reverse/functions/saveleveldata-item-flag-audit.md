# SaveLevelData item flag audit

Status: Generated
Story: `docs/stories/RE-014-saveleveldata-item-flag-audit.md`

## Progress tracker

- [x] Model source item serialization write-count cases.
- [x] Compare RE-013 item call groups against the source count model.
- [x] Identify source gaps without versioning original instructions or bytes.
- [x] Preserve marker verdict limits.

## Inputs

- Source: `GAME/SAVEGAME.C`
- Call-group map CSV: `docs/reverse/generated/saveleveldata-write-call-map.csv`

## Summary

- item candidate groups: `9`
- original item-group `WriteSG` calls: `64`
- possible current-source active branch counts: `0, 1, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15`
- active control word written: `no`
- save_flags write sites: `0`
- unrepresented original item groups: `4, 6`
- status: `source-gaps-found`

## Source count model

Current source rows 17-32 model the active/full-save item branch as:

- `save_position`: absent, or 5 required writes plus up to 4 optional writes (`x_rot`, `z_rot`, `speed`, `fallspeed`).
- `save_anim`: absent, or 5 writes (`current`, `goal`, `required`, anim number/byte, frame).
- `save_hitpoints`: absent, or 1 write.
- `save_flags`: currently 0 writes; the branch is a TODO/comment-only body.
- active branch control word: currently not written after `word = 0x8000` is assembled.

## Item group comparison

### Original item group 4

- original call count: `17`
- call index range: `338` → `441`
- call address range: `0x80054458` → `0x800545f4`
- candidate source rows: `17-25`
- candidate context: `item position block and optional speed/fallspeed writes`
- count status: `not-representable-by-current-source-count-model`
- matching source cases: `none`
- notes: Count exceeds current source maximum; likely missing active control word and/or save_flags writes.

### Original item group 5

- original call count: `15`
- call index range: `501` → `600`
- call address range: `0x800546e4` → `0x80054870`
- candidate source rows: `17-32`
- candidate context: `item active/full-save branch variant`
- count status: `representable-count-needs-control-flow-proof`
- matching source cases: `save_position=9 + save_anim=5 + save_hitpoints=1`
- notes: Count can be produced by current source write-count model; branch conditions still need manual proof.

### Original item group 6

- original call count: `3`
- call index range: `635` → `645`
- call address range: `0x800548fc` → `0x80054924`
- candidate source rows: `26-32`
- candidate context: `item animation and hitpoint fields`
- count status: `not-representable-by-current-source-count-model`
- matching source cases: `none`
- notes: Count falls into a gap in current optional flag combinations; audit original branch boundaries.

### Original item group 7

- original call count: `1`
- call index range: `698` → `698`
- call address range: `0x800549f8` → `0x800549f8`
- candidate source rows: `17-32`
- candidate context: `item serialization alternate control-flow region`
- count status: `representable-count-needs-control-flow-proof`
- matching source cases: `save_hitpoints=1`
- notes: Count can be produced by current source write-count model; branch conditions still need manual proof.

### Original item group 8

- original call count: `12`
- call index range: `750` → `800`
- call address range: `0x80054ac8` → `0x80054b90`
- candidate source rows: `17-32`
- candidate context: `item serialization dense call region`
- count status: `representable-count-needs-control-flow-proof`
- matching source cases: `save_position=6 + save_anim=5 + save_hitpoints=1; save_position=7 + save_anim=5`
- notes: Count can be produced by current source write-count model; branch conditions still need manual proof.

### Original item group 9

- original call count: `1`
- call index range: `841` → `841`
- call address range: `0x80054c34` → `0x80054c34`
- candidate source rows: `29-32`
- candidate context: `lara/non-lara anim-number and frame/hitpoint tail`
- count status: `representable-count-needs-control-flow-proof`
- matching source cases: `save_hitpoints=1`
- notes: Count can be produced by current source write-count model; branch conditions still need manual proof.

### Original item group 10

- original call count: `7`
- call index range: `885` → `916`
- call address range: `0x80054ce4` → `0x80054d60`
- candidate source rows: `17-32`
- candidate context: `item serialization second variant`
- count status: `representable-count-needs-control-flow-proof`
- matching source cases: `save_position=6 + save_hitpoints=1; save_position=7`
- notes: Count can be produced by current source write-count model; branch conditions still need manual proof.

### Original item group 11

- original call count: `1`
- call index range: `946` → `946`
- call address range: `0x80054dd8` → `0x80054dd8`
- candidate source rows: `31-32`
- candidate context: `frame number / hit points tail`
- count status: `representable-count-needs-control-flow-proof`
- matching source cases: `save_hitpoints=1`
- notes: Count can be produced by current source write-count model; branch conditions still need manual proof.

### Original item group 12

- original call count: `7`
- call index range: `988` → `1019`
- call address range: `0x80054e80` → `0x80054efc`
- candidate source rows: `17-32`
- candidate context: `item serialization final variant`
- count status: `representable-count-needs-control-flow-proof`
- matching source cases: `save_position=6 + save_hitpoints=1; save_position=7`
- notes: Count can be produced by current source write-count model; branch conditions still need manual proof.

## Verdict

RE-014 finds source-level gaps in the item serializer model. In particular, the active item branch assembles `word = 0x8000` but does not currently write that control word, and `obj->save_flags` has no serialized writes. Groups whose counts are representable still require branch/control-flow proof; groups whose counts are not representable need source-vs-original reconciliation before any `(F)`, `(D)`, or `(**)` marker.
