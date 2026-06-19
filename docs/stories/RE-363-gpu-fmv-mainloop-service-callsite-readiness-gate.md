# RE-363 gpu/fmv mainloop service callsite readiness gate

## Goal

Gate the RE-362 source-backed callsite map, close the gpu/fmv mainloop service queue if no family proves candidate-level behavior, and hand off to the next deferred parent subcluster.

## Inputs

- Upstream handoff: `docs/reverse/generated/re362-gpu-fmv-mainloop-service-candidate-callsite-handoff.csv`
- Source-backed callsite map: `docs/reverse/generated/re362-gpu-fmv-mainloop-service-candidate-callsite-map.csv`
- Source context functions: `docs/reverse/generated/re362-gpu-fmv-mainloop-service-candidate-callsite-functions.csv`
- gpu/fmv mainloop candidate queue: `docs/reverse/generated/re360-gpu-fmv-mainloop-service-readiness-gate-candidates.csv`
- Parent platform/frontend subcluster queue: `docs/reverse/generated/re343-ghidra-platform-frontend-service-narrow-subclusters.csv`

## Progress tracker

- [x] RE-362 callsite handoff validated.
- [x] RE-360 gpu/fmv mainloop candidate queue verified exhausted after the single candidate.
- [x] Parent RE-343 deferred subcluster queue checked.
- [x] Callsite families grouped and readiness-gated.
- [x] Candidate-level proof and source-patch authorization denied for every family.
- [x] Next parent subcluster selection follow-up emitted.

## Generated artifacts

- `docs/reverse/generated/re363-gpu-fmv-mainloop-service-callsite-readiness-families.csv`
- `docs/reverse/generated/re363-gpu-fmv-mainloop-service-callsite-readiness-decision.csv`
- `docs/reverse/generated/re363-gpu-fmv-mainloop-service-callsite-readiness-summary.csv`
- `docs/reverse/generated/re363-gpu-fmv-mainloop-service-callsite-readiness-handoff.csv`
- `docs/reverse/functions/re363-gpu-fmv-mainloop-service-callsite-readiness-gate.md`

## Findings

- Source context functions: `14`
- Source-backed callsite rows: `87`
- Callsite families: `8`
- Implemented callsite families: `8`
- Stub-only callsite families: `0`
- Candidate-level proof rows: `0`
- Ready to reopen domain selection: `0`
- Source patch authorized rows: `0`
- Next deferred candidate: `none`
- Next deferred subcluster: `runtime-callee-bridge`

## Readiness decision

The gpu/fmv mainloop candidate's source-backed callsite map still does not prove candidate-level behavior. Domain and pivot remain `none`; code readiness remains `blocked`. The gpu/fmv mainloop candidate queue is exhausted.

## Follow-up ticket breakdown

- `RE-364` / `platform-frontend-service-post-gpu-fmv-mainloop-next-subcluster-selection`: close `gpu-fmv-mainloop-service` and select `runtime-callee-bridge` from the parent RE-343 deferred subcluster queue.
  - Inputs: RE-363 handoff plus RE-343 subcluster queue.
  - Deliverables: metadata-only selected subcluster/candidate rows, summary, and handoff to that subcluster readiness gate.
  - Stop condition: keep source/code readiness blocked until the next selected subcluster has candidate-level proof.

## Validation commands

- `python -m pytest tests/reverse/test_re363_gpu_fmv_mainloop_service_callsite_readiness_gate.py -q`
- `python scripts/reverse/re363_gpu_fmv_mainloop_service_callsite_readiness_gate.py --repo .`
- `python -m pytest tests/reverse -q`
