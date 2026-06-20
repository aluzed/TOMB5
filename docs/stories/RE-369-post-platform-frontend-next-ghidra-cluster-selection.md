# RE-369 post platform-frontend next Ghidra cluster selection

## Goal

After RE-368 exhausted the final platform/frontend service subcluster, select the next deferred parent Ghidra bridge cluster autonomously instead of stopping at an exhausted topic.

## Inputs

- Exhaustion handoff: `docs/reverse/generated/re368-runtime-callee-bridge-callsite-readiness-handoff.csv`
- Parent Ghidra bridge cluster gate: `docs/reverse/generated/re310-ghidra-bridge-candidate-readiness-gate-clusters.csv`
- Parent Ghidra bridge candidate gate: `docs/reverse/generated/re310-ghidra-bridge-candidate-readiness-gate-candidates.csv`

## Progress tracker

- [x] RE-368 platform/frontend service exhaustion validated.
- [x] RE-310 parent Ghidra bridge cluster queue re-opened.
- [x] Collision/switch/door and platform/frontend service clusters marked closed.
- [x] Next deferred cluster selected in parent order.
- [x] Source/domain readiness kept blocked pending a narrow export.

## Generated artifacts

- `docs/reverse/generated/re369-post-platform-frontend-next-ghidra-cluster-selection-clusters.csv`
- `docs/reverse/generated/re369-post-platform-frontend-next-ghidra-cluster-selection-candidates.csv`
- `docs/reverse/generated/re369-post-platform-frontend-next-ghidra-cluster-selection-summary.csv`
- `docs/reverse/generated/re369-post-platform-frontend-next-ghidra-cluster-selection-handoff.csv`
- `docs/reverse/functions/re369-post-platform-frontend-next-ghidra-cluster-selection.md`

## Findings

- Parent scope: `ghidra-bridge-candidate-clusters`
- Closed clusters: `collision-switch-door-cluster;platform-frontend-service-cluster`
- Deferred clusters: `5`
- Selected follow-up cluster: `effects-lighting-cluster`
- Selected candidate count: `4`
- Ready to reopen domain selection: `0`
- Source patch authorized rows: `0`

## Readiness decision

The next safe hypothesis is `effects-lighting-cluster`, but it remains source-symbolic. Domain and pivot stay `none` / `none`, and code readiness remains `blocked` until a narrow export and gate establish candidate-level proof.

## Follow-up ticket breakdown

- `RE-370` / `ghidra-effects-lighting-cluster-narrow-export`: generate a metadata-only narrow source-symbolic export for `effects-lighting-cluster`.
  - Inputs: RE-369 selected candidates and the local Ghidra/repo maps.
  - Deliverables: cluster-specific narrowed candidates, summary/handoff, and readiness-preserving story.
  - Stop condition: if the export still lacks candidate-level proof, keep source/code readiness blocked and hand off to a readiness gate.

## Validation commands

- `python -m pytest tests/reverse/test_re369_post_platform_frontend_next_ghidra_cluster_selection.py -q`
- `python scripts/reverse/re369_post_platform_frontend_next_ghidra_cluster_selection.py --repo .`
- `python -m pytest tests/reverse -q`
