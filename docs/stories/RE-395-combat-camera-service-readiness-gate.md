# RE-395 combat camera service readiness gate

## Goal

Gate the RE-394 combat-camera-service candidate and decide whether it can reopen proof-domain selection or authorize a source patch.

## Inputs

- Upstream handoff: `docs/reverse/generated/re394-lara-combat-camera-post-lara-control-next-subcluster-selection-handoff.csv`
- Candidate rows: `docs/reverse/generated/re394-lara-combat-camera-post-lara-control-next-subcluster-selection-candidates.csv`

## Progress tracker

- [x] RE-394 combat-camera handoff validated.
- [x] Selected candidate checked for drift.
- [x] Candidate-level proof requirement evaluated.
- [x] Domain/source-patch authorization denied.
- [x] Still-narrower proof export handoff emitted.

## Generated artifacts

- `docs/reverse/generated/re395-combat-camera-service-readiness-gate-candidates.csv`
- `docs/reverse/generated/re395-combat-camera-service-readiness-gate-gates.csv`
- `docs/reverse/generated/re395-combat-camera-service-readiness-gate-summary.csv`
- `docs/reverse/generated/re395-combat-camera-service-readiness-gate-handoff.csv`
- `docs/reverse/functions/re395-combat-camera-service-readiness-gate.md`

## Readiness decision

The `combat-camera-service` candidate remains source-symbolic. Domain and pivot stay `none` / `none`, and code readiness remains `blocked`.

## Follow-up ticket breakdown

- `RE-396` / `combat-camera-service-candidate-proof-export`: export still-narrower candidate proof context for `0aaa76206517`.
  - Stop condition: without candidate-level proof, source/code readiness stays blocked.

## Validation commands

- `python -m pytest tests/reverse/test_re395_combat_camera_service_readiness_gate.py -q`
- `python scripts/reverse/re395_combat_camera_service_readiness_gate.py --repo .`
- `python -m pytest tests/reverse -q`
