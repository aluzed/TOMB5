# RE-315 collision geometry helper callsite readiness gate

## Goal

Gate the RE-314 source-backed callsite map and decide whether any callsite family can reopen a proof domain or authorize a source patch.

## Inputs

- Upstream handoff: `docs/reverse/generated/re314-collision-geometry-helper-candidate-callsite-handoff.csv`
- Source-backed callsite map: `docs/reverse/generated/re314-collision-geometry-helper-candidate-callsite-map.csv`
- Source context functions: `docs/reverse/generated/re314-collision-geometry-helper-candidate-callsite-functions.csv`
- Deferred candidate order: `docs/reverse/generated/re312-collision-geometry-helper-readiness-gate-candidates.csv`

## Progress tracker

- [x] RE-314 callsite handoff validated.
- [x] RE-312 deferred candidate order verified fail-closed.
- [x] Callsite families grouped and readiness-gated.
- [x] Candidate-level proof and source-patch authorization denied for every family.
- [x] Next deferred candidate proof export selected.

## Generated artifacts

- `docs/reverse/generated/re315-collision-geometry-helper-callsite-readiness-families.csv`
- `docs/reverse/generated/re315-collision-geometry-helper-callsite-readiness-decision.csv`
- `docs/reverse/generated/re315-collision-geometry-helper-callsite-readiness-summary.csv`
- `docs/reverse/generated/re315-collision-geometry-helper-callsite-readiness-handoff.csv`
- `docs/reverse/functions/re315-collision-geometry-helper-callsite-readiness-gate.md`

## Findings

- Source context functions: `20`
- Source-backed callsite rows: `37`
- Callsite families: `4`
- Implemented callsite families: `3`
- Stub-only callsite families: `1`
- Candidate-level proof rows: `0`
- Ready to reopen domain selection: `0`
- Source patch authorized rows: `0`

## Readiness decision

No RE-314 callsite family proves candidate-level behavior. Domain and pivot stay `none`; source/code readiness remains `blocked`.

## Follow-up ticket breakdown

- `RE-316` / `collision-geometry-helper-next-candidate-proof-export`: export source-symbolic context for deferred candidate `d96359c1d9f3`.
  - Inputs: RE-312 candidate order and RE-315 denial handoff.
  - Deliverables: candidate-scoped source-symbolic context rows, candidate proof summary, handoff to a callsite map or deferral gate.
  - Stop condition: if direct source identity and candidate-level proof remain absent, keep domain/pivot/source readiness blocked.

## Validation commands

- `python -m pytest tests/reverse/test_re315_collision_geometry_helper_callsite_readiness_gate.py -q`
- `python scripts/reverse/re315_collision_geometry_helper_callsite_readiness_gate.py --repo .`
- `python -m pytest tests/reverse -q`
