# Save/Restore level data audit

Date: 2026-06-14
Story: `docs/stories/RE-009-savegame-level-data-audit.md`
Status: Done

## Progress tracker

- [x] Dump `RestoreLevelData` from the verified original payload.
- [x] Dump `SaveLevelData` from the verified original payload.
- [x] Self-compare both dumps to validate the extraction/diff path.
- [x] Audit current source state in `GAME/SAVEGAME.C`.
- [x] Record an actionable verdict without committing original bytes/instructions.

## Versioning rule

The generated dump files contain original game instructions and machine words. They are intentionally kept under ignored paths:

```text
build/reverse/re007/original/
build/reverse/re007/compare/
```

Do not commit those dumps. This report only records metadata, call targets, and conclusions.

## Inputs

- Mapping: `docs/reverse/generated/repo-function-map.csv`
- Backlog: `docs/reverse/backlog.md`
- Source: `GAME/SAVEGAME.C`
- Extraction tool: `scripts/reverse/disasm_extract.py`
- Comparison tool: `scripts/reverse/compare_function.py`
- Original payload: `build/reverse/extracted/SLUS_013.11.payload.bin` (ignored)

## Commands run

```bash
python3 scripts/reverse/disasm_extract.py RestoreLevelData
python3 scripts/reverse/disasm_extract.py SaveLevelData
python3 scripts/reverse/compare_function.py \
  build/reverse/re007/original/SaveLevelData_80053f10.csv \
  build/reverse/re007/original/SaveLevelData_80053f10.csv \
  --name SaveLevelData_selftest
python3 scripts/reverse/compare_function.py \
  build/reverse/re007/original/RestoreLevelData_80054f6c.csv \
  build/reverse/re007/original/RestoreLevelData_80054f6c.csv \
  --name RestoreLevelData_selftest
```

Self-test result:

- `SaveLevelData_selftest`: `exact_match=yes`, `differences=0`, `total=1047`.
- `RestoreLevelData_selftest`: `exact_match=yes`, `differences=0`, `total=1020`.

## Function summary

### `RestoreLevelData`

- Source: `GAME/SAVEGAME.C:82`
- Final PSX address: `0x80054f6c`
- Ghidra: `0x80054f6c` / `FUN_80054f6c`
- Body size: `4080` bytes
- Dumped instruction count: `1020`
- Backlog priority: `P0`, rank `#1`
- Runtime focus: yes
- Current source state: only `UNIMPLEMENTED();`

Observed call targets from the original function:

- `ReadSG` — 79 calls
- `AlterFloorHeight` — 4 calls
- `GetFloor` — 2 calls
- `GetHeight` — 2 calls
- `AddActiveItem` — 2 calls
- `TestTriggers` — 1 call
- `KillItem` — 1 call
- `ItemNewRoom` — 1 call
- `EnableBaddieAI` — 1 call
- `CreateItem` — 1 call
- `InitialiseItem` — 1 call
- `0x8001f9e8` — 1 unmapped call target in the current mapping

Interpretation:

- This is not a small wrapper; the original is a large restore routine with many serialized fields and several state-reconstruction calls.
- The dominant helper is `ReadSG`, which mirrors the save stream writer used by `SaveLevelData`.
- The current C body has no implementation, so no source-level equivalence claim can be made yet.

Verdict:

- `(**)`: no — no rebuilt comparable artifact and source is unimplemented.
- `(F)`: no — source does not implement the original behavior.
- `(D)`: no — no functional/runtime validation and source is unimplemented.
- `(ND)`: not currently present on this function; do not add/remove markers based on this audit alone.

### `SaveLevelData`

- Source: `GAME/SAVEGAME.C:100`
- Final PSX address: `0x80053f10`
- Ghidra: `0x80053f10` / `FUN_80053f10`
- Body size: `4188` bytes
- Dumped instruction count: `1047`
- Backlog priority: `P0`, rank `#2`
- Runtime focus: yes
- Current source state:
  - PC branch contains a partial level-save implementation.
  - PSX/non-PC branch is still `UNIMPLEMENTED();` with `// todo check for psx`.

Observed call targets from the original function:

- `WriteSG` — 81 calls

Interpretation:

- The original function is a large serializer dominated by repeated writes through `WriteSG`.
- The current source already documents many PC-side serialized fields, flags, item fields, camera/spotcam flags, and object save flags.
- The PSX path, which is the path relevant to the verified original payload, remains unimplemented in source.
- Because the extracted original has 1047 instructions and the PSX branch currently compiles to the `UNIMPLEMENTED()` placeholder path, the current PSX source cannot be marked equivalent.

Verdict:

- `(**)`: no — no rebuilt comparable artifact and PSX source path is unimplemented.
- `(F)`: no for PSX — the PC branch is not sufficient proof for the PSX original.
- `(D)`: no — no functional/runtime validation of PSX save behavior.
- `(ND)`: not currently present on this function; do not add/remove markers based on this audit alone.

## Key source findings

`GAME/SAVEGAME.C` currently has asymmetric save/restore coverage:

- `sgRestoreGame` calls `RestoreLevelData(1)` and `RestoreLaraData(1)`.
- `sgSaveGame` calls `SaveLevelData(1)` and `SaveLaraData()`.
- `RestoreLaraData`, `SaveLaraData`, `ReadSG`, and `WriteSG` are already marked `(F)`.
- `RestoreLevelData` is wholly unimplemented.
- `SaveLevelData` is implemented only under `#if PC_VERSION`; the PSX-relevant `#else` branch remains unimplemented.

This means the next meaningful work is implementation/reconstruction, not marker cleanup.

## Recommended next ticket

Create an implementation ticket for the PSX save/restore stream:

1. Use the existing PC `SaveLevelData` branch as a field-order hypothesis.
2. Reconstruct the PSX `SaveLevelData` write sequence against the original `WriteSG` call count and control-flow shape.
3. Reconstruct `RestoreLevelData` as the inverse `ReadSG` stream.
4. Resolve the one unmapped call target in `RestoreLevelData` (`0x8001f9e8`) before claiming completeness.
5. Add a non-versioned comparison checklist under `build/reverse/re007/` for every reconstruction attempt.
6. Only then consider adding `(F)`; reserve `(**)` until a rebuilt binary/object comparison exists.

RE-010 produced the first versionable stream schema from the current PC `SaveLevelData` branch. RE-011 then removed the PSX `UNIMPLEMENTED()` fallback by making the existing `SaveLevelData` stream implementation compile for PSX/PSXPC_N:

- `scripts/reverse/savegame_schema.py`
- `docs/reverse/generated/savegame-level-data-schema.csv`
- `docs/reverse/generated/savegame-level-data-schema.md`
- `tests/reverse/test_savegame_source.py`

Suggested next story id: `RE-012 — Audit SaveLevelData against the original dump`.
