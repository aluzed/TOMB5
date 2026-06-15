# RE-162 post-module-game domain reprioritization

## Progress tracker

- [x] RE-161 module-game exhaustion handoff consumed.
- [x] Closed domains excluded from the next-domain shortlist.
- [x] Ranked metadata-only next-domain rows emitted.
- [x] Proof-first next ticket selected without source or marker changes.

## Decision

- Upstream status: `module-game-exhausted`
- Closed domains excluded: `audio-effects, collision, module-game`
- Selected next domain: `module-spec_psxpc_n`
- Selected pivot: `PrintString`
- Recommended next ticket: `RE-163`
- Code-change readiness: `documentation-only-selection-gate`

No production source or marker change is authorized by this selection gate.

## Ranked candidates

- #1 `module-spec_psxpc_n` / `PrintString` (27 candidates): open RE-163 module-spec_psxpc_n proof-first audit; readiness `blocked`.
- #2 `maths-render-support` / `mTranslateXYZ` (92 candidates): defer until higher-ranked post-module-game domain is selected; readiness `blocked`.
- #3 `traps-switches-doors` / `ControlRollingBall` (20 candidates): defer until higher-ranked post-module-game domain is selected; readiness `blocked`.
- #4 `module-spec_psxpc` / `PrintString` (28 candidates): defer until higher-ranked post-module-game domain is selected; readiness `blocked`.
- #5 `module-spec_psx` / `main` (12 candidates): defer until higher-ranked post-module-game domain is selected; readiness `blocked`.
- #6 `lara-combat` / `DoProperDetection` (10 candidates): defer until higher-ranked post-module-game domain is selected; readiness `blocked`.
- #7 `inventory` / `S_CallInventory2` (11 candidates): defer until higher-ranked post-module-game domain is selected; readiness `blocked`.
- #8 `input` / `S_UpdateInput` (3 candidates): defer until higher-ranked post-module-game domain is selected; readiness `blocked`.
- #9 `camera` / `CalculateSpotCams` (4 candidates): defer until higher-ranked post-module-game domain is selected; readiness `blocked`.

## Next proof

Open `RE-163` as a proof-first audit for `module-spec_psxpc_n` before any source reconstruction or marker update.
