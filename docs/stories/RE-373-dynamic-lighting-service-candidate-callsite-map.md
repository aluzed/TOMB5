# RE-373 dynamic-lighting service candidate callsite map

## Goal

Build a source-backed metadata-only callsite map for dynamic-lighting candidate `f5d0099b5511` using RE-372 context rows.

## Inputs

- Upstream handoff: `docs/reverse/generated/re372-dynamic-lighting-service-candidate-proof-handoff.csv`
- Candidate context rows: `docs/reverse/generated/re372-dynamic-lighting-service-candidate-proof-contexts.csv`
- Source files referenced by the context rows.

## Progress tracker

- [x] RE-372 proof-export handoff validated.
- [x] Caller context function set verified fail-closed.
- [x] Function spans and source-backed callsite line metadata emitted.
- [x] Raw line text and local reverse identity omitted from generated artifacts.
- [x] Callsite readiness gate follow-up selected.

## Generated artifacts

- `docs/reverse/generated/re373-dynamic-lighting-service-candidate-callsite-functions.csv`
- `docs/reverse/generated/re373-dynamic-lighting-service-candidate-callsite-map.csv`
- `docs/reverse/generated/re373-dynamic-lighting-service-candidate-callsite-gate.csv`
- `docs/reverse/generated/re373-dynamic-lighting-service-candidate-callsite-summary.csv`
- `docs/reverse/generated/re373-dynamic-lighting-service-candidate-callsite-handoff.csv`
- `docs/reverse/functions/re373-dynamic-lighting-service-candidate-callsite-map.md`

## Findings

- Source context functions: `23`
- Source-backed callsite rows: `129`
- Implemented context functions: `16`
- Stub context functions: `7`
- No-callsite context functions: `0`
- Candidate-level proof rows: `0`
- Ready to reopen domain selection: `0`
- Source patch authorized rows: `0`

## Readiness decision

The callsite map is source-backed and metadata-ready, but it is not yet a proof-domain decision. Domain and pivot stay `none`; code readiness remains blocked.

## Follow-up ticket breakdown

- `RE-374` / `dynamic-lighting-service-callsite-readiness-gate`: gate the source-backed callsite map and decide whether any dynamic-lighting callsite family can become a proof pivot.
  - Inputs: RE-373 function/callsite/gate rows.
  - Deliverables: readiness gate rows, selected or denied pivot, and handoff for either source-patch denial or deferred dynamic-lighting candidate selection.
  - Stop condition: if source-backed callsites still do not prove candidate-level behavior, keep source/code readiness blocked and defer to the other dynamic-lighting candidate.

## Validation commands

- `python -m pytest tests/reverse/test_re373_dynamic_lighting_service_candidate_callsite_map.py -q`
- `python scripts/reverse/re373_dynamic_lighting_service_candidate_callsite_map.py --repo .`
- `python -m pytest tests/reverse -q`
