# RE-320 collision geometry helper final candidate callsite map

## Goal

Build a source-backed metadata-only callsite map for final candidate `61d55bb1809b` using RE-319 context rows.

## Inputs

- Upstream handoff: `docs/reverse/generated/re319-collision-geometry-helper-final-candidate-proof-handoff.csv`
- Candidate context rows: `docs/reverse/generated/re319-collision-geometry-helper-final-candidate-proof-contexts.csv`
- Source files referenced by the context rows.

## Progress tracker

- [x] RE-319 final-candidate callsite-map handoff validated.
- [x] Caller context function set verified fail-closed.
- [x] Function spans and source-backed callsite line metadata emitted.
- [x] Raw line text and local reverse identity omitted from generated artifacts.
- [x] Final-candidate callsite readiness gate follow-up selected.

## Generated artifacts

- `docs/reverse/generated/re320-collision-geometry-helper-final-candidate-callsite-functions.csv`
- `docs/reverse/generated/re320-collision-geometry-helper-final-candidate-callsite-map.csv`
- `docs/reverse/generated/re320-collision-geometry-helper-final-candidate-callsite-gate.csv`
- `docs/reverse/generated/re320-collision-geometry-helper-final-candidate-callsite-summary.csv`
- `docs/reverse/generated/re320-collision-geometry-helper-final-candidate-callsite-handoff.csv`
- `docs/reverse/functions/re320-collision-geometry-helper-final-candidate-callsite-map.md`

## Findings

- Source context functions: `20`
- Source-backed callsite rows: `28`
- Implemented context functions: `4`
- Stub context functions: `15`
- No-callsite context functions: `1`
- Candidate-level proof rows: `0`
- Ready to reopen domain selection: `0`
- Source patch authorized rows: `0`

## Readiness decision

The final-candidate callsite map is source-backed and metadata-ready, but it is not yet a proof-domain decision. Domain and pivot stay `none`; code readiness remains blocked.

## Follow-up ticket breakdown

- `RE-321` / `collision-geometry-helper-final-candidate-callsite-readiness-gate`: gate the final-candidate source-backed callsite map and decide whether any callsite family can become a proof pivot or whether the candidate queue remains blocked.
  - Inputs: RE-320 function/callsite/gate rows.
  - Deliverables: readiness gate rows, selected or denied pivot, handoff for either source-patch denial or final candidate-queue exhaustion.
  - Stop condition: if implemented source callsites still do not prove candidate-level behavior, keep source/code readiness blocked and emit a queue-exhaustion handoff.

## Validation commands

- `python -m pytest tests/reverse/test_re320_collision_geometry_helper_final_candidate_callsite_map.py -q`
- `python scripts/reverse/re320_collision_geometry_helper_final_candidate_callsite_map.py --repo .`
- `python -m pytest tests/reverse -q`
