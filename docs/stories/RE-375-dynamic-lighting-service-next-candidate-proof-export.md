# RE-375 dynamic-lighting service next-candidate proof export

## Goal

Produce a candidate-scoped metadata-only proof export for deferred dynamic-lighting service candidate `3a208e2bf745` after `f5d0099b5511` stayed blocked, without committing raw local identity.

## Inputs

- Upstream handoff: `docs/reverse/generated/re374-dynamic-lighting-service-callsite-readiness-handoff.csv`
- RE-371 candidates: `docs/reverse/generated/re371-dynamic-lighting-service-readiness-gate-candidates.csv`
- Local function export: `docs/reverse/generated/ghidra-functions.csv`
- Local repo function map: `docs/reverse/generated/repo-function-map.csv`

## Progress tracker

- [x] RE-374 next-candidate proof-export handoff validated.
- [x] RE-371 deferred candidate row verified fail-closed.
- [x] Next candidate context reconstructed inside the generator only.
- [x] Candidate-scoped source-symbolic rows emitted without raw identity columns.
- [x] Domain/pivot/source-patch readiness kept blocked.
- [x] Source-backed next-candidate callsite-map follow-up selected.

## Generated artifacts

- `docs/reverse/generated/re375-dynamic-lighting-service-next-candidate-proof-contexts.csv`
- `docs/reverse/generated/re375-dynamic-lighting-service-next-candidate-proof-gate.csv`
- `docs/reverse/generated/re375-dynamic-lighting-service-next-candidate-proof-summary.csv`
- `docs/reverse/generated/re375-dynamic-lighting-service-next-candidate-proof-handoff.csv`
- `docs/reverse/functions/re375-dynamic-lighting-service-next-candidate-proof-export.md`

## Findings

- Previous candidate id: `f5d0099b5511`
- Selected candidate id: `3a208e2bf745`
- Source-symbolic context rows: `21`
- Caller context rows: `21`
- Callee context rows: `0`
- Direct repo symbol rows: `0`
- Candidate-level proof rows: `0`
- Ready to reopen domain selection: `0`
- Source patch authorized rows: `0`

## Readiness decision

The next candidate has useful source-symbolic caller context across dynamic lighting controls, flame emitters, trap/switch/door runtime code, effect emitters, moving traps, and geometry/collision helpers, but no direct source-backed candidate proof. Domain and pivot remain `none`, and code readiness remains blocked.

## Follow-up ticket breakdown

- `RE-376` / `dynamic-lighting-service-next-candidate-callsite-map`: build a source-backed callsite map for candidate `3a208e2bf745`.
  - Inputs: RE-375 context/proof rows plus local source files and repo map metadata.
  - Deliverables: source-backed callsite rows with real file/line references, proof/blocker rows, and a handoff that either selects a proof pivot or closes the dynamic-lighting candidate queue.
  - Stop condition: if source-backed callsites cannot prove candidate-level behavior without raw evidence, keep source/code readiness blocked and close or transition from the dynamic-lighting subcluster.

## Validation commands

- `python -m pytest tests/reverse/test_re375_dynamic_lighting_service_next_candidate_proof_export.py -q`
- `python scripts/reverse/re375_dynamic_lighting_service_next_candidate_proof_export.py --repo .`
- `python -m pytest tests/reverse -q`
