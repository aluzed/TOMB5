# RE-170 — Module SPEC_PSXPC_N closure or handoff

Status: Done

## Goal

Consume the RE-169 next-cluster selection and either close module SPEC_PSXPC_N or hand off a bounded geometry-support proof chain.

## Scope

- depends on: `RE-169`, `RE-163`
- safety contract: metadata-only closure/handoff decision; source and marker edits stay blocked

## Progress tracker

- [x] RE-169 geometry-support handoff consumed.
- [x] RE-163 geometry-support scope consumed.
- [x] domain closure denied while proof blockers remain.
- [x] RE-171..RE-177 follow-up plan emitted.
- [x] Forbidden evidence excluded from generated artifacts.

## Generated artifacts

- `docs/reverse/generated/re170-module-spec-psxpc-n-geometry-support-scope.csv`
- `docs/reverse/generated/re170-geometry-support-ticket-plan.csv`
- `docs/reverse/generated/re170-module-spec-psxpc-n-closure-or-handoff.csv`
- `docs/reverse/generated/re170-geometry-support-handoff.csv`
- `docs/reverse/functions/re170-module-spec-psxpc-n-closure-or-handoff.md`

## Findings

- selected cluster: `geometry-support`
- selected pivot: `GetBoundsAccurate`
- domain closure denied: selected cluster still lacks caller/state and non-raw equivalence proof
- source-patch-ready rows: `0`
- marker-ready rows: `0`

## Follow-up ticket breakdown

- `RE-171` `geometry-support-proof-first-audit`: Open the geometry-support proof chain and publish exact scope, pivot, blockers, and source-backed inventory.
- `RE-172` `geometry-support-caller-state-map`: Map source-backed callers, state surfaces, return-value consumers, and helper dependencies for geometry-support rows.
- `RE-173` `geometry-support-argument-taxonomy`: Classify coordinate, frame, bounds, and track argument families into stable metadata categories.
- `RE-174` `geometry-support-state-contract`: Document structure, matrix, frame, and bounds state contracts required before reconstruction or marker updates.
- `RE-175` `geometry-support-equivalence-gate`: Compare source-level contract rows against non-raw binary metadata without versioning raw evidence.
- `RE-176` `geometry-support-source-patch-gate`: Apply a minimal patch only if RE-175 marks rows ready; otherwise emit a no-patch gate.
- `RE-177` `module-spec-psxpc-n-post-geometry-next-cluster-selection`: Select the next SPEC_PSXPC_N cluster after geometry-support closes or blocks.

## Readiness decision

- decision: `module-spec-psxpc-n-not-closed-geometry-support-proof-chain-opened`
- code change readiness: `documentation-only-handoff-gate`
- next ticket: `RE-171`

No production source or marker change is authorized by this gate.

## Validation

- `python3 -m pytest tests/reverse/test_re170_module_spec_psxpc_n_closure_or_handoff.py -q`
- `python3 -m pytest tests/reverse -q`
- metadata-only guard over RE-170 outputs
