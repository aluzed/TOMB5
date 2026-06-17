# RE-324 switch-door-control helper candidate proof export

## Goal

Produce a candidate-scoped metadata-only proof export for switch-door-control helper candidate `8d1fc6fc3cfc` without committing raw local identity.

## Inputs

- Upstream handoff: `docs/reverse/generated/re323-switch-door-control-helper-readiness-gate-handoff.csv`
- RE-323 candidates: `docs/reverse/generated/re323-switch-door-control-helper-readiness-gate-candidates.csv`
- Local function export: `docs/reverse/generated/ghidra-functions.csv`
- Local repo function map: `docs/reverse/generated/repo-function-map.csv`

## Progress tracker

- [x] RE-323 candidate proof-export handoff validated.
- [x] Selected candidate context reconstructed inside the generator only.
- [x] Candidate-scoped source-symbolic rows emitted without raw identity columns.
- [x] Domain/pivot/source-patch readiness kept blocked.
- [x] Source-backed callsite-map follow-up selected.

## Generated artifacts

- `docs/reverse/generated/re324-switch-door-control-helper-candidate-proof-contexts.csv`
- `docs/reverse/generated/re324-switch-door-control-helper-candidate-proof-gate.csv`
- `docs/reverse/generated/re324-switch-door-control-helper-candidate-proof-summary.csv`
- `docs/reverse/generated/re324-switch-door-control-helper-candidate-proof-handoff.csv`
- `docs/reverse/functions/re324-switch-door-control-helper-candidate-proof-export.md`

## Findings

- Selected candidate id: `8d1fc6fc3cfc`
- Source-symbolic context rows: `23`
- Caller context rows: `22`
- Callee context rows: `1`
- Direct repo symbol rows: `0`
- Candidate-level proof rows: `0`
- Ready to reopen domain selection: `0`
- Source patch authorized rows: `0`

## Readiness decision

The candidate has useful source-symbolic caller/callee context, but no direct source-backed candidate proof. Domain and pivot remain `none`, and code readiness remains blocked.

## Follow-up ticket breakdown

- `RE-325` / `switch-door-control-helper-candidate-callsite-map`: build a source-backed callsite map for candidate `8d1fc6fc3cfc`.
  - Inputs: RE-324 context/proof rows plus local source files and repo map metadata.
  - Deliverables: source-backed callsite rows with real file/line references, proof/blocker rows, and a handoff that either selects a proof pivot or stays blocked.
  - Stop condition: if source-backed callsites cannot prove candidate-level behavior without raw evidence, keep source/code readiness blocked and defer to the next switch/door candidate action.

## Validation commands

- `python -m pytest tests/reverse/test_re324_switch_door_control_helper_candidate_proof_export.py -q`
- `python scripts/reverse/re324_switch_door_control_helper_candidate_proof_export.py --repo .`
- `python -m pytest tests/reverse -q`
