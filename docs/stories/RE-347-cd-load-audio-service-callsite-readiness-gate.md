# RE-347 cd-load-audio service callsite readiness gate

## Goal

Gate the RE-346 source-backed callsite map and decide whether any callsite family can reopen a proof domain or authorize a source patch.

## Inputs

- Upstream handoff: `docs/reverse/generated/re346-cd-load-audio-service-candidate-callsite-handoff.csv`
- Source-backed callsite map: `docs/reverse/generated/re346-cd-load-audio-service-candidate-callsite-map.csv`
- Source context functions: `docs/reverse/generated/re346-cd-load-audio-service-candidate-callsite-functions.csv`
- Deferred candidate order: `docs/reverse/generated/re344-cd-load-audio-service-readiness-gate-candidates.csv`

## Progress tracker

- [x] RE-346 callsite handoff validated.
- [x] RE-344 deferred candidate order verified fail-closed.
- [x] Callsite families grouped and readiness-gated.
- [x] Candidate-level proof and source-patch authorization denied for every family.
- [x] Next deferred candidate proof export selected.

## Generated artifacts

- `docs/reverse/generated/re347-cd-load-audio-service-callsite-readiness-families.csv`
- `docs/reverse/generated/re347-cd-load-audio-service-callsite-readiness-decision.csv`
- `docs/reverse/generated/re347-cd-load-audio-service-callsite-readiness-summary.csv`
- `docs/reverse/generated/re347-cd-load-audio-service-callsite-readiness-handoff.csv`
- `docs/reverse/functions/re347-cd-load-audio-service-callsite-readiness-gate.md`

## Findings

- Source context functions: `34`
- Source-backed callsite rows: `266`
- Callsite families: `9`
- Implemented callsite families: `9`
- Stub-only callsite families: `0`
- Candidate-level proof rows: `0`
- Ready to reopen domain selection: `0`
- Source patch authorized rows: `0`

## Readiness decision

The source-backed callsite map is rich but still does not prove candidate-level behavior. Domain and pivot remain `none`; code readiness remains `blocked`.

## Follow-up ticket breakdown

- `RE-348` / `cd-load-audio-service-next-candidate-proof-export`: export candidate-scoped proof metadata for deferred candidate `653df7c5909b`.
  - Inputs: RE-344 candidate gate rows plus local function exports and repo map metadata.
  - Deliverables: metadata-only proof context/gate/summary/handoff for the next candidate.
  - Stop condition: if no candidate-level proof exists, keep source/code readiness blocked and decide whether the cd-load-audio candidate queue is exhausted.

## Validation commands

- `python -m pytest tests/reverse/test_re347_cd_load_audio_service_callsite_readiness_gate.py -q`
- `python scripts/reverse/re347_cd_load_audio_service_callsite_readiness_gate.py --repo .`
- `python -m pytest tests/reverse -q`
