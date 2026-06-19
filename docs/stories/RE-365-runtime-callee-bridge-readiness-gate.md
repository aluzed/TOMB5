# RE-365 runtime callee bridge readiness gate

## Goal

Gate the RE-364 `runtime-callee-bridge` candidate and decide whether it can reopen proof-domain selection or authorize a source patch.

## Inputs

- Upstream handoff: `docs/reverse/generated/re364-platform-frontend-service-post-gpu-fmv-mainloop-next-subcluster-selection-handoff.csv`
- Candidate rows: `docs/reverse/generated/re364-platform-frontend-service-post-gpu-fmv-mainloop-next-subcluster-selection-candidates.csv`
- Source-context metadata: `docs/reverse/generated/re343-ghidra-platform-frontend-service-narrow-candidates.csv`

## Progress tracker

- [x] RE-364 runtime callee bridge handoff validated.
- [x] Selected candidate set checked for drift.
- [x] Candidate-level proof requirement evaluated.
- [x] Domain/source-patch authorization denied.
- [x] Still-narrower proof export handoff emitted.

## Generated artifacts

- `docs/reverse/generated/re365-runtime-callee-bridge-readiness-gate-candidates.csv`
- `docs/reverse/generated/re365-runtime-callee-bridge-readiness-gate-gates.csv`
- `docs/reverse/generated/re365-runtime-callee-bridge-readiness-gate-summary.csv`
- `docs/reverse/generated/re365-runtime-callee-bridge-readiness-gate-handoff.csv`
- `docs/reverse/functions/re365-runtime-callee-bridge-readiness-gate.md`

## Findings

- Selected narrow subcluster: `runtime-callee-bridge`
- Input candidates: `1`
- Gate rows: `1`
- Ready to reopen domain selection: `0`
- Source patch authorized rows: `0`

## Readiness decision

The `runtime-callee-bridge` row remains source-symbolic. Domain and pivot stay `none` / `none`, and code readiness remains `blocked`.

## Follow-up ticket breakdown

- `RE-366` / `runtime-callee-bridge-candidate-proof-export`: export still-narrower candidate proof context for `a01f47cb95a4`.
  - Inputs: RE-365 candidate/gate CSVs plus RE-343 source-context metadata.
  - Deliverables: metadata-only proof export, summary/handoff, story.
  - Stop condition: if no candidate-level proof exists, keep source/code readiness blocked and propose the next deferred hypothesis.

## Validation commands

- `python -m pytest tests/reverse/test_re365_runtime_callee_bridge_readiness_gate.py -q`
- `python scripts/reverse/re365_runtime_callee_bridge_readiness_gate.py --repo .`
- `python -m pytest tests/reverse -q`
