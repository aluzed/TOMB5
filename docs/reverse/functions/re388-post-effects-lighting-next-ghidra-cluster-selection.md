# RE-388 post effects-lighting next Ghidra cluster selection

## Purpose

Close the exhausted effects/lighting bridge-cluster path from RE-387 and select the next deferred Ghidra bridge cluster without authorizing a proof domain or source patch.

## Inputs

- Exhaustion handoff: `docs/reverse/generated/re387-spotcam-projectile-effect-service-callsite-readiness-handoff.csv`
- Parent cluster queue: `docs/reverse/generated/re369-post-platform-frontend-next-ghidra-cluster-selection-clusters.csv`
- Parent candidates: `docs/reverse/generated/re310-ghidra-bridge-candidate-readiness-gate-candidates.csv`

## Selection

Selected `maths-render-cluster` with `3` source-symbolic candidates.

## Counts

- Input clusters: `5`
- Closed clusters: `3`
- Deferred clusters: `4`
- Selected mapped caller total: `5`
- Selected mapped callee total: `30`
- Ready to reopen domain: `0`
- Source patch authorized: `0`

## Readiness

Domain and pivot remain `none` / `none`. Code readiness remains `blocked` because the selected cluster still needs a narrow source-symbolic export before any proof-domain selection.

## Handoff

- Next ticket: `RE-389`
- Next topic: `ghidra-maths-render-cluster-narrow-export`
- Stop condition: `effects/lighting cluster exhausted; select next deferred Ghidra bridge cluster for a narrow export`

Code readiness remains `blocked`.
