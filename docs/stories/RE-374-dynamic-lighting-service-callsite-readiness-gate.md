# RE-374 dynamic-lighting service callsite readiness gate

## Goal

Gate the RE-373 source-backed callsite map and decide whether any dynamic-lighting callsite family can reopen a proof domain or authorize a source patch.

## Inputs

- Upstream handoff: `docs/reverse/generated/re373-dynamic-lighting-service-candidate-callsite-handoff.csv`
- Source-backed callsite map: `docs/reverse/generated/re373-dynamic-lighting-service-candidate-callsite-map.csv`
- Source context functions: `docs/reverse/generated/re373-dynamic-lighting-service-candidate-callsite-functions.csv`
- Deferred candidate order: `docs/reverse/generated/re371-dynamic-lighting-service-readiness-gate-candidates.csv`

## Progress tracker

- [x] RE-373 callsite handoff validated.
- [x] RE-371 deferred candidate order verified fail-closed.
- [x] Callsite families grouped from metadata-only rows.
- [x] Domain/pivot/source-patch readiness denied because candidate-level proof rows remain absent.
- [x] Next deferred dynamic-lighting candidate selected.

## Generated artifacts

- `docs/reverse/generated/re374-dynamic-lighting-service-callsite-readiness-families.csv`
- `docs/reverse/generated/re374-dynamic-lighting-service-callsite-readiness-decision.csv`
- `docs/reverse/generated/re374-dynamic-lighting-service-callsite-readiness-summary.csv`
- `docs/reverse/generated/re374-dynamic-lighting-service-callsite-readiness-handoff.csv`
- `docs/reverse/functions/re374-dynamic-lighting-service-callsite-readiness-gate.md`

## Findings

- Selected candidate id: `f5d0099b5511`
- Source context functions: `23`
- Source-backed callsite rows: `129`
- Callsite families: `7`
- Implemented callsite families: `6`
- Stub-only callsite families: `1`
- Candidate-level proof rows: `0`
- Ready to reopen domain selection: `0`
- Source patch authorized rows: `0`

## Readiness decision

The callsite families are source-backed and useful prioritization evidence, but they do not prove candidate-level behavior for the unmapped selected candidate. Domain and pivot stay `none`; code readiness remains `blocked`.

## Follow-up ticket breakdown

- `RE-375` / `dynamic-lighting-service-next-candidate-proof-export`: reconstruct candidate `3a208e2bf745` and export source-symbolic proof context for the deferred dynamic-lighting candidate.
  - Inputs: RE-374 decision/handoff plus RE-371 candidate queue.
  - Deliverables: next-candidate context/proof rows and a handoff to either source-backed callsite mapping or queue exhaustion.
  - Stop condition: if the next candidate also lacks candidate-level proof, keep source/code readiness blocked.

## Validation commands

- `python -m pytest tests/reverse/test_re374_dynamic_lighting_service_callsite_readiness_gate.py -q`
- `python scripts/reverse/re374_dynamic_lighting_service_callsite_readiness_gate.py --repo .`
- `python -m pytest tests/reverse -q`
