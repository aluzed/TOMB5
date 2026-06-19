# RE-355 frontend display/menu service callsite readiness gate

## Goal

Gate the RE-354 source-backed callsite map and decide whether any frontend display/menu callsite family can reopen a proof domain or authorize a source patch.

## Inputs

- Upstream handoff: `docs/reverse/generated/re354-frontend-display-menu-service-candidate-callsite-handoff.csv`
- Source-backed callsite map: `docs/reverse/generated/re354-frontend-display-menu-service-candidate-callsite-map.csv`
- Source context functions: `docs/reverse/generated/re354-frontend-display-menu-service-candidate-callsite-functions.csv`
- Deferred candidate order: `docs/reverse/generated/re352-frontend-display-menu-service-readiness-gate-candidates.csv`

## Progress tracker

- [x] RE-354 callsite handoff validated.
- [x] RE-352 deferred candidate order verified fail-closed.
- [x] Callsite families grouped from metadata-only rows.
- [x] Domain/pivot/source-patch readiness denied because candidate-level proof rows remain absent.
- [x] Next deferred frontend display/menu candidate selected.

## Generated artifacts

- `docs/reverse/generated/re355-frontend-display-menu-service-callsite-readiness-families.csv`
- `docs/reverse/generated/re355-frontend-display-menu-service-callsite-readiness-decision.csv`
- `docs/reverse/generated/re355-frontend-display-menu-service-callsite-readiness-summary.csv`
- `docs/reverse/generated/re355-frontend-display-menu-service-callsite-readiness-handoff.csv`
- `docs/reverse/functions/re355-frontend-display-menu-service-callsite-readiness-gate.md`

## Findings

- Selected candidate id: `de919274685f`
- Source context functions: `25`
- Source-backed callsite rows: `326`
- Callsite families: `9`
- Implemented callsite families: `9`
- Stub-only callsite families: `0`
- Candidate-level proof rows: `0`
- Ready to reopen domain selection: `0`
- Source patch authorized rows: `0`

## Readiness decision

The callsite families are source-backed and useful prioritization evidence, but they do not prove candidate-level behavior for the unmapped selected candidate. Domain and pivot stay `none`; code readiness remains `blocked`.

## Follow-up ticket breakdown

- `RE-356` / `frontend-display-menu-service-next-candidate-proof-export`: reconstruct candidate `4c90c6af8f9d` and export source-symbolic proof context for the deferred frontend display/menu candidate.
  - Inputs: RE-355 decision/handoff plus RE-352 candidate queue.
  - Deliverables: next-candidate context/proof rows and a handoff to either source-backed callsite mapping or queue exhaustion.
  - Stop condition: if the next candidate also lacks candidate-level proof, keep source/code readiness blocked.

## Validation commands

- `python -m pytest tests/reverse/test_re355_frontend_display_menu_service_callsite_readiness_gate.py -q`
- `python scripts/reverse/re355_frontend_display_menu_service_callsite_readiness_gate.py --repo .`
- `python -m pytest tests/reverse -q`
