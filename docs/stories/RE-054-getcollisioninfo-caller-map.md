# RE-054 — GetCollisionInfo caller map

Status: Done

## Goal

Advance `collision` / `GetCollisionInfo` through `getcollisioninfo-caller-map` as a metadata-only reverse-engineering step.

## Scope

- depends on: `RE-053`
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

- callers classified: `19`
- selected cluster: `lara-movement-collision`

## Readiness decision

- decision: `caller-clusters-published`
- safe next action: `advance to collision argument/data taxonomy`
- code change readiness: `blocked`
- next ticket: `RE-055`

Do not patch production source or add `(F)`, `(D)`, or `(**)` markers from this story alone.

## Validation

- `python3 -m pytest tests/reverse/test_re053_re060_collision_chain.py -q`
- metadata-only guard over RE-053..RE-060 outputs

## Next step

RE-055: advance to collision argument/data taxonomy.
