# RE-384 spotcam/projectile effect service readiness gate

## Goal

Gate the RE-383 `spotcam-projectile-effect-service` candidate and decide whether it can reopen proof-domain selection or authorize a source patch.

## Inputs

- Upstream handoff: `docs/reverse/generated/re383-effects-lighting-cluster-post-explosion-flare-next-subcluster-selection-handoff.csv`
- Candidate rows: `docs/reverse/generated/re383-effects-lighting-cluster-post-explosion-flare-next-subcluster-selection-candidates.csv`
- Source-context baseline: `docs/reverse/generated/re370-ghidra-effects-lighting-narrow-candidates.csv`

## Progress tracker

- [x] RE-383 spotcam/projectile effect service handoff validated.
- [x] Selected candidate checked for drift.
- [x] Candidate-level proof requirement evaluated.
- [x] Domain/source-patch authorization denied.
- [x] Still-narrower proof export handoff emitted.

## Generated artifacts

- `docs/reverse/generated/re384-spotcam-projectile-effect-service-readiness-gate-candidates.csv`
- `docs/reverse/generated/re384-spotcam-projectile-effect-service-readiness-gate-gates.csv`
- `docs/reverse/generated/re384-spotcam-projectile-effect-service-readiness-gate-summary.csv`
- `docs/reverse/generated/re384-spotcam-projectile-effect-service-readiness-gate-handoff.csv`
- `docs/reverse/functions/re384-spotcam-projectile-effect-service-readiness-gate.md`

## Findings

- Selected narrow subcluster: `spotcam-projectile-effect-service`
- Input candidates: `1`
- Gate rows: `1`
- Ready to reopen domain selection: `0`
- Source patch authorized rows: `0`

## Readiness decision

The `spotcam-projectile-effect-service` row remains source-symbolic. Domain and pivot stay `none` / `none`, and code readiness remains `blocked`.

## Follow-up ticket breakdown

- `RE-385` / `spotcam-projectile-effect-service-candidate-proof-export`: export still-narrower candidate proof context for `b6d128932004`.
  - Inputs: RE-384 candidate/gate CSVs plus RE-370 context.
  - Deliverables: metadata-only proof export, summary/handoff, story.
  - Stop condition: if no candidate-level proof exists, keep source/code readiness blocked and propose the next deferred hypothesis.

## Validation commands

- `python -m pytest tests/reverse/test_re384_spotcam_projectile_effect_service_readiness_gate.py -q`
- `python scripts/reverse/re384_spotcam_projectile_effect_service_readiness_gate.py --repo .`
- `python -m pytest tests/reverse -q`
