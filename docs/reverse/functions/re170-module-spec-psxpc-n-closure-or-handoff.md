# RE-170 module SPEC_PSXPC_N closure or handoff

## Progress tracker

- [x] RE-169 geometry-support handoff consumed.
- [x] Geometry-support scope loaded from RE-163 audit rows.
- [x] Domain closure denied because selected cluster still needs proof.
- [x] Bounded RE-171..RE-177 follow-up plan emitted.
- [x] No source or marker changes authorized.

## Decision

- domain: `module-spec_psxpc_n`
- selected cluster: `geometry-support`
- selected pivot: `GetBoundsAccurate`
- domain decision: `module-spec-psxpc-n-not-closed-geometry-support-proof-chain-opened`
- next ticket: `RE-171` `geometry-support-proof-first-audit`
- code-change readiness: `documentation-only-handoff-gate`
- source-patch-ready rows: `0`
- marker-ready rows: `0`

No production source or marker change is authorized by this gate.

## Geometry-support scope

- `GetBoundsAccurate` in `SPEC_PSXPC_N/CALCLARA.C`: `pivot`, source `decompiled`, patch `denied`.
- `CalcClipWindow_ONGTE` in `SPEC_PSXPC_N/BUBBLES.C`: `supporting-candidate`, source `decompiled`, patch `denied`.
- `InterpolateMatrix_CL` in `SPEC_PSXPC_N/CALCLARA.C`: `supporting-candidate`, source `decompiled`, patch `denied`.
- `GetFrames_CL` in `SPEC_PSXPC_N/CALCLARA.C`: `supporting-candidate`, source `decompiled`, patch `denied`.
- `GetBestFrame` in `SPEC_PSXPC_N/CALCLARA.C`: `supporting-candidate`, source `decompiled`, patch `denied`.
- `GetChange` in `SPEC_PSXPC_N/CONTROL_S.C`: `supporting-candidate`, source `decompiled`, patch `denied`.
- `DecodeTrack` in `SPEC_PSXPC_N/DELTAPAK_S.C`: `supporting-candidate`, source `decompiled`, patch `denied`.

## Follow-up plan

- `RE-171` `geometry-support-proof-first-audit` — Open the geometry-support proof chain and publish exact scope, pivot, blockers, and source-backed inventory. Exit: proof-first audit emitted with no source or marker changes.
- `RE-172` `geometry-support-caller-state-map` — Map source-backed callers, state surfaces, return-value consumers, and helper dependencies for geometry-support rows. Exit: Caller/state map published with no synthetic edges.
- `RE-173` `geometry-support-argument-taxonomy` — Classify coordinate, frame, bounds, and track argument families into stable metadata categories. Exit: Taxonomy separates source-backed shapes from unproven runtime assumptions.
- `RE-174` `geometry-support-state-contract` — Document structure, matrix, frame, and bounds state contracts required before reconstruction or marker updates. Exit: State contract either unblocks comparison or records exact blockers.
- `RE-175` `geometry-support-equivalence-gate` — Compare source-level contract rows against non-raw binary metadata without versioning raw evidence. Exit: Readiness matrix names ready rows or remains blocked.
- `RE-176` `geometry-support-source-patch-gate` — Apply a minimal patch only if RE-175 marks rows ready; otherwise emit a no-patch gate. Exit: Patch/build/tests pass or no-patch blocker is published.
- `RE-177` `module-spec-psxpc-n-post-geometry-next-cluster-selection` — Select the next SPEC_PSXPC_N cluster after geometry-support closes or blocks. Exit: Next cluster or domain handoff artifact names the next objective.

## Handoff

- next ticket: `RE-171`
- next topic: `geometry-support-proof-first-audit`
- reason: `module SPEC_PSXPC_N remains open; geometry-support needs caller/state and non-raw equivalence proof before source or marker changes`
