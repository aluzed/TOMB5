# RE-389 Ghidra maths/render cluster narrow export

## Purpose

Narrow the RE-388 selected `maths-render-cluster` source-symbolic cluster into deterministic subclusters without exposing raw Ghidra identity.

## Inputs

- Upstream handoff: `docs/reverse/generated/re388-post-effects-lighting-next-ghidra-cluster-selection-handoff.csv`
- Selected candidates: `docs/reverse/generated/re388-post-effects-lighting-next-ghidra-cluster-selection-candidates.csv`

## Selection

Selected `matrix-transform-core` with `3` candidates.

## Counts

- Focus candidates: `3`
- Narrow subclusters: `1`
- Ready to reopen domain: `0`
- Source patch authorized: `0`

## Readiness

Domain and pivot remain `none` / `none`. Code readiness remains `blocked` until `matrix-transform-core` passes a candidate-level readiness gate.

## Handoff

- Next ticket: `RE-390`
- Next topic: `matrix-transform-core-readiness-gate`
- Stop condition: `maths/render cluster narrowed; gate selected matrix transform core before proof-domain selection`
