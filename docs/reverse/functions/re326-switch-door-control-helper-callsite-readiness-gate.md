# RE-326 switch-door-control helper callsite readiness gate

## Summary

Gated `5` source-backed callsite families for candidate `8d1fc6fc3cfc`.
No switch-door-control callsite family proves candidate-level behavior, so the proof domain and pivot remain `none`.

## Family gates

- `door-helper`: `14` rows, gate `blocked-no-candidate-level-proof`.
- `animation-helper`: `7` rows, gate `blocked-no-candidate-level-proof`.
- `trigger-helper`: `2` rows, gate `blocked-no-candidate-level-proof`.
- `effect-helper`: `3` rows, gate `blocked-no-candidate-level-proof`.
- `stub-marker`: `13` rows, gate `blocked-stub-only-family`.

## Readiness decision

- candidate-level proof rows: `0`
- ready-to-reopen rows: `0`
- source-patch authorized rows: `0`
- next candidate: `none`
- next ticket: `TBD` / `switch-door-control-helper-candidate-queue-exhausted`

Code readiness remains `blocked`.
