# RE-352 frontend display/menu service readiness gate

## Goal

Gate the RE-351 `frontend-display-menu-service` candidates and decide whether any row can reopen proof-domain selection or authorize a source patch.

## Inputs

- Upstream handoff: `docs/reverse/generated/re351-platform-frontend-service-post-cd-load-audio-next-subcluster-selection-handoff.csv`
- Candidate rows: `docs/reverse/generated/re351-platform-frontend-service-post-cd-load-audio-next-subcluster-selection-candidates.csv`
- Source-context metadata: `docs/reverse/generated/re343-ghidra-platform-frontend-service-narrow-candidates.csv`

## Progress tracker

- [x] RE-351 frontend display/menu service handoff validated.
- [x] Selected candidate set checked for drift.
- [x] Candidate-level proof requirement evaluated.
- [x] Domain/source-patch authorization denied.
- [x] Still-narrower proof export handoff emitted.

## Generated artifacts

- `docs/reverse/generated/re352-frontend-display-menu-service-readiness-gate-candidates.csv`
- `docs/reverse/generated/re352-frontend-display-menu-service-readiness-gate-gates.csv`
- `docs/reverse/generated/re352-frontend-display-menu-service-readiness-gate-summary.csv`
- `docs/reverse/generated/re352-frontend-display-menu-service-readiness-gate-handoff.csv`
- `docs/reverse/functions/re352-frontend-display-menu-service-readiness-gate.md`

## Findings

- Selected narrow subcluster: `frontend-display-menu-service`
- Input candidates: `2`
- Gate rows: `1`
- Ready to reopen domain selection: `0`
- Source patch authorized rows: `0`

## Readiness decision

The `frontend-display-menu-service` rows remain source-symbolic. Domain and pivot stay `none` / `none`, and code readiness remains `blocked`.

## Follow-up ticket breakdown

- `RE-353` / `frontend-display-menu-service-candidate-proof-export`: export still-narrower candidate proof context for `de919274685f`.
  - Inputs: RE-352 candidate/gate CSVs plus RE-343 source-context metadata.
  - Deliverables: metadata-only proof export, summary/handoff, story.
  - Stop condition: if no candidate-level proof exists, keep source/code readiness blocked and propose the next deferred hypothesis.

## Validation commands

- `python -m pytest tests/reverse/test_re352_frontend_display_menu_service_readiness_gate.py -q`
- `python scripts/reverse/re352_frontend_display_menu_service_readiness_gate.py --repo .`
- `python -m pytest tests/reverse -q`
