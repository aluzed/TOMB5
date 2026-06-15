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

RE-012 produced a versionable original-dump metadata audit in `docs/reverse/functions/saveleveldata-original-audit.md`:

- original `WriteSG` calls in `SaveLevelData`: `81`
- source-level static `Write(...)` sites: `34`
- current verdict: `needs-control-flow-audit`

RE-013 then generated the first versionable call-group map:

- `docs/reverse/generated/saveleveldata-write-call-map.csv`
- `docs/reverse/functions/saveleveldata-write-call-map.md`
- original call groups: `12`
- status: `candidate-map-needs-manual-audit`

RE-014 audited the item-serialization groups against the then-current source flag model:

- `docs/reverse/generated/saveleveldata-item-flag-audit.csv`
- `docs/reverse/functions/saveleveldata-item-flag-audit.md`
- item candidate groups: `9`
- original item-group `WriteSG` calls: `64`
- original groups `4` and `6` were not representable before RE-015
- source gaps found by RE-014: active branch control word assembled but not written; `obj->save_flags` had no `Write(...)` sites

RE-015 reconstructed the active item count gaps in source:

- active/full-save item branch now writes the `word` control header before optional payload fields
- `obj->save_flags` now writes one packed 32-bit flags word
- source-level static `Write(...)` sites: `34`
- item count model status: `counts-representable-needs-proof`
- unrepresented item groups by count: `none`

RE-016 compared the original item `WriteSG` groups against exact size sequences derived from safe call metadata:

- `docs/reverse/generated/saveleveldata-item-control-flow-audit.csv`
- `docs/reverse/functions/saveleveldata-item-control-flow-audit.md`
- item groups covered: `9`
- exact size-sequence match groups: `12`
- mismatch groups: `4, 5, 6, 7, 8, 9, 10, 11`
- status: `control-flow-gaps-found`

RE-017 reconciled the mismatched item groups into a source-vs-original field/width hypothesis table:

- `docs/reverse/generated/saveleveldata-item-field-width-audit.csv`
- `docs/reverse/functions/saveleveldata-item-field-width-audit.md`
- mismatch groups covered: `4, 5, 6, 7, 8, 9, 10, 11`
- original calls classified: `57`
- exact field-width matches: `26`
- source width mismatches: `3`
- source missing fields: `21`
- source layout mismatches: `4`
- branch/sentinel groups: `3`
- status: `field-width-gaps-found`

RE-018 checked those hypotheses against current restore-side source support:

- `docs/reverse/generated/saveleveldata-restore-side-audit.csv`
- `docs/reverse/functions/saveleveldata-restore-side-audit.md`
- `RestoreLevelData` source status: `source-unimplemented`
- hypotheses audited: `57`
- priority hypotheses: `34`
- patch-ready hypotheses: `0`
- status: `restore-side-proof-missing`

RE-019 extracted a metadata-only original `RestoreLevelData` `ReadSG` call map and compared the RE-017 item groups against restore read size sequences:

- `docs/reverse/generated/restoreleveldata-read-call-map.csv`
- `docs/reverse/functions/restoreleveldata-read-call-map.md`
- original `ReadSG` calls: `79`
- restore read groups: `10`
- RE-017 item groups compared: `8`
- groups with size-only restore match: `4`
- patch-ready groups: `0`
- status: `restore-size-proof-partial`

RE-020 then derived a stronger metadata-only restore-side field/control-flow proof matrix for the priority item groups:

- `docs/reverse/generated/restoreleveldata-field-control-flow-proof.csv`
- `docs/reverse/functions/restoreleveldata-field-control-flow-proof.md`
- priority groups covered: `4, 5, 8, 10`
- proof rows: `4`
- patch-ready groups: `0`
- status: `restore-field-control-flow-proof-partial`

RE-020 findings:

- group `4`: candidate restore regions `4;5`, but repeated 2-byte fields and split control-flow still block field/predicate proof.
- group `5`: rare payload anchors `24,20` exist in restore group `6`, but packed flags and separate item flag/timer/trigger payload predicates remain unproved.
- group `8`: rare payload anchors `20,4` exist in restore group `8`, but extra restore bytes and layout mismatches still block field equivalence.
- group `10`: exact size window exists in restore group `9`, but exact size is still not predicate proof.

RE-021 then mapped metadata-only branch/predicate shapes around the candidate restore regions:

- `docs/reverse/generated/restoreleveldata-branch-predicate-map.csv`
- `docs/reverse/functions/restoreleveldata-branch-predicate-map.md`
- restore groups covered: `4, 5, 6, 8, 9`
- proof rows: `5`
- patch-ready groups: `0`
- status: `restore-branch-predicate-map-partial`

RE-021 findings:

- restore groups `4` and `5` link to save group `4`; both are branch-rich split candidates, not field identity proof.
- restore group `6` links to save group `5`; rare payload anchors sit in a compact branch envelope, but optional payload predicates remain unknown.
- restore group `8` links to save group `8`; object/layout payload anchors sit inside branch fanout with extra restore bytes and unresolved field identity.
- restore group `9` links to save group `10`; exact read-size window still lacks field predicate identity.

RE-022 then reconciled the RE-020/RE-021 restore candidates with source field identities and optional predicate families:

- `docs/reverse/generated/restoreleveldata-field-predicate-reconciliation.csv`
- `docs/reverse/functions/restoreleveldata-field-predicate-reconciliation.md`
- save groups covered: `4, 5, 8, 10`
- proof rows: `4`
- patch-ready groups: `0`
- status: `restore-field-predicate-reconciliation-partial`

RE-022 findings:

- save group `4`: `14` matched fields and `3` unresolved width mismatches; split restore groups `4;5` still block predicate identity.
- save group `5`: only the packed flags word is source-backed; `14` separate flag/timer/trigger/object payload fields remain unresolved.
- save group `8`: `5` matched fields and `7` unresolved layout/payload fields; extra restore bytes and item flag predicates still block equivalence.
- save group `10`: `6` matched fields and `1` room/layout mismatch; exact size window remains weaker than predicate proof.

Suggested next story: build a restore implementation plan only after missing payload predicates and layout blockers have source-level proof. Current field/predicate reconciliation is insufficient for serializer patching or `(F)`, `(D)`, or `(**)` markers.

RE-023 converted the RE-022 blockers into a metadata-only implementation readiness plan:

- `docs/reverse/generated/restoreleveldata-implementation-plan.csv`
- `docs/reverse/functions/restoreleveldata-implementation-plan.md`
- save groups covered: `4, 5, 8, 10`
- plan rows: `4`
- patch-ready groups: `0`
- code-change-ready groups: `0`
- status: `restoreleveldata-implementation-plan-blocked`

RE-023 recommended proof-first follow-ups:

- RE-024: prove the room/layout predicate window for save group `10` and the split active item predicate path for save group `4`.
- RE-025: prove item flag, timer, trigger, and object extension payload predicates for save group `5`.
- RE-026: prove object subtype/layout fanout and extra restore bytes for save group `8`.

Current next story: RE-024. Do not patch `GAME/SAVEGAME.C` or add `(F)`, `(D)`, or `(**)` until one of the readiness rows becomes code-change-ready.

RE-024 narrowed the first proof target into a metadata-only room/split predicate matrix:

- `docs/reverse/generated/restoreleveldata-room-split-predicate-proof.csv`
- `docs/reverse/functions/restoreleveldata-room-split-predicate-proof.md`
- target save groups: `10, 4`
- proof rows: `2`
- code-change-ready groups: `0`
- status: `restoreleveldata-room-split-proof-partial`

RE-024 findings:

- save group `10`: exact-size window remains useful but room byte order/layout predicate is still unproved.
- save group `4`: split restore groups `4;5` and anim-state byte-vs-word predicates remain unproved.

RE-025 then narrowed save group `5` into a metadata-only payload predicate matrix:

- `docs/reverse/generated/restoreleveldata-group5-payload-predicate-proof.csv`
- `docs/reverse/functions/restoreleveldata-group5-payload-predicate-proof.md`
- target save group: `5`
- restore group: `6`
- payload rows: `5`
- code-change-ready payload families: `0`
- status: `restoreleveldata-group5-payload-proof-blocked`

RE-025 findings:

- packed status flags are source-backed only as a group anchor.
- `item_flags[0..3]`, `timer`, and `trigger_flags` have visible header-bit predicates, but their separate payload bodies and restore assignments remain unproved.
- object-extension payloads total `8` rows / `56` bytes with rare blocks `24,20`, but no source predicate or field identity is proven.

RE-026 then narrowed save group `8` into a metadata-only layout/fanout predicate matrix:

- `docs/reverse/generated/restoreleveldata-group8-layout-fanout-proof.csv`
- `docs/reverse/functions/restoreleveldata-group8-layout-fanout-proof.md`
- target save group: `8`
- restore group: `8`
- fanout rows: `7`
- code-change-ready fanout families: `0`
- status: `restoreleveldata-group8-layout-fanout-proof-blocked`

RE-026 findings:

- subtype byte and extra restore byte candidate remain without source predicate identity.
- layout block `20` and room/rotation ordering still conflict with the current split source representation.
- speed/fallspeed and anim-state widths are source-visible, but still blocked by the enclosing fanout/layout predicate.
- item data word has no source field identity.
- item flag payload bodies inherit the RE-025 `group5-item-flag-payloads-blocked` dependency.

RE-027 then refreshed the global `RestoreLevelData` readiness matrix from RE-024, RE-025, and RE-026:

- `docs/reverse/generated/restoreleveldata-readiness-refresh.csv`
- `docs/reverse/functions/restoreleveldata-readiness-refresh.md`
- source proof inputs: `RE-024, RE-025, RE-026`
- target save groups: `4, 5, 8, 10`
- readiness rows: `4`
- code-change-ready groups: `0`
- status: `restoreleveldata-readiness-refresh-blocked`

RE-027 findings:

- save group `4`: split restore groups and anim-state byte-vs-word predicate remain blocked.
- save group `5`: item_flags/timer/trigger payload bodies and object-extension field identity remain blocked.
- save group `8`: subtype/extra byte, layout block `20`, room/rotation ordering, item data word, and item flag payload bodies remain blocked.
- save group `10`: room byte order/layout predicate remains blocked.

RE-028 then selected the highest-value blocked family, save group `5` / restore group `6`, and produced a source-field identity checklist:

- `docs/reverse/generated/restoreleveldata-group5-source-field-identity-checklist.csv`
- `docs/reverse/functions/restoreleveldata-group5-source-field-identity-checklist.md`
- source inputs: `RE-017, RE-025, GAME/SAVEGAME.C`
- checklist rows: `5`
- patch-ready checklist rows: `0`
- status: `restoreleveldata-group5-source-field-identity-checklist-blocked`

RE-028 findings:

- packed status flags are source-backed only as a payload-cluster anchor.
- `item_flags[0..3]`, `timer`, and `trigger_flags` have header predicates in source but lack separate payload write bodies and restore assignment identity.
- object-extension payloads remain without named source field identities or object predicate mapping.

Current next story: RE-029. Prove one group `5` payload-body family end-to-end, starting with `item_flags[0..3]` if source identities can be recovered without publishing raw dump payloads. Do not patch `GAME/SAVEGAME.C` or add `(F)`, `(D)`, or `(**)` until a checklist row becomes code-change-ready.
