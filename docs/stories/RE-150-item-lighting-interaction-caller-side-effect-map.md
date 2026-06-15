# RE-150 — Item lighting interaction caller and side-effect map

Status: Done

## Goal

Map callers and side-effect surfaces for `DoFlameTorch` and `TriggerAlertLight` without authorizing source or marker changes.

## Progress tracker

- [x] RE-149 ticket plan consumed.
- [x] Item-lighting callsites mapped.
- [x] Torch and alert-light side-effect surfaces classified.
- [x] Forbidden evidence excluded from generated artifacts.

## Generated artifacts

- `docs/reverse/generated/re150-item-lighting-interaction-scope.csv`
- `docs/reverse/generated/re150-item-lighting-interaction-callsite-map.csv`
- `docs/reverse/functions/re150-item-lighting-interaction-caller-side-effect-map.md`

## Readiness decision

- decision: `caller-side-effect-map-blocked`
- code change readiness: `blocked`
- marker readiness: `blocked`
- next ticket: `RE-151`
- blocker: `missing-item-lighting-state-contract-and-symbolic-equivalence-proof`

## Validation

- `python3 -m pytest tests/reverse/test_re150_item_lighting_callsite_map.py -q`
- `python3 -m pytest tests/reverse -q`
- metadata-only guard over RE-150 artifacts
