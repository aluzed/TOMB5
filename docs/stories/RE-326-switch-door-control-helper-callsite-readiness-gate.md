# RE-326 switch-door-control helper callsite readiness gate

## Goal

Gate the RE-325 source-backed callsite map and decide whether any switch-door-control callsite family can reopen a proof domain or authorize a source patch.

## Inputs

- Upstream handoff: `docs/reverse/generated/re325-switch-door-control-helper-candidate-callsite-handoff.csv`
- Source-backed callsite map: `docs/reverse/generated/re325-switch-door-control-helper-candidate-callsite-map.csv`
- Source context functions: `docs/reverse/generated/re325-switch-door-control-helper-candidate-callsite-functions.csv`
- Candidate queue: `docs/reverse/generated/re323-switch-door-control-helper-readiness-gate-candidates.csv`

## Progress tracker

- [x] RE-325 callsite handoff validated.
- [x] RE-323 single-candidate queue verified fail-closed.
- [x] Switch-door-control callsite families grouped and readiness-gated.
- [x] Candidate-level proof and source-patch authorization denied for every family.
- [x] Candidate queue exhaustion handoff emitted.

## Generated artifacts

- `docs/reverse/generated/re326-switch-door-control-helper-callsite-readiness-families.csv`
- `docs/reverse/generated/re326-switch-door-control-helper-callsite-readiness-decision.csv`
- `docs/reverse/generated/re326-switch-door-control-helper-callsite-readiness-summary.csv`
- `docs/reverse/generated/re326-switch-door-control-helper-callsite-readiness-handoff.csv`
- `docs/reverse/functions/re326-switch-door-control-helper-callsite-readiness-gate.md`

## Findings

- Source context functions: `22`
- Source-backed callsite rows: `39`
- Callsite families: `5`
- Implemented callsite families: `4`
- Stub-only callsite families: `1`
- Candidate-level proof rows: `0`
- Ready to reopen domain selection: `0`
- Source patch authorized rows: `0`

## Readiness decision

No RE-325 switch-door-control callsite family proves candidate-level behavior. Domain and pivot stay `none`; source/code readiness remains `blocked`, and the candidate queue is exhausted.

## Follow-up ticket breakdown

- `TBD` / `switch-door-control-helper-candidate-queue-exhausted`: no remaining deferred switch-door-control helper candidate exists after `8d1fc6fc3cfc`.
  - Inputs: RE-323 candidate queue and RE-326 denial handoff.
  - Deliverables: await next parent-subcluster selection or changed non-raw candidate-level proof evidence before reopening domain selection.
  - Stop condition: candidate queue is exhausted and source/code readiness remains blocked.

## Validation commands

- `python -m pytest tests/reverse/test_re326_switch_door_control_helper_callsite_readiness_gate.py -q`
- `python scripts/reverse/re326_switch_door_control_helper_callsite_readiness_gate.py --repo .`
- `python -m pytest tests/reverse -q`
