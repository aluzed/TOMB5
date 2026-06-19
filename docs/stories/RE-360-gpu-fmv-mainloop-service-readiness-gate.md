# RE-360 gpu/fmv mainloop service readiness gate

## Goal

Gate the RE-359 `gpu-fmv-mainloop-service` candidate and decide whether it can reopen proof-domain selection or authorize a source patch.

## Inputs

- Upstream handoff: `docs/reverse/generated/re359-platform-frontend-service-post-frontend-display-menu-next-subcluster-selection-handoff.csv`
- Candidate rows: `docs/reverse/generated/re359-platform-frontend-service-post-frontend-display-menu-next-subcluster-selection-candidates.csv`
- Source-context metadata: `docs/reverse/generated/re343-ghidra-platform-frontend-service-narrow-candidates.csv`

## Progress tracker

- [x] RE-359 gpu/fmv mainloop service handoff validated.
- [x] Selected candidate set checked for drift.
- [x] Candidate-level proof requirement evaluated.
- [x] Domain/source-patch authorization denied.
- [x] Still-narrower proof export handoff emitted.

## Generated artifacts

- `docs/reverse/generated/re360-gpu-fmv-mainloop-service-readiness-gate-candidates.csv`
- `docs/reverse/generated/re360-gpu-fmv-mainloop-service-readiness-gate-gates.csv`
- `docs/reverse/generated/re360-gpu-fmv-mainloop-service-readiness-gate-summary.csv`
- `docs/reverse/generated/re360-gpu-fmv-mainloop-service-readiness-gate-handoff.csv`
- `docs/reverse/functions/re360-gpu-fmv-mainloop-service-readiness-gate.md`

## Findings

- Selected narrow subcluster: `gpu-fmv-mainloop-service`
- Input candidates: `1`
- Gate rows: `1`
- Ready to reopen domain selection: `0`
- Source patch authorized rows: `0`

## Readiness decision

The `gpu-fmv-mainloop-service` row remains source-symbolic. Domain and pivot stay `none` / `none`, and code readiness remains `blocked`.

## Follow-up ticket breakdown

- `RE-361` / `gpu-fmv-mainloop-service-candidate-proof-export`: export still-narrower candidate proof context for `1b3534d34062`.
  - Inputs: RE-360 candidate/gate CSVs plus RE-343 source-context metadata.
  - Deliverables: metadata-only proof export, summary/handoff, story.
  - Stop condition: if no candidate-level proof exists, keep source/code readiness blocked and propose the next deferred hypothesis.

## Validation commands

- `python -m pytest tests/reverse/test_re360_gpu_fmv_mainloop_service_readiness_gate.py -q`
- `python scripts/reverse/re360_gpu_fmv_mainloop_service_readiness_gate.py --repo .`
- `python -m pytest tests/reverse -q`
