# RE-372 dynamic-lighting service candidate proof export

## Goal

Produce a candidate-scoped metadata-only proof export for dynamic-lighting service candidate `f5d0099b5511` without committing raw local identity.

## Inputs

- Upstream handoff: `docs/reverse/generated/re371-dynamic-lighting-service-readiness-gate-handoff.csv`
- RE-371 candidates: `docs/reverse/generated/re371-dynamic-lighting-service-readiness-gate-candidates.csv`
- Local function export: `docs/reverse/generated/ghidra-functions.csv`
- Local repo function map: `docs/reverse/generated/repo-function-map.csv`

## Progress tracker

- [x] RE-371 candidate proof-export handoff validated.
- [x] Selected candidate context reconstructed inside the generator only.
- [x] Candidate-scoped source-symbolic rows emitted without raw identity columns.
- [x] Domain/pivot/source-patch readiness kept blocked.
- [x] Source-backed callsite-map follow-up selected.

## Generated artifacts

- `docs/reverse/generated/re372-dynamic-lighting-service-candidate-proof-contexts.csv`
- `docs/reverse/generated/re372-dynamic-lighting-service-candidate-proof-gate.csv`
- `docs/reverse/generated/re372-dynamic-lighting-service-candidate-proof-summary.csv`
- `docs/reverse/generated/re372-dynamic-lighting-service-candidate-proof-handoff.csv`
- `docs/reverse/functions/re372-dynamic-lighting-service-candidate-proof-export.md`

## Findings

- Selected candidate id: `f5d0099b5511`
- Source-symbolic context rows: `23`
- Caller context rows: `23`
- Callee context rows: `0`
- Direct repo symbol rows: `0`
- Candidate-level proof rows: `0`
- Ready to reopen domain selection: `0`
- Source patch authorized rows: `0`

## Readiness decision

The candidate has useful source-symbolic caller context across dynamic lighting controls, torch/flare lighting, flame emitters, creature controls, weapon dynamics, and Lara runtime code, but no direct source-backed candidate proof. Domain and pivot remain `none`, and code readiness remains blocked.

## Follow-up ticket breakdown

- `RE-373` / `dynamic-lighting-service-candidate-callsite-map`: build a source-backed callsite map for candidate `f5d0099b5511`.
  - Inputs: RE-372 context/proof rows plus local source files and repo map metadata.
  - Deliverables: source-backed callsite rows with real file/line references, proof/blocker rows, and a handoff that either selects a proof pivot or stays blocked.
  - Stop condition: if source-backed callsites cannot prove candidate-level behavior without raw evidence, keep source/code readiness blocked and defer to the other dynamic-lighting candidate.

## Validation commands

- `python -m pytest tests/reverse/test_re372_dynamic_lighting_service_candidate_proof_export.py -q`
- `python scripts/reverse/re372_dynamic_lighting_service_candidate_proof_export.py --repo .`
- `python -m pytest tests/reverse -q`
