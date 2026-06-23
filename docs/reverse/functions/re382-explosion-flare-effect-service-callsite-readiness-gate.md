# RE-382 explosion/flare effect service callsite readiness gate

## Summary

Gated `7` source-backed callsite families for explosion/flare candidate `87d9c8a62335`.
No explosion/flare callsite family proves candidate-level behavior, so the proof domain and pivot remain `none`.

## Family gates

- `control-flow-helper`: `38` rows, gate `blocked-no-candidate-level-proof`.
- `explosion-flare-effect-helper`: `23` rows, gate `blocked-no-candidate-level-proof`.
- `joint-position-helper`: `21` rows, gate `blocked-no-candidate-level-proof`.
- `audio-camera-helper`: `17` rows, gate `blocked-no-candidate-level-proof`.
- `runtime-effect-support`: `8` rows, gate `blocked-no-candidate-level-proof`.
- `room-floor-helper`: `8` rows, gate `blocked-no-candidate-level-proof`.
- `stub-marker`: `6` rows, gate `blocked-stub-only-family`.

## Readiness decision

- candidate-level proof rows: `0`
- ready-to-reopen rows: `0`
- source-patch authorized rows: `0`
- next deferred candidate: `none`
- next subcluster: `spotcam-projectile-effect-service`
- next ticket: `RE-383` / `effects-lighting-cluster-post-explosion-flare-next-subcluster-selection`

Code readiness remains `blocked`.
