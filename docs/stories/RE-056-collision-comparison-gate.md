# RE-056 — Collision source-vs-binary comparison gate

Status: Done

## Goal

Advance `collision` / `GetCollisionInfo` through `collision-comparison-gate` as a metadata-only reverse-engineering step.

## Scope

- depends on: `RE-054`, `RE-055`
- safety contract: `metadata-only; no opcodes; no machine words; no payload coordinates; no branch or call targets; no copied dump records; no raw addresses in generated outputs`

## Progress

- [x] Input artifacts loaded.
- [x] Metadata only artifact published.
- [x] Readiness decision recorded.
- [x] Forbidden raw evidence excluded.

## Generated artifacts

- `docs/reverse/generated/re053-re060-collision-chain.csv`
- `docs/reverse/functions/re053-re060-collision-chain.md`

## Findings

- no non-raw equivalence proof names collision side effects
- source-level taxonomy is insufficient for marker/source changes

## Readiness decision

- decision: `blocked-by-missing-non-raw-binary-equivalence-proof`
- safe next action: `do not patch; reduce proof to selected collision cluster`
- code change readiness: `blocked`
- next ticket: `RE-057`

Do not patch production source or add `(F)`, `(D)`, or `(**)` markers from this story alone.

## Validation

- `python3 -m pytest tests/reverse/test_re053_re060_collision_chain.py -q`
- metadata-only guard over RE-053..RE-060 outputs

## Next step

RE-057: do not patch; reduce proof to selected collision cluster.
