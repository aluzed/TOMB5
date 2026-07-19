# RE-391 post maths-render next Ghidra cluster selection

## Purpose

Close the exhausted maths/render bridge-cluster path from RE-390 and select the next deferred Ghidra bridge cluster without authorizing a proof domain or source patch.

## Inputs

- Exhaustion handoff: `docs/reverse/generated/re390-matrix-transform-core-readiness-gate-handoff.csv`
- Parent cluster queue: `docs/reverse/generated/re388-post-effects-lighting-next-ghidra-cluster-selection-clusters.csv`
- Parent candidates: `docs/reverse/generated/re310-ghidra-bridge-candidate-readiness-gate-candidates.csv`

## Selection

Selected `lara-combat-camera-cluster` with `2` source-symbolic candidates.

## Counts

- Input clusters: `4`
- Closed clusters: `4`
- Deferred clusters: `3`
- Selected mapped caller total: `29`
- Selected mapped callee total: `6`
- Ready to reopen domain: `0`
- Source patch authorized: `0`

## Readiness

Domain and pivot remain `none` / `none`. Code readiness remains `blocked` because the selected cluster still needs a narrow source-symbolic export before any proof-domain selection.

## Handoff

- Next ticket: `RE-392`
- Next topic: `ghidra-lara-combat-camera-cluster-narrow-export`
- Stop condition: `maths/render cluster exhausted; select next deferred Ghidra bridge cluster for a narrow export`

Code readiness remains `blocked`.
