# RE-375 dynamic-lighting service next-candidate proof export

## Summary

Exported `21` source-symbolic context rows for next candidate `3a208e2bf745` after previous candidate `f5d0099b5511` stayed blocked.
No proof-domain is reopened by this export; the next candidate hash still lacks direct source-backed proof.

## Proof gate

- candidate `3a208e2bf745`: contexts `21`, direct repo symbols `0`, gate `blocked-unmapped-next-candidate-identity`, next `dynamic-lighting-service-next-candidate-callsite-map`

## Context families

- `dynamic-lighting-control`: `5` rows
- `effect-emitter-runtime`: `3` rows
- `flame-emitter`: `3` rows
- `geometry-collision-runtime`: `2` rows
- `moving-trap-runtime`: `4` rows
- `trap-door-switch-runtime`: `4` rows

## Readiness decision

The export is metadata-ready, but source/domain readiness remains blocked until a source-backed next-candidate callsite map can prove candidate-level behavior without raw binary evidence.
