# RE-356 frontend display/menu service next candidate proof export

## Goal

Produce a candidate-scoped metadata-only proof export for deferred frontend display/menu service candidate `4c90c6af8f9d` without committing raw local identity.

## Inputs

- Upstream handoff: `docs/reverse/generated/re355-frontend-display-menu-service-callsite-readiness-handoff.csv`
- RE-352 candidates: `docs/reverse/generated/re352-frontend-display-menu-service-readiness-gate-candidates.csv`
- Local function export: `docs/reverse/generated/ghidra-functions.csv`
- Local repo function map: `docs/reverse/generated/repo-function-map.csv`

## Progress tracker

- [x] RE-355 next-candidate handoff validated.
- [x] Deferred RE-352 candidate row verified fail-closed.
- [x] Selected next-candidate context reconstructed inside the generator only.
- [x] Candidate-scoped source-symbolic rows emitted without raw identity columns.
- [x] Domain/pivot/source-patch readiness kept blocked.
- [x] Source-backed next-candidate callsite-map follow-up selected.

## Generated artifacts

- `docs/reverse/generated/re356-frontend-display-menu-service-next-candidate-proof-contexts.csv`
- `docs/reverse/generated/re356-frontend-display-menu-service-next-candidate-proof-gate.csv`
- `docs/reverse/generated/re356-frontend-display-menu-service-next-candidate-proof-summary.csv`
- `docs/reverse/generated/re356-frontend-display-menu-service-next-candidate-proof-handoff.csv`
- `docs/reverse/functions/re356-frontend-display-menu-service-next-candidate-proof-export.md`

## Findings

- Selected candidate id: `4c90c6af8f9d`
- Previous candidate id: `de919274685f`
- Source-symbolic context rows: `18`
- Caller context rows: `18`
- Callee context rows: `0`
- Direct repo symbol rows: `0`
- Candidate-level proof rows: `0`
- Ready to reopen domain selection: `0`
- Source patch authorized rows: `0`

## Readiness decision

The next candidate has useful source-symbolic caller context across frontend display/menu, file-service, load/save, and platform modules, but no direct source-backed candidate proof. Domain and pivot remain `none`, and code readiness remains blocked.

## Follow-up ticket breakdown

- `RE-357` / `frontend-display-menu-service-next-candidate-callsite-map`: build a source-backed callsite map for candidate `4c90c6af8f9d`.
  - Inputs: RE-356 context/proof rows plus local source files and repo map metadata.
  - Deliverables: source-backed callsite rows with file/line references, proof/blocker rows, and a handoff that either selects a proof pivot or marks the frontend display/menu candidate queue exhausted.
  - Stop condition: if source-backed callsites cannot prove candidate-level behavior without raw evidence, keep source/code readiness blocked and close or reprioritize from the parent queue.

## Validation commands

- `python -m pytest tests/reverse/test_re356_frontend_display_menu_service_next_candidate_proof_export.py -q`
- `python scripts/reverse/re356_frontend_display_menu_service_next_candidate_proof_export.py --repo .`
- `python -m pytest tests/reverse -q`
