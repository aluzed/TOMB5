# RE-376 dynamic-lighting service next-candidate callsite map

## Goal

Build a source-backed metadata-only callsite map for dynamic-lighting next candidate `3a208e2bf745` using RE-375 context rows.

## Inputs

- Upstream handoff: `docs/reverse/generated/re375-dynamic-lighting-service-next-candidate-proof-handoff.csv`
- Candidate context rows: `docs/reverse/generated/re375-dynamic-lighting-service-next-candidate-proof-contexts.csv`
- Source files referenced by the context rows.

## Progress tracker

- [x] RE-375 next-candidate proof-export handoff validated.
- [x] Caller context function set verified fail-closed.
- [x] Function spans and source-backed callsite line metadata emitted.
- [x] Raw line text and local reverse identity omitted from generated artifacts.
- [x] Next-candidate callsite readiness gate follow-up selected.

## Generated artifacts

- `docs/reverse/generated/re376-dynamic-lighting-service-next-candidate-callsite-functions.csv`
- `docs/reverse/generated/re376-dynamic-lighting-service-next-candidate-callsite-map.csv`
- `docs/reverse/generated/re376-dynamic-lighting-service-next-candidate-callsite-gate.csv`
- `docs/reverse/generated/re376-dynamic-lighting-service-next-candidate-callsite-summary.csv`
- `docs/reverse/generated/re376-dynamic-lighting-service-next-candidate-callsite-handoff.csv`
- `docs/reverse/functions/re376-dynamic-lighting-service-next-candidate-callsite-map.md`

## Findings

- Source context functions: `21`
- Source-backed callsite rows: `40`
- Implemented context functions: `9`
- Stub context functions: `12`
- No-callsite context functions: `0`
- Candidate-level proof rows: `0`
- Ready to reopen domain selection: `0`
- Source patch authorized rows: `0`

## Readiness decision

The callsite map is source-backed and metadata-ready, but it is not yet a proof-domain decision. Domain and pivot stay `none`; code readiness remains blocked.

## Follow-up ticket breakdown

- `RE-377` / `dynamic-lighting-service-next-candidate-callsite-readiness-gate`: gate the source-backed next-candidate callsite map and decide whether any dynamic-lighting callsite family can become a proof pivot or whether the dynamic-lighting queue closes.
  - Inputs: RE-376 function/callsite/gate rows.
  - Deliverables: readiness gate rows, selected or denied pivot, and handoff for either source-patch denial or dynamic-lighting queue exhaustion/transition.
  - Stop condition: if source-backed callsites still do not prove candidate-level behavior, keep source/code readiness blocked and close or transition from the dynamic-lighting subcluster.

## Validation commands

- `python -m pytest tests/reverse/test_re376_dynamic_lighting_service_next_candidate_callsite_map.py -q`
- `python scripts/reverse/re376_dynamic_lighting_service_next_candidate_callsite_map.py --repo .`
- `python -m pytest tests/reverse -q`
