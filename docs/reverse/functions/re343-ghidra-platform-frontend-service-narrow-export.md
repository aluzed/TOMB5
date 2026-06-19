# RE-343 Ghidra platform/frontend service narrow export

## Purpose

Narrow the RE-342 selected `platform-frontend-service-cluster` source-symbolic cluster into deterministic subclusters without exposing raw Ghidra identity.

## Inputs

- Upstream handoff: `docs/reverse/generated/re342-post-collision-switch-door-next-ghidra-cluster-selection-handoff.csv`
- Selected candidates: `docs/reverse/generated/re342-post-collision-switch-door-next-ghidra-cluster-selection-candidates.csv`

## Selection

Selected `cd-load-audio-service` with `2` candidates.

## Counts

- Focus candidates: `6`
- Narrow subclusters: `4`
- Ready to reopen domain: `0`
- Source patch authorized: `0`

## Readiness

Domain and pivot remain `none` / `none`. Code readiness remains `blocked` until `cd-load-audio-service` passes a candidate-level readiness gate.

## Handoff

- Next ticket: `RE-344`
- Next topic: `cd-load-audio-service-readiness-gate`
- Stop condition: `platform/frontend cluster narrowed; gate selected cd/load/audio service before proof-domain selection`
