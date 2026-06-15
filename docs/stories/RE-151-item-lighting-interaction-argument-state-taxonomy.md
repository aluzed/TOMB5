# RE-151 — Item lighting interaction argument and state taxonomy

Status: Done

## Goal

Classify item-lighting argument shapes, state fields, and side-effect surfaces from the source-backed RE-150 callsite map.

## Progress tracker

- [x] RE-150 callsite map consumed.
- [x] Argument and state taxonomy emitted.
- [x] State and side-effect labels consolidated.
- [x] Forbidden evidence excluded from generated artifacts.

## Generated artifacts

- `docs/reverse/generated/re151-item-lighting-interaction-argument-state-taxonomy.csv`
- `docs/reverse/functions/re151-item-lighting-interaction-argument-state-taxonomy.md`

## Readiness decision

- decision: `argument-state-taxonomy-blocked`
- code change readiness: `blocked`
- marker readiness: `blocked`
- next ticket: `RE-152`
- blocker: `missing-item-lighting-state-contract-and-symbolic-equivalence-proof`

## Validation

- `python3 -m pytest tests/reverse/test_re151_item_lighting_argument_state_taxonomy.py -q`
- `python3 -m pytest tests/reverse -q`
- metadata-only guard over RE-151 artifacts
