# RE-380 explosion/flare effect service candidate proof export

## Goal

Produce a candidate-scoped metadata-only proof export for explosion/flare effect service candidate `87d9c8a62335` without committing raw local identity.

## Inputs

- Upstream handoff: `docs/reverse/generated/re379-explosion-flare-effect-service-readiness-gate-handoff.csv`
- RE-379 candidates: `docs/reverse/generated/re379-explosion-flare-effect-service-readiness-gate-candidates.csv`
- Local function export: `docs/reverse/generated/ghidra-functions.csv`
- Local repo function map: `docs/reverse/generated/repo-function-map.csv`

## Progress tracker

- [x] RE-379 candidate proof-export handoff validated.
- [x] Selected candidate context reconstructed inside the generator only.
- [x] Candidate-scoped source-symbolic rows emitted without raw identity columns.
- [x] Domain/pivot/source-patch readiness kept blocked.
- [x] Source-backed callsite-map follow-up selected.

## Generated artifacts

- `docs/reverse/generated/re380-explosion-flare-effect-service-candidate-proof-contexts.csv`
- `docs/reverse/generated/re380-explosion-flare-effect-service-candidate-proof-gate.csv`
- `docs/reverse/generated/re380-explosion-flare-effect-service-candidate-proof-summary.csv`
- `docs/reverse/generated/re380-explosion-flare-effect-service-candidate-proof-handoff.csv`
- `docs/reverse/functions/re380-explosion-flare-effect-service-candidate-proof-export.md`

## Findings

- Selected candidate id: `87d9c8a62335`
- Source-symbolic context rows: `18`
- Caller context rows: `18`
- Callee context rows: `0`
- Direct repo symbol rows: `0`
- Candidate-level proof rows: `0`
- Ready to reopen domain selection: `0`
- Source patch authorized rows: `0`

## Readiness decision

The candidate has useful source-symbolic caller context across flare, flame, explosion, bubble, camera, weapon, collision, and Lara runtime code, but no direct source-backed candidate proof. Domain and pivot remain `none`, and code readiness remains blocked.

## Follow-up ticket breakdown

- `RE-381` / `explosion-flare-effect-service-candidate-callsite-map`: build a source-backed callsite map for candidate `87d9c8a62335`.
  - Inputs: RE-380 context/proof rows plus local source files and repo map metadata.
  - Deliverables: source-backed callsite rows with real file/line references, proof/blocker rows, and a handoff that either selects a proof pivot or stays blocked.
  - Stop condition: if source-backed callsites cannot prove candidate-level behavior without raw evidence, keep source/code readiness blocked and close or defer the explosion/flare service queue safely.

## Validation commands

- `python -m pytest tests/reverse/test_re380_explosion_flare_effect_service_candidate_proof_export.py -q`
- `python scripts/reverse/re380_explosion_flare_effect_service_candidate_proof_export.py --repo .`
- `python -m pytest tests/reverse -q`
