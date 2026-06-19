# RE-342 post collision-switch-door next Ghidra cluster selection

## Purpose

Close the exhausted collision/switch/door bridge-cluster path from RE-341 and select the next deferred Ghidra bridge cluster without authorizing a proof domain or source patch.

## Inputs

- Exhaustion handoff: `docs/reverse/generated/re341-camera-collision-helper-callsite-readiness-handoff.csv`
- Parent cluster gate: `docs/reverse/generated/re310-ghidra-bridge-candidate-readiness-gate-clusters.csv`
- Parent candidates: `docs/reverse/generated/re310-ghidra-bridge-candidate-readiness-gate-candidates.csv`

## Selection

Selected `platform-frontend-service-cluster` with `6` source-symbolic candidates.

## Counts

- Input clusters: `7`
- Closed clusters: `1`
- Deferred clusters: `6`
- Selected mapped caller total: `109`
- Selected mapped callee total: `13`
- Ready to reopen domain: `0`
- Source patch authorized: `0`

## Readiness

Domain and pivot remain `none` / `none`. Code readiness remains `blocked` because the selected cluster still needs a narrow source-symbolic export before any proof-domain selection.

## Handoff

- Next ticket: `RE-343`
- Next topic: `ghidra-platform-frontend-service-cluster-narrow-export`
- Stop condition: `collision-switch-door cluster exhausted; select next deferred Ghidra bridge cluster for a narrow export`
