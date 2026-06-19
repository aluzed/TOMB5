# RE-366 runtime callee bridge candidate proof export

## Goal

Produce a candidate-scoped metadata-only proof export for runtime callee bridge service candidate `a01f47cb95a4` without committing raw local identity.

## Inputs

- Upstream handoff: `docs/reverse/generated/re365-runtime-callee-bridge-readiness-gate-handoff.csv`
- RE-365 candidates: `docs/reverse/generated/re365-runtime-callee-bridge-readiness-gate-candidates.csv`
- Local function export: `docs/reverse/generated/ghidra-functions.csv`
- Local repo function map: `docs/reverse/generated/repo-function-map.csv`

## Progress tracker

- [x] RE-365 candidate proof-export handoff validated.
- [x] Selected candidate context reconstructed inside the generator only.
- [x] Candidate-scoped source-symbolic rows emitted without raw identity columns.
- [x] Domain/pivot/source-patch readiness kept blocked.
- [x] Source-backed callsite-map follow-up selected.

## Generated artifacts

- `docs/reverse/generated/re366-runtime-callee-bridge-candidate-proof-contexts.csv`
- `docs/reverse/generated/re366-runtime-callee-bridge-candidate-proof-gate.csv`
- `docs/reverse/generated/re366-runtime-callee-bridge-candidate-proof-summary.csv`
- `docs/reverse/generated/re366-runtime-callee-bridge-candidate-proof-handoff.csv`
- `docs/reverse/functions/re366-runtime-callee-bridge-candidate-proof-export.md`

## Findings

- Selected candidate id: `a01f47cb95a4`
- Source-symbolic context rows: `11`
- Caller context rows: `0`
- Callee context rows: `11`
- Direct repo symbol rows: `0`
- Candidate-level proof rows: `0`
- Ready to reopen domain selection: `0`
- Source patch authorized rows: `0`

## Readiness decision

The candidate has useful source-symbolic caller context across GPU/display, movie playback, loading, and platform-entry modules, but no direct source-backed candidate proof. Domain and pivot remain `none`, and code readiness remains blocked.

## Follow-up ticket breakdown

- `RE-367` / `runtime-callee-bridge-candidate-callsite-map`: build a source-backed callsite map for candidate `a01f47cb95a4`.
  - Inputs: RE-366 context/proof rows plus local source files and repo map metadata.
  - Deliverables: source-backed callsite rows with real file/line references, proof/blocker rows, and a handoff that either selects a proof pivot or stays blocked.
  - Stop condition: if source-backed callsites cannot prove candidate-level behavior without raw evidence, keep source/code readiness blocked and return to the parent platform/frontend queue.

## Validation commands

- `python -m pytest tests/reverse/test_re366_runtime_callee_bridge_candidate_proof_export.py -q`
- `python scripts/reverse/re366_runtime_callee_bridge_candidate_proof_export.py --repo .`
- `python -m pytest tests/reverse -q`
