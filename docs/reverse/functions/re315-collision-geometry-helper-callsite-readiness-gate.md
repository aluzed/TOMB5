# RE-315 collision geometry helper callsite readiness gate

## Summary

Gated `4` source-backed callsite families for candidate `5e99f39fd8ef`.
No callsite family proves candidate-level behavior, so the proof domain and pivot remain `none`.

## Family gates

- `collision-helper`: `8` rows, gate `blocked-no-candidate-level-proof`.
- `position-test`: `8` rows, gate `blocked-no-candidate-level-proof`.
- `trigger-helper`: `5` rows, gate `blocked-no-candidate-level-proof`.
- `stub-marker`: `16` rows, gate `blocked-stub-only-family`.

## Readiness decision

- candidate-level proof rows: `0`
- ready-to-reopen rows: `0`
- source-patch authorized rows: `0`
- next candidate: `d96359c1d9f3`
- next ticket: `RE-316` / `collision-geometry-helper-next-candidate-proof-export`

Code readiness remains `blocked`.
