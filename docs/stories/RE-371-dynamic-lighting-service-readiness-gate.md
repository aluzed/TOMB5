# RE-371 dynamic-lighting service readiness gate

## Goal

Gate the RE-370 `dynamic-lighting-service` candidates and decide whether any row can reopen proof-domain selection or authorize a source patch.

## Inputs

- Upstream handoff: `docs/reverse/generated/re370-ghidra-effects-lighting-narrow-handoff.csv`
- Candidate rows: `docs/reverse/generated/re370-ghidra-effects-lighting-narrow-candidates.csv`

## Progress tracker

- [x] RE-370 dynamic-lighting service handoff validated.
- [x] Selected candidate set checked for drift.
- [x] Candidate-level proof requirement evaluated.
- [x] Domain/source-patch authorization denied.
- [x] Still-narrower proof export handoff emitted.

## Generated artifacts

- `docs/reverse/generated/re371-dynamic-lighting-service-readiness-gate-candidates.csv`
- `docs/reverse/generated/re371-dynamic-lighting-service-readiness-gate-gates.csv`
- `docs/reverse/generated/re371-dynamic-lighting-service-readiness-gate-summary.csv`
- `docs/reverse/generated/re371-dynamic-lighting-service-readiness-gate-handoff.csv`
- `docs/reverse/functions/re371-dynamic-lighting-service-readiness-gate.md`

## Findings

- Selected narrow subcluster: `dynamic-lighting-service`
- Input candidates: `2`
- Gate rows: `1`
- Ready to reopen domain selection: `0`
- Source patch authorized rows: `0`

## Readiness decision

The `dynamic-lighting-service` rows remain source-symbolic. Domain and pivot stay `none` / `none`, and code readiness remains `blocked`.

## Follow-up ticket breakdown

- `RE-372` / `dynamic-lighting-service-candidate-proof-export`: export still-narrower candidate proof context for `f5d0099b5511`.
  - Inputs: RE-371 candidate/gate CSVs plus RE-370 context.
  - Deliverables: metadata-only proof export, summary/handoff, story.
  - Stop condition: if no candidate-level proof exists, keep source/code readiness blocked and propose the next deferred hypothesis.

## Validation commands

- `python -m pytest tests/reverse/test_re371_dynamic_lighting_service_readiness_gate.py -q`
- `python scripts/reverse/re371_dynamic_lighting_service_readiness_gate.py --repo .`
- `python -m pytest tests/reverse -q`
