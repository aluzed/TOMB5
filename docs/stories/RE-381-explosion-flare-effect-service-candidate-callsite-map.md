# RE-381 explosion/flare effect service candidate callsite map

## Goal

Build a source-backed metadata-only callsite map for explosion/flare candidate `87d9c8a62335` using RE-380 context rows.

## Inputs

- Upstream handoff: `docs/reverse/generated/re380-explosion-flare-effect-service-candidate-proof-handoff.csv`
- Candidate context rows: `docs/reverse/generated/re380-explosion-flare-effect-service-candidate-proof-contexts.csv`
- Source files referenced by the context rows.

## Progress tracker

- [x] RE-380 proof-export handoff validated.
- [x] Caller context function set verified fail-closed.
- [x] Function spans and source-backed callsite line metadata emitted.
- [x] Raw line text and local reverse identity omitted from generated artifacts.
- [x] Callsite readiness gate follow-up selected.

## Generated artifacts

- `docs/reverse/generated/re381-explosion-flare-effect-service-candidate-callsite-functions.csv`
- `docs/reverse/generated/re381-explosion-flare-effect-service-candidate-callsite-map.csv`
- `docs/reverse/generated/re381-explosion-flare-effect-service-candidate-callsite-gate.csv`
- `docs/reverse/generated/re381-explosion-flare-effect-service-candidate-callsite-summary.csv`
- `docs/reverse/generated/re381-explosion-flare-effect-service-candidate-callsite-handoff.csv`
- `docs/reverse/functions/re381-explosion-flare-effect-service-candidate-callsite-map.md`

## Findings

- Source context functions: `18`
- Source-backed callsite rows: `121`
- Implemented context functions: `12`
- Stub context functions: `6`
- No-callsite context functions: `0`
- Candidate-level proof rows: `0`
- Ready to reopen domain selection: `0`
- Source patch authorized rows: `0`

## Readiness decision

The callsite map is source-backed and metadata-ready, but it is not yet a proof-domain decision. Domain and pivot stay `none`; code readiness remains blocked.

## Follow-up ticket breakdown

- `RE-382` / `explosion-flare-effect-service-callsite-readiness-gate`: gate the source-backed callsite map and decide whether any explosion/flare callsite family can become a proof pivot.
  - Inputs: RE-381 function/callsite/gate rows.
  - Deliverables: readiness gate rows, selected or denied pivot, and handoff for either source-patch denial or deferred explosion/flare candidate selection.
  - Stop condition: if source-backed callsites still do not prove candidate-level behavior, keep source/code readiness blocked and defer to the other explosion/flare candidate.

## Validation commands

- `python -m pytest tests/reverse/test_re381_explosion_flare_effect_service_candidate_callsite_map.py -q`
- `python scripts/reverse/re381_explosion_flare_effect_service_candidate_callsite_map.py --repo .`
- `python -m pytest tests/reverse -q`
