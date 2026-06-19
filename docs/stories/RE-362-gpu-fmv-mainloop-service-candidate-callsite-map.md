# RE-362 gpu/fmv mainloop service candidate callsite map

## Goal

Build a source-backed metadata-only callsite map for gpu/fmv mainloop candidate `1b3534d34062` using RE-361 context rows.

## Inputs

- Upstream handoff: `docs/reverse/generated/re361-gpu-fmv-mainloop-service-candidate-proof-handoff.csv`
- Candidate context rows: `docs/reverse/generated/re361-gpu-fmv-mainloop-service-candidate-proof-contexts.csv`
- Source files referenced by the context rows.

## Progress tracker

- [x] RE-361 proof-export handoff validated.
- [x] Caller context function set verified fail-closed.
- [x] Function spans and source-backed callsite line metadata emitted.
- [x] Raw line text and local reverse identity omitted from generated artifacts.
- [x] Callsite readiness gate follow-up selected.

## Generated artifacts

- `docs/reverse/generated/re362-gpu-fmv-mainloop-service-candidate-callsite-functions.csv`
- `docs/reverse/generated/re362-gpu-fmv-mainloop-service-candidate-callsite-map.csv`
- `docs/reverse/generated/re362-gpu-fmv-mainloop-service-candidate-callsite-gate.csv`
- `docs/reverse/generated/re362-gpu-fmv-mainloop-service-candidate-callsite-summary.csv`
- `docs/reverse/generated/re362-gpu-fmv-mainloop-service-candidate-callsite-handoff.csv`
- `docs/reverse/functions/re362-gpu-fmv-mainloop-service-candidate-callsite-map.md`

## Findings

- Source context functions: `14`
- Source-backed callsite rows: `87`
- Implemented context functions: `12`
- Stub context functions: `0`
- No-callsite context functions: `2`
- Candidate-level proof rows: `0`
- Ready to reopen domain selection: `0`
- Source patch authorized rows: `0`

## Readiness decision

The callsite map is source-backed and metadata-ready, but it is not yet a proof-domain decision. Domain and pivot stay `none`; code readiness remains blocked.

## Follow-up ticket breakdown

- `RE-363` / `gpu-fmv-mainloop-service-callsite-readiness-gate`: gate the source-backed callsite map and decide whether any gpu/fmv mainloop callsite family can become a proof pivot.
  - Inputs: RE-362 function/callsite/gate rows.
  - Deliverables: readiness gate rows, selected or denied pivot, and handoff for source-patch denial or parent-queue return.
  - Stop condition: if source-backed callsites still do not prove candidate-level behavior, keep source/code readiness blocked and return to the parent platform/frontend queue.

## Validation commands

- `python -m pytest tests/reverse/test_re362_gpu_fmv_mainloop_service_candidate_callsite_map.py -q`
- `python scripts/reverse/re362_gpu_fmv_mainloop_service_candidate_callsite_map.py --repo .`
- `python -m pytest tests/reverse -q`
