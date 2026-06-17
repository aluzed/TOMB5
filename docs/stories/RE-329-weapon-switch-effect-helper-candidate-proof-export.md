# RE-329 weapon-switch-effect helper candidate proof export

## Goal

Produce a candidate-scoped metadata-only proof export for weapon-switch-effect helper candidate `1ddbda046e37` without committing raw local identity.

## Inputs

- Upstream handoff: `docs/reverse/generated/re328-weapon-switch-effect-helper-readiness-gate-handoff.csv`
- RE-328 candidates: `docs/reverse/generated/re328-weapon-switch-effect-helper-readiness-gate-candidates.csv`
- Local function export: `docs/reverse/generated/ghidra-functions.csv`
- Local repo function map: `docs/reverse/generated/repo-function-map.csv`

## Progress tracker

- [x] RE-328 candidate proof-export handoff validated.
- [x] Selected candidate context reconstructed inside the generator only.
- [x] Candidate-scoped source-symbolic rows emitted without raw identity columns.
- [x] Domain/pivot/source-patch readiness kept blocked.
- [x] Source-backed callsite-map follow-up selected.

## Generated artifacts

- `docs/reverse/generated/re329-weapon-switch-effect-helper-candidate-proof-contexts.csv`
- `docs/reverse/generated/re329-weapon-switch-effect-helper-candidate-proof-gate.csv`
- `docs/reverse/generated/re329-weapon-switch-effect-helper-candidate-proof-summary.csv`
- `docs/reverse/generated/re329-weapon-switch-effect-helper-candidate-proof-handoff.csv`
- `docs/reverse/functions/re329-weapon-switch-effect-helper-candidate-proof-export.md`

## Findings

- Selected candidate id: `1ddbda046e37`
- Source-symbolic context rows: `17`
- Caller context rows: `1`
- Callee context rows: `16`
- Direct repo symbol rows: `0`
- Candidate-level proof rows: `0`
- Ready to reopen domain selection: `0`
- Source patch authorized rows: `0`

## Readiness decision

The candidate has useful source-symbolic caller/callee context, but no direct source-backed candidate proof. Domain and pivot remain `none`, and code readiness remains blocked.

## Follow-up ticket breakdown

- `RE-330` / `weapon-switch-effect-helper-candidate-callsite-map`: build a source-backed callsite map for candidate `1ddbda046e37`.
  - Inputs: RE-329 context/proof rows plus local source files and repo map metadata.
  - Deliverables: source-backed callsite rows with real file/line references, proof/blocker rows, and a handoff that either selects a proof pivot or stays blocked.
  - Stop condition: if source-backed callsites cannot prove candidate-level behavior without raw evidence, keep source/code readiness blocked and defer to the next weapon/switch candidate action.

## Validation commands

- `python -m pytest tests/reverse/test_re329_weapon_switch_effect_helper_candidate_proof_export.py -q`
- `python scripts/reverse/re329_weapon_switch_effect_helper_candidate_proof_export.py --repo .`
- `python -m pytest tests/reverse -q`
