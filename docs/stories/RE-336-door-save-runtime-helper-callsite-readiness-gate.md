# RE-336 door-save-runtime helper callsite readiness gate

## Goal

Gate the RE-335 source-backed callsite map and decide whether any door-save-runtime callsite family can reopen a proof domain or authorize a source patch.

## Inputs

- Upstream handoff: `docs/reverse/generated/re335-door-save-runtime-helper-candidate-callsite-handoff.csv`
- Source-backed callsite map: `docs/reverse/generated/re335-door-save-runtime-helper-candidate-callsite-map.csv`
- Source context functions: `docs/reverse/generated/re335-door-save-runtime-helper-candidate-callsite-functions.csv`
- Candidate queue: `docs/reverse/generated/re333-door-save-runtime-helper-readiness-gate-candidates.csv`

## Progress tracker

- [x] RE-335 callsite handoff validated.
- [x] RE-333 single-candidate queue verified fail-closed.
- [x] Door-save-runtime callsite families grouped and readiness-gated.
- [x] Candidate-level proof and source-patch authorization denied for every family.
- [x] Candidate queue exhaustion handoff emitted.

## Generated artifacts

- `docs/reverse/generated/re336-door-save-runtime-helper-callsite-readiness-families.csv`
- `docs/reverse/generated/re336-door-save-runtime-helper-callsite-readiness-decision.csv`
- `docs/reverse/generated/re336-door-save-runtime-helper-callsite-readiness-summary.csv`
- `docs/reverse/generated/re336-door-save-runtime-helper-callsite-readiness-handoff.csv`
- `docs/reverse/functions/re336-door-save-runtime-helper-callsite-readiness-gate.md`

## Findings

- Source context functions: `14`
- Source-backed callsite rows: `185`
- Callsite families: `13`
- Implemented callsite families: `12`
- Stub-only callsite families: `1`
- Candidate-level proof rows: `0`
- Ready to reopen domain selection: `0`
- Source patch authorized rows: `0`

## Readiness decision

No RE-335 door-save-runtime callsite family proves candidate-level behavior. Domain and pivot stay `none`; source/code readiness remains `blocked`, and the candidate queue is exhausted.

## Follow-up ticket breakdown

- `TBD` / `door-save-runtime-helper-candidate-queue-exhausted`: no remaining deferred door-save-runtime helper candidate exists after `f457f2772655`.
  - Inputs: RE-333 candidate queue and RE-336 denial handoff.
  - Deliverables: await next parent-subcluster selection or changed non-raw candidate-level proof evidence before reopening domain selection.
  - Stop condition: candidate queue is exhausted and source/code readiness remains blocked.

## Validation commands

- `python -m pytest tests/reverse/test_re336_door_save_runtime_helper_callsite_readiness_gate.py -q`
- `python scripts/reverse/re336_door_save_runtime_helper_callsite_readiness_gate.py --repo .`
- `python -m pytest tests/reverse -q`
