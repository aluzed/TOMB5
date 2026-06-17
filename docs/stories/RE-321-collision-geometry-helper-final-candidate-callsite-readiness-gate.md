# RE-321 collision geometry helper final candidate callsite readiness gate

## Goal

Gate the RE-320 final-candidate source-backed callsite map and decide whether any callsite family can reopen a proof domain or authorize a source patch.

## Inputs

- Upstream handoff: `docs/reverse/generated/re320-collision-geometry-helper-final-candidate-callsite-handoff.csv`
- Source-backed callsite map: `docs/reverse/generated/re320-collision-geometry-helper-final-candidate-callsite-map.csv`
- Source context functions: `docs/reverse/generated/re320-collision-geometry-helper-final-candidate-callsite-functions.csv`
- Deferred candidate order: `docs/reverse/generated/re312-collision-geometry-helper-readiness-gate-candidates.csv`

## Progress tracker

- [x] RE-320 final-candidate callsite handoff validated.
- [x] RE-312 candidate queue exhaustion verified fail-closed.
- [x] Final-candidate callsite families grouped and readiness-gated.
- [x] Candidate-level proof and source-patch authorization denied for every family.
- [x] Candidate queue exhaustion handoff emitted.

## Generated artifacts

- `docs/reverse/generated/re321-collision-geometry-helper-final-candidate-callsite-readiness-families.csv`
- `docs/reverse/generated/re321-collision-geometry-helper-final-candidate-callsite-readiness-decision.csv`
- `docs/reverse/generated/re321-collision-geometry-helper-final-candidate-callsite-readiness-summary.csv`
- `docs/reverse/generated/re321-collision-geometry-helper-final-candidate-callsite-readiness-handoff.csv`
- `docs/reverse/functions/re321-collision-geometry-helper-final-candidate-callsite-readiness-gate.md`

## Findings

- Source context functions: `20`
- Source-backed callsite rows: `28`
- Callsite families: `4`
- Implemented callsite families: `3`
- Stub-only callsite families: `1`
- Candidate-level proof rows: `0`
- Ready to reopen domain selection: `0`
- Source patch authorized rows: `0`

## Readiness decision

No RE-320 final-candidate callsite family proves candidate-level behavior. Domain and pivot stay `none`; source/code readiness remains `blocked`, and the candidate queue is exhausted.

## Follow-up ticket breakdown

- `TBD` / `collision-geometry-helper-candidate-queue-exhausted`: no remaining deferred collision-geometry helper candidate exists after `61d55bb1809b`.
  - Inputs: RE-312 candidate order and RE-321 denial handoff.
  - Deliverables: await changed upstream mapping or new non-raw candidate-level proof evidence before reopening domain selection.
  - Stop condition: candidate queue is exhausted and source/code readiness remains blocked.

## Validation commands

- `python -m pytest tests/reverse/test_re321_collision_geometry_helper_final_candidate_callsite_readiness_gate.py -q`
- `python scripts/reverse/re321_collision_geometry_helper_final_candidate_callsite_readiness_gate.py --repo .`
- `python -m pytest tests/reverse -q`
