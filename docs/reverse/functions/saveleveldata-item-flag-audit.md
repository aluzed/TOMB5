# SaveLevelData item flag audit

Status: Generated
Story: `docs/stories/RE-015-saveleveldata-active-item-serialization.md`

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
- possible current-source active branch counts: `1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17`
- active control word written: `yes`
- save_flags write sites: `1`
- unrepresented original item groups: `none`
- status: `counts-representable-needs-proof`

## Source count model

The active/full-save item branch is modeled as:

- `save_position`: absent, or 5 required writes plus up to 4 optional writes (`x_rot`, `z_rot`, `speed`, `fallspeed`).
- `save_anim`: absent, or 5 writes (`current`, `goal`, `required`, anim number/byte, frame).
- `save_hitpoints`: absent, or 1 write.
- `save_flags`: absent, or one packed 32-bit write (`flags` plus active/status bitfield low 15 bits).
- active branch control word: written once after `word` is assembled and before optional payload fields.

## Item group comparison

### Original item group 4

- original call count: `17`
- call index range: `338` → `441`
- call address range: `0x80054458` → `0x800545f4`
- candidate source rows: `17-26`
- candidate context: `item header/position block and optional speed/fallspeed writes`
- count status: `representable-count-needs-control-flow-proof`
- matching source cases: `active_header=1 + save_position=9 + save_anim=5 + save_hitpoints=1 + save_flags=1`
- notes: Count can be produced by current source write-count model; branch conditions still need manual proof.

### Original item group 5

- original call count: `15`
- call index range: `501` → `600`
- call address range: `0x800546e4` → `0x80054870`
- candidate source rows: `17-34`
- candidate context: `item active/full-save branch variant`
- count status: `representable-count-needs-control-flow-proof`
- matching source cases: `active_header=1 + save_position=7 + save_anim=5 + save_hitpoints=1 + save_flags=1; active_header=1 + save_position=8 + save_anim=5 + save_flags=1; active_header=1 + save_position=8 + save_anim=5 + save_hitpoints=1; active_header=1 + save_position=9 + save_anim=5`
- notes: Count can be produced by current source write-count model; branch conditions still need manual proof.

### Original item group 6

- original call count: `3`
- call index range: `635` → `645`
- call address range: `0x800548fc` → `0x80054924`
- candidate source rows: `27-34`
- candidate context: `item animation, hitpoint, and flags fields`
- count status: `representable-count-needs-control-flow-proof`
- matching source cases: `active_header=1 + save_hitpoints=1 + save_flags=1`
- notes: Count can be produced by current source write-count model; branch conditions still need manual proof.

### Original item group 7

- original call count: `1`
- call index range: `698` → `698`
- call address range: `0x800549f8` → `0x800549f8`
- candidate source rows: `17-34`
- candidate context: `item serialization alternate control-flow region`
- count status: `representable-count-needs-control-flow-proof`
- matching source cases: `active_header=1`
- notes: Count can be produced by current source write-count model; branch conditions still need manual proof.

### Original item group 8

- original call count: `12`
- call index range: `750` → `800`
- call address range: `0x80054ac8` → `0x80054b90`
- candidate source rows: `17-34`
- candidate context: `item serialization dense call region`
- count status: `representable-count-needs-control-flow-proof`
- matching source cases: `active_header=1 + save_position=5 + save_anim=5 + save_flags=1; active_header=1 + save_position=5 + save_anim=5 + save_hitpoints=1; active_header=1 + save_position=6 + save_anim=5; active_header=1 + save_position=9 + save_hitpoints=1 + save_flags=1`
- notes: Count can be produced by current source write-count model; branch conditions still need manual proof.

### Original item group 9

- original call count: `1`
- call index range: `841` → `841`
- call address range: `0x80054c34` → `0x80054c34`
- candidate source rows: `30-34`
- candidate context: `lara/non-lara anim-number, frame, hitpoint, flags tail`
- count status: `representable-count-needs-control-flow-proof`
- matching source cases: `active_header=1`
- notes: Count can be produced by current source write-count model; branch conditions still need manual proof.

### Original item group 10

- original call count: `7`
- call index range: `885` → `916`
- call address range: `0x80054ce4` → `0x80054d60`
- candidate source rows: `17-34`
- candidate context: `item serialization second variant`
- count status: `representable-count-needs-control-flow-proof`
- matching source cases: `active_header=1 + save_anim=5 + save_flags=1; active_header=1 + save_anim=5 + save_hitpoints=1; active_header=1 + save_position=5 + save_flags=1; active_header=1 + save_position=5 + save_hitpoints=1; active_header=1 + save_position=6`
- notes: Count can be produced by current source write-count model; branch conditions still need manual proof.

### Original item group 11

- original call count: `1`
- call index range: `946` → `946`
- call address range: `0x80054dd8` → `0x80054dd8`
- candidate source rows: `32-34`
- candidate context: `frame number / hit points / flags tail`
- count status: `representable-count-needs-control-flow-proof`
- matching source cases: `active_header=1`
- notes: Count can be produced by current source write-count model; branch conditions still need manual proof.

### Original item group 12

- original call count: `7`
- call index range: `988` → `1019`
- call address range: `0x80054e80` → `0x80054efc`
- candidate source rows: `17-34`
- candidate context: `item serialization final variant`
- count status: `representable-count-needs-control-flow-proof`
- matching source cases: `active_header=1 + save_anim=5 + save_flags=1; active_header=1 + save_anim=5 + save_hitpoints=1; active_header=1 + save_position=5 + save_flags=1; active_header=1 + save_position=5 + save_hitpoints=1; active_header=1 + save_position=6`
- notes: Count can be produced by current source write-count model; branch conditions still need manual proof.

## Verdict

RE-015 resolves the source-level count gaps that RE-014 identified: the active item branch now writes the control word, and `obj->save_flags` now serializes one packed 32-bit flags word. The original item groups are therefore representable by source write counts, including groups `4` and `6`; this is still a count-level result, not a control-flow equivalence proof, so no `(F)`, `(D)`, or `(**)` marker is justified yet.
