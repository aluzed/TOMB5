# RE-331 weapon-switch-effect helper callsite readiness gate

## Goal

Gate the RE-330 source-backed callsite map and decide whether any weapon-switch-effect callsite family can reopen a proof domain or authorize a source patch.

## Inputs

- Upstream handoff: `docs/reverse/generated/re330-weapon-switch-effect-helper-candidate-callsite-handoff.csv`
- Source-backed callsite map: `docs/reverse/generated/re330-weapon-switch-effect-helper-candidate-callsite-map.csv`
- Source context functions: `docs/reverse/generated/re330-weapon-switch-effect-helper-candidate-callsite-functions.csv`
- Candidate queue: `docs/reverse/generated/re328-weapon-switch-effect-helper-readiness-gate-candidates.csv`

## Progress tracker

- [x] RE-330 callsite handoff validated.
- [x] RE-328 single-candidate queue verified fail-closed.
- [x] Weapon-switch-effect callsite families grouped and readiness-gated.
- [x] Candidate-level proof and source-patch authorization denied for every family.
- [x] Candidate queue exhaustion handoff emitted.

## Generated artifacts

- `docs/reverse/generated/re331-weapon-switch-effect-helper-callsite-readiness-families.csv`
- `docs/reverse/generated/re331-weapon-switch-effect-helper-callsite-readiness-decision.csv`
- `docs/reverse/generated/re331-weapon-switch-effect-helper-callsite-readiness-summary.csv`
- `docs/reverse/generated/re331-weapon-switch-effect-helper-callsite-readiness-handoff.csv`
- `docs/reverse/functions/re331-weapon-switch-effect-helper-callsite-readiness-gate.md`

## Findings

- Source context functions: `1`
- Source-backed callsite rows: `1`
- Callsite families: `1`
- Implemented callsite families: `0`
- Stub-only callsite families: `1`
- Candidate-level proof rows: `0`
- Ready to reopen domain selection: `0`
- Source patch authorized rows: `0`

## Readiness decision

No RE-330 weapon-switch-effect callsite family proves candidate-level behavior. Domain and pivot stay `none`; source/code readiness remains `blocked`, and the candidate queue is exhausted.

## Follow-up ticket breakdown

- `TBD` / `weapon-switch-effect-helper-candidate-queue-exhausted`: no remaining deferred weapon-switch-effect helper candidate exists after `1ddbda046e37`.
  - Inputs: RE-328 candidate queue and RE-331 denial handoff.
  - Deliverables: await next parent-subcluster selection or changed non-raw candidate-level proof evidence before reopening domain selection.
  - Stop condition: candidate queue is exhausted and source/code readiness remains blocked.

## Validation commands

- `python -m pytest tests/reverse/test_re331_weapon_switch_effect_helper_callsite_readiness_gate.py -q`
- `python scripts/reverse/re331_weapon_switch_effect_helper_callsite_readiness_gate.py --repo .`
- `python -m pytest tests/reverse -q`
