# RE-344 cd-load-audio service readiness gate

## Goal

Gate the RE-343 `cd-load-audio-service` candidates and decide whether any row can reopen proof-domain selection or authorize a source patch.

## Inputs

- Upstream handoff: `docs/reverse/generated/re343-ghidra-platform-frontend-service-narrow-handoff.csv`
- Candidate rows: `docs/reverse/generated/re343-ghidra-platform-frontend-service-narrow-candidates.csv`

## Progress tracker

- [x] RE-343 cd-load-audio service handoff validated.
- [x] Selected candidate set checked for drift.
- [x] Candidate-level proof requirement evaluated.
- [x] Domain/source-patch authorization denied.
- [x] Still-narrower proof export handoff emitted.

## Generated artifacts

- `docs/reverse/generated/re344-cd-load-audio-service-readiness-gate-candidates.csv`
- `docs/reverse/generated/re344-cd-load-audio-service-readiness-gate-gates.csv`
- `docs/reverse/generated/re344-cd-load-audio-service-readiness-gate-summary.csv`
- `docs/reverse/generated/re344-cd-load-audio-service-readiness-gate-handoff.csv`
- `docs/reverse/functions/re344-cd-load-audio-service-readiness-gate.md`

## Findings

- Selected narrow subcluster: `cd-load-audio-service`
- Input candidates: `2`
- Gate rows: `1`
- Ready to reopen domain selection: `0`
- Source patch authorized rows: `0`

## Readiness decision

The `cd-load-audio-service` rows remain source-symbolic. Domain and pivot stay `none` / `none`, and code readiness remains `blocked`.

## Follow-up ticket breakdown

- `RE-345` / `cd-load-audio-service-candidate-proof-export`: export still-narrower candidate proof context for `1e35f3f4fb97`.
  - Inputs: RE-344 candidate/gate CSVs plus RE-343 context.
  - Deliverables: metadata-only proof export, summary/handoff, story.
  - Stop condition: if no candidate-level proof exists, keep source/code readiness blocked and propose the next deferred hypothesis.

## Validation commands

- `python -m pytest tests/reverse/test_re344_cd_load_audio_service_readiness_gate.py -q`
- `python scripts/reverse/re344_cd_load_audio_service_readiness_gate.py --repo .`
- `python -m pytest tests/reverse -q`
