# RE-370 Ghidra effects/lighting narrow export

## Purpose

Narrow the RE-369 selected `effects-lighting-cluster` source-symbolic cluster into deterministic subclusters without exposing raw Ghidra identity.

## Inputs

- Upstream handoff: `docs/reverse/generated/re369-post-platform-frontend-next-ghidra-cluster-selection-handoff.csv`
- Selected candidates: `docs/reverse/generated/re369-post-platform-frontend-next-ghidra-cluster-selection-candidates.csv`

## Selection

Selected `dynamic-lighting-service` with `2` candidates.

## Counts

- Focus candidates: `4`
- Narrow subclusters: `3`
- Ready to reopen domain: `0`
- Source patch authorized: `0`

## Readiness

Domain and pivot remain `none` / `none`. Code readiness remains `blocked` until `dynamic-lighting-service` passes a candidate-level readiness gate.

## Handoff

- Next ticket: `RE-371`
- Next topic: `dynamic-lighting-service-readiness-gate`
- Stop condition: `effects/lighting cluster narrowed; gate selected dynamic lighting service before proof-domain selection`
