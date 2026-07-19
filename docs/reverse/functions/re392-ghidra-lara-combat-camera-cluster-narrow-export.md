# RE-392 Ghidra lara/combat/camera cluster narrow export

## Purpose

Narrow the RE-391 selected `lara-combat-camera-cluster` source-symbolic cluster into deterministic subclusters without exposing raw Ghidra identity.

## Inputs

- Upstream handoff: `docs/reverse/generated/re391-post-maths-render-next-ghidra-cluster-selection-handoff.csv`
- Selected candidates: `docs/reverse/generated/re391-post-maths-render-next-ghidra-cluster-selection-candidates.csv`

## Selection

Selected `lara-control-service` with `1` candidates.

## Counts

- Focus candidates: `2`
- Narrow subclusters: `2`
- Ready to reopen domain: `0`
- Source patch authorized: `0`

## Readiness

Domain and pivot remain `none` / `none`. Code readiness remains `blocked` until `lara-control-service` passes a candidate-level readiness gate.

## Handoff

- Next ticket: `RE-393`
- Next topic: `lara-control-service-readiness-gate`
- Stop condition: `lara/combat/camera cluster narrowed; gate selected lara control service before proof-domain selection`
