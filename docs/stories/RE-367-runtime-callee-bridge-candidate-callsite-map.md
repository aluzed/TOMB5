# RE-367 runtime callee bridge candidate callsite map

## Goal

Build a source-backed metadata-only callsite map for runtime/callee bridge candidate `a01f47cb95a4` using RE-366 context rows.

## Inputs

- Upstream handoff: `docs/reverse/generated/re366-runtime-callee-bridge-candidate-proof-handoff.csv`
- Candidate context rows: `docs/reverse/generated/re366-runtime-callee-bridge-candidate-proof-contexts.csv`
- Source files referenced by the context rows.

## Progress tracker

- [x] RE-366 proof-export handoff validated.
- [x] Callee context function set verified fail-closed.
- [x] Function spans and source-backed callsite line metadata emitted.
- [x] Raw line text and local reverse identity omitted from generated artifacts.
- [x] Callsite readiness gate follow-up selected.

## Generated artifacts

- `docs/reverse/generated/re367-runtime-callee-bridge-candidate-callsite-functions.csv`
- `docs/reverse/generated/re367-runtime-callee-bridge-candidate-callsite-map.csv`
- `docs/reverse/generated/re367-runtime-callee-bridge-candidate-callsite-gate.csv`
- `docs/reverse/generated/re367-runtime-callee-bridge-candidate-callsite-summary.csv`
- `docs/reverse/generated/re367-runtime-callee-bridge-candidate-callsite-handoff.csv`
- `docs/reverse/functions/re367-runtime-callee-bridge-candidate-callsite-map.md`

## Findings

- Source context functions: `11`
- Source-backed callsite rows: `1`
- Implemented context functions: `1`
- Stub context functions: `1`
- No-callsite context functions: `9`
- Candidate-level proof rows: `0`
- Ready to reopen domain selection: `0`
- Source patch authorized rows: `0`

## Readiness decision

The callsite map is source-backed and metadata-ready, but it is not yet a proof-domain decision. Domain and pivot stay `none`; code readiness remains blocked.

## Follow-up ticket breakdown

- `RE-368` / `runtime-callee-bridge-callsite-readiness-gate`: gate the source-backed callsite map and decide whether any runtime/callee bridge callsite family can become a proof pivot.
  - Inputs: RE-367 function/callsite/gate rows.
  - Deliverables: readiness gate rows, selected or denied pivot, and handoff for source-patch denial or parent-queue return.
  - Stop condition: if source-backed callsites still do not prove candidate-level behavior, keep source/code readiness blocked and return to the parent platform/frontend queue.

## Validation commands

- `python -m pytest tests/reverse/test_re367_runtime_callee_bridge_candidate_callsite_map.py -q`
- `python scripts/reverse/re367_runtime_callee_bridge_candidate_callsite_map.py --repo .`
- `python -m pytest tests/reverse -q`
