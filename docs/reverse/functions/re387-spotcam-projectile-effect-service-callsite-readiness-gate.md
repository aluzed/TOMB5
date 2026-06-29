# RE-387 spotcam/projectile effect service callsite readiness gate

## Summary

Gated `8` source-backed callsite families for candidate `b6d128932004`.

No spotcam/projectile callsite family proves candidate-level behavior. Source-backed family volume remains prioritization evidence only, so domain reopen and source patch authorization stay denied.

## Family gates

- `spotcam-projectile-helper`: `204` rows, gate `blocked-no-candidate-level-proof`.
- `ambient-combat-effect-helper`: `32` rows, gate `blocked-no-candidate-level-proof`.
- `room-floor-helper`: `16` rows, gate `blocked-no-candidate-level-proof`.
- `runtime-effect-support`: `16` rows, gate `blocked-no-candidate-level-proof`.
- `conversation-helper`: `6` rows, gate `blocked-no-candidate-level-proof`.
- `audio-camera-helper`: `2` rows, gate `blocked-no-candidate-level-proof`.
- `trap-effect-helper`: `1` rows, gate `blocked-no-candidate-level-proof`.
- `stub-marker`: `19` rows, gate `blocked-stub-only-family`.

## Decision

- Decision: `deny-domain-reopen-and-exhaust-effects-lighting-queue`
- Next ticket: `TBD`
- Next topic: `effects-lighting-cluster-subcluster-queue-exhausted`
- Code readiness: `blocked`
