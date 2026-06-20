# RE-369 post platform-frontend next Ghidra cluster selection

## Purpose

Close the exhausted platform/frontend bridge-cluster path from RE-368 and select the next deferred Ghidra bridge cluster without authorizing a proof domain or source patch.

## Inputs

- Exhaustion handoff: `docs/reverse/generated/re368-runtime-callee-bridge-callsite-readiness-handoff.csv`
- Parent cluster gate: `docs/reverse/generated/re310-ghidra-bridge-candidate-readiness-gate-clusters.csv`
- Parent candidates: `docs/reverse/generated/re310-ghidra-bridge-candidate-readiness-gate-candidates.csv`

## Selection

Selected `effects-lighting-cluster` with `4` source-symbolic candidates.

## Counts

- Input clusters: `7`
- Closed clusters: `2`
- Deferred clusters: `5`
- Selected mapped caller total: `114`
- Selected mapped callee total: `0`
- Ready to reopen domain: `0`
- Source patch authorized: `0`

## Readiness

Domain and pivot remain `none` / `none`. Code readiness remains `blocked` because the selected cluster still needs a narrow source-symbolic export before any proof-domain selection.

## Handoff

- Next ticket: `RE-370`
- Next topic: `ghidra-effects-lighting-cluster-narrow-export`
- Stop condition: `platform/frontend service cluster exhausted; select next deferred Ghidra bridge cluster for a narrow export`

Code readiness remains `blocked`.
