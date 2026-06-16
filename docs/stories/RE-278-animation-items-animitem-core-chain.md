# RE-278 — animation-items-animitem-core-chain

Status: Done

## Goal

Advance `animation-items-animitem-core-chain` for `animation-items` without source or marker changes.

## Progress tracker

- [x] Upstream metadata consumed.
- [x] Source-backed function/file/line metadata reviewed.
- [x] Metadata-only artifacts emitted.
- [x] Readiness and blockers recorded.

## Scope

- Scope: `CalcAnimatingItem_ASM, CalcAllAnimatingItems_ASM, DrawAllAnimatingItems_ASM, AnimateLara`
- Candidate count: `4`
- Artifact: `docs/reverse/generated/re276-animation-items-subclusters.csv`

## Readiness

- Readiness: `blocked`
- Source patch ready: `no`
- Marker ready: `no`
- Blocker: `missing-animation-item-state-contract-and-non-raw-equivalence-proof`

No production source or marker change is authorized by this story.
