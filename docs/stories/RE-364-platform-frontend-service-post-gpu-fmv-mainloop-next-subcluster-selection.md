# RE-364 platform/frontend service post gpu/fmv mainloop next subcluster selection

## Goal

Consume the RE-363 gpu/fmv mainloop queue exhaustion and select the next deferred platform/frontend service subcluster from the parent queue.

## Inputs

- Exhausted selected-subcluster handoff: `docs/reverse/generated/re363-gpu-fmv-mainloop-service-callsite-readiness-handoff.csv`
- Parent selection handoff: `docs/reverse/generated/re343-ghidra-platform-frontend-service-narrow-handoff.csv`
- Parent subcluster queue: `docs/reverse/generated/re343-ghidra-platform-frontend-service-narrow-subclusters.csv`
- Candidate metadata: `docs/reverse/generated/re343-ghidra-platform-frontend-service-narrow-candidates.csv`

## Progress tracker

- [x] RE-363 gpu/fmv mainloop queue exhaustion validated.
- [x] Parent platform/frontend service subcluster queue verified fail-closed.
- [x] Closed subclusters excluded: `cd-load-audio-service;frontend-display-menu-service;gpu-fmv-mainloop-service`.
- [x] Next deferred subcluster selected: `runtime-callee-bridge`.
- [x] Readiness gate handoff emitted for `RE-365`.

## Generated artifacts

- `docs/reverse/generated/re364-platform-frontend-service-post-gpu-fmv-mainloop-next-subcluster-selection-subclusters.csv`
- `docs/reverse/generated/re364-platform-frontend-service-post-gpu-fmv-mainloop-next-subcluster-selection-candidates.csv`
- `docs/reverse/generated/re364-platform-frontend-service-post-gpu-fmv-mainloop-next-subcluster-selection-summary.csv`
- `docs/reverse/generated/re364-platform-frontend-service-post-gpu-fmv-mainloop-next-subcluster-selection-handoff.csv`
- `docs/reverse/functions/re364-platform-frontend-service-post-gpu-fmv-mainloop-next-subcluster-selection.md`

## Findings

- Parent scope: `platform-frontend-service-cluster`
- Closed subclusters: `cd-load-audio-service;frontend-display-menu-service;gpu-fmv-mainloop-service`
- Input subclusters: `4`
- Remaining deferred subclusters: `1`
- Selected subcluster: `runtime-callee-bridge`
- Selected candidates: `a01f47cb95a4`
- Ready to reopen domain selection: `0`
- Source patch authorized rows: `0`

## Readiness decision

The selected runtime callee bridge subcluster is only ready for a readiness gate. Domain and pivot stay `none`; source/code readiness remains `blocked`.

## Follow-up ticket breakdown

- `RE-365` / `runtime-callee-bridge-readiness-gate`: gate candidates `a01f47cb95a4` before any proof-domain selection.
  - Inputs: RE-364 selected subcluster/candidate rows plus parent queue metadata.
  - Deliverables: candidate readiness rows, selected/denied follow-up proof export, and handoff.
  - Stop condition: if candidate-level source-symbolic proof is still missing, keep source/code readiness blocked.

## Validation commands

- `python -m pytest tests/reverse/test_re364_platform_frontend_service_post_gpu_fmv_mainloop_next_subcluster_selection.py -q`
- `python scripts/reverse/re364_platform_frontend_service_post_gpu_fmv_mainloop_next_subcluster_selection.py --repo .`
- `python -m pytest tests/reverse -q`
