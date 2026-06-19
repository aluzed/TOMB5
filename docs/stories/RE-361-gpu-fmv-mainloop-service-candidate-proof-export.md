# RE-361 gpu/fmv mainloop service candidate proof export

## Goal

Produce a candidate-scoped metadata-only proof export for gpu/fmv mainloop service candidate `1b3534d34062` without committing raw local identity.

## Inputs

- Upstream handoff: `docs/reverse/generated/re360-gpu-fmv-mainloop-service-readiness-gate-handoff.csv`
- RE-360 candidates: `docs/reverse/generated/re360-gpu-fmv-mainloop-service-readiness-gate-candidates.csv`
- Local function export: `docs/reverse/generated/ghidra-functions.csv`
- Local repo function map: `docs/reverse/generated/repo-function-map.csv`

## Progress tracker

- [x] RE-360 candidate proof-export handoff validated.
- [x] Selected candidate context reconstructed inside the generator only.
- [x] Candidate-scoped source-symbolic rows emitted without raw identity columns.
- [x] Domain/pivot/source-patch readiness kept blocked.
- [x] Source-backed callsite-map follow-up selected.

## Generated artifacts

- `docs/reverse/generated/re361-gpu-fmv-mainloop-service-candidate-proof-contexts.csv`
- `docs/reverse/generated/re361-gpu-fmv-mainloop-service-candidate-proof-gate.csv`
- `docs/reverse/generated/re361-gpu-fmv-mainloop-service-candidate-proof-summary.csv`
- `docs/reverse/generated/re361-gpu-fmv-mainloop-service-candidate-proof-handoff.csv`
- `docs/reverse/functions/re361-gpu-fmv-mainloop-service-candidate-proof-export.md`

## Findings

- Selected candidate id: `1b3534d34062`
- Source-symbolic context rows: `14`
- Caller context rows: `14`
- Callee context rows: `0`
- Direct repo symbol rows: `0`
- Candidate-level proof rows: `0`
- Ready to reopen domain selection: `0`
- Source patch authorized rows: `0`

## Readiness decision

The candidate has useful source-symbolic caller context across GPU/display, movie playback, loading, and platform-entry modules, but no direct source-backed candidate proof. Domain and pivot remain `none`, and code readiness remains blocked.

## Follow-up ticket breakdown

- `RE-362` / `gpu-fmv-mainloop-service-candidate-callsite-map`: build a source-backed callsite map for candidate `1b3534d34062`.
  - Inputs: RE-361 context/proof rows plus local source files and repo map metadata.
  - Deliverables: source-backed callsite rows with real file/line references, proof/blocker rows, and a handoff that either selects a proof pivot or stays blocked.
  - Stop condition: if source-backed callsites cannot prove candidate-level behavior without raw evidence, keep source/code readiness blocked and return to the parent platform/frontend queue.

## Validation commands

- `python -m pytest tests/reverse/test_re361_gpu_fmv_mainloop_service_candidate_proof_export.py -q`
- `python scripts/reverse/re361_gpu_fmv_mainloop_service_candidate_proof_export.py --repo .`
- `python -m pytest tests/reverse -q`
