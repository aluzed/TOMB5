# RE-318 collision geometry helper next candidate callsite readiness gate

## Goal

Gate the RE-317 next-candidate source-backed callsite map and decide whether any callsite family can reopen a proof domain or authorize a source patch.

## Inputs

- Upstream handoff: `docs/reverse/generated/re317-collision-geometry-helper-next-candidate-callsite-handoff.csv`
- Source-backed callsite map: `docs/reverse/generated/re317-collision-geometry-helper-next-candidate-callsite-map.csv`
- Source context functions: `docs/reverse/generated/re317-collision-geometry-helper-next-candidate-callsite-functions.csv`
- Deferred candidate order: `docs/reverse/generated/re312-collision-geometry-helper-readiness-gate-candidates.csv`

## Progress tracker

- [x] RE-317 next-candidate callsite handoff validated.
- [x] RE-312 final deferred candidate order verified fail-closed.
- [x] Next-candidate callsite families grouped and readiness-gated.
- [x] Candidate-level proof and source-patch authorization denied for every family.
- [x] Final deferred candidate proof export selected.

## Generated artifacts

- `docs/reverse/generated/re318-collision-geometry-helper-next-candidate-callsite-readiness-families.csv`
- `docs/reverse/generated/re318-collision-geometry-helper-next-candidate-callsite-readiness-decision.csv`
- `docs/reverse/generated/re318-collision-geometry-helper-next-candidate-callsite-readiness-summary.csv`
- `docs/reverse/generated/re318-collision-geometry-helper-next-candidate-callsite-readiness-handoff.csv`
- `docs/reverse/functions/re318-collision-geometry-helper-next-candidate-callsite-readiness-gate.md`

## Findings

- Source context functions: `23`
- Source-backed callsite rows: `40`
- Callsite families: `4`
- Implemented callsite families: `3`
- Stub-only callsite families: `1`
- Candidate-level proof rows: `0`
- Ready to reopen domain selection: `0`
- Source patch authorized rows: `0`

## Readiness decision

No RE-317 next-candidate callsite family proves candidate-level behavior. Domain and pivot stay `none`; source/code readiness remains `blocked`.

## Follow-up ticket breakdown

- `RE-319` / `collision-geometry-helper-final-candidate-proof-export`: export source-symbolic context for final deferred candidate `61d55bb1809b`.
  - Inputs: RE-312 candidate order and RE-318 denial handoff.
  - Deliverables: candidate-scoped source-symbolic context rows, candidate proof summary, and handoff to a callsite map or terminal candidate-exhaustion gate.
  - Stop condition: if direct source identity and candidate-level proof remain absent for the final candidate, keep domain/pivot/source readiness blocked.

## Validation commands

- `python -m pytest tests/reverse/test_re318_collision_geometry_helper_next_candidate_callsite_readiness_gate.py -q`
- `python scripts/reverse/re318_collision_geometry_helper_next_candidate_callsite_readiness_gate.py --repo .`
- `python -m pytest tests/reverse -q`
