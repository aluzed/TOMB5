# SaveLevelData WriteSG call-group map

Status: Generated
Story: `docs/stories/RE-013-saveleveldata-write-call-map.md`

## Progress tracker

- [x] Group original `WriteSG` calls by instruction-index gaps.
- [x] Attach conservative source `Write(...)` candidate row spans.
- [x] Keep original instruction rows and machine words out of versioned outputs.
- [x] State that this is not an equivalence marker proof.

## Inputs

- Source: `GAME/SAVEGAME.C`
- Original dump CSV: `build/reverse/re007/original/SaveLevelData_80053f10.csv` (ignored; not versioned)
- `WriteSG` final PSX address: `0x80053b04`
- Grouping gap threshold: `24` instruction indices

## Summary

- original `WriteSG` calls: `81`
- original call groups: `12`
- source `Write(...)` sites: `34`
- status: `candidate-map-needs-manual-audit`

## Candidate map

The `first/last_call_*` columns are metadata coordinates only. This report does not include the original instruction text or machine words.

### Original call group 1

- original call count: `9`
- call index range: `13` → `71`
- call address range: `0x80053f44` → `0x8005402c`
- candidate source rows: `1-9`
- candidate context: `global state, flipmap loop, flip status, cd flags, atmosphere`
- confidence: `medium`
- notes: front-loaded top-level serializer fields

### Original call group 2

- original call count: `7`
- call index range: `106` → `179`
- call address range: `0x800540b8` → `0x800541dc`
- candidate source rows: `10-15`
- candidate context: `room static flags, sequence byte, camera flags, spotcam flags`
- confidence: `low`
- notes: contains runtime-count loops; verify control-flow boundaries

### Original call group 3

- original call count: `1`
- call index range: `218` → `218`
- call address range: `0x80054278` → `0x80054278`
- candidate source rows: `16`
- candidate context: `level item killed marker`
- confidence: `low`
- notes: single killed-item branch candidate

### Original call group 4

- original call count: `17`
- call index range: `338` → `441`
- call address range: `0x80054458` → `0x800545f4`
- candidate source rows: `17-26`
- candidate context: `item header/position block and optional speed/fallspeed writes`
- confidence: `low`
- notes: candidate item save_position branch after RE-015 header insertion

### Original call group 5

- original call count: `15`
- call index range: `501` → `600`
- call address range: `0x800546e4` → `0x80054870`
- candidate source rows: `17-34`
- candidate context: `item active/full-save branch variant`
- confidence: `low`
- notes: same source rows can compile into several original call regions

### Original call group 6

- original call count: `3`
- call index range: `635` → `645`
- call address range: `0x800548fc` → `0x80054924`
- candidate source rows: `27-34`
- candidate context: `item animation, hitpoint, and flags fields`
- confidence: `low`
- notes: candidate save_anim/save_hitpoints/save_flags branch

### Original call group 7

- original call count: `1`
- call index range: `698` → `698`
- call address range: `0x800549f8` → `0x800549f8`
- candidate source rows: `17-34`
- candidate context: `item serialization alternate control-flow region`
- confidence: `low`
- notes: requires size-sequence/control-flow audit

### Original call group 8

- original call count: `12`
- call index range: `750` → `800`
- call address range: `0x80054ac8` → `0x80054b90`
- candidate source rows: `17-34`
- candidate context: `item serialization dense call region`
- confidence: `low`
- notes: largest repeated candidate item region

### Original call group 9

- original call count: `1`
- call index range: `841` → `841`
- call address range: `0x80054c34` → `0x80054c34`
- candidate source rows: `30-34`
- candidate context: `lara/non-lara anim-number, frame, hitpoint, flags tail`
- confidence: `low`
- notes: tail branch candidate

### Original call group 10

- original call count: `7`
- call index range: `885` → `916`
- call address range: `0x80054ce4` → `0x80054d60`
- candidate source rows: `17-34`
- candidate context: `item serialization second variant`
- confidence: `low`
- notes: requires mapping against item/object flags

### Original call group 11

- original call count: `1`
- call index range: `946` → `946`
- call address range: `0x80054dd8` → `0x80054dd8`
- candidate source rows: `32-34`
- candidate context: `frame number / hit points / flags tail`
- confidence: `low`
- notes: late item tail candidate

### Original call group 12

- original call count: `7`
- call index range: `988` → `1019`
- call address range: `0x80054e80` → `0x80054efc`
- candidate source rows: `17-34`
- candidate context: `item serialization final variant`
- confidence: `low`
- notes: final original call group before function return

## Verdict

This map is a triage artifact, not an equivalence proof. The repeated item-serialization regions need manual control-flow audit before `SaveLevelData` can receive `(F)`, `(D)`, or `(**)`.
