# RE-213 post-module-spec_psxpc_n domain selection

## Progress tracker

- [x] RE-212 module-spec_psxpc_n exhaustion handoff consumed.
- [x] Closed/exhausted domains excluded from the next-domain shortlist.
- [x] Ranked metadata-only next-domain rows emitted.
- [x] Proof-first next ticket selected without source or marker changes.

## Decision

- Upstream status: `module-spec-psxpc-n-exhausted`
- Closed/exhausted domains excluded: `module-spec_psxpc_n`
- Selected next domain: `maths-render-support`
- Selected pivot: `mTranslateXYZ`
- Recommended next ticket: `RE-214`
- Code-change readiness: `documentation-only-selection-gate`

No production source or marker change is authorized by this selection gate.

## Ranked candidates

- #1 `maths-render-support` / `mTranslateXYZ` (92 candidates): open RE-214 maths-render-support proof-first audit; readiness `blocked`.
- #2 `traps-switches-doors` / `ControlRollingBall` (20 candidates): defer until higher-ranked post-module-spec_psxpc_n domain is selected; readiness `blocked`.
- #3 `module-spec_psxpc` / `PrintString` (28 candidates): defer until higher-ranked post-module-spec_psxpc_n domain is selected; readiness `blocked`.
- #4 `module-spec_psx` / `main` (12 candidates): defer until higher-ranked post-module-spec_psxpc_n domain is selected; readiness `blocked`.
- #5 `lara-combat` / `DoProperDetection` (10 candidates): defer until higher-ranked post-module-spec_psxpc_n domain is selected; readiness `blocked`.
- #6 `inventory` / `S_CallInventory2` (11 candidates): defer until higher-ranked post-module-spec_psxpc_n domain is selected; readiness `blocked`.
- #7 `input` / `S_UpdateInput` (3 candidates): defer until higher-ranked post-module-spec_psxpc_n domain is selected; readiness `blocked`.
- #8 `camera` / `CalculateSpotCams` (4 candidates): defer until higher-ranked post-module-spec_psxpc_n domain is selected; readiness `blocked`.

## Next proof

Open `RE-214` as a proof-first audit for `maths-render-support` before any source reconstruction or marker update.
