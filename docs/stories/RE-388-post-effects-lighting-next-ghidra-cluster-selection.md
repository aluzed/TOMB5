# RE-388 post effects-lighting next Ghidra cluster selection

## Goal

After RE-387 exhausted the effects/lighting service subcluster queue, select the next deferred parent Ghidra bridge cluster autonomously instead of stopping at an exhausted topic.

## Inputs

- Exhaustion handoff: `docs/reverse/generated/re387-spotcam-projectile-effect-service-callsite-readiness-handoff.csv`
- Parent Ghidra bridge cluster queue: `docs/reverse/generated/re369-post-platform-frontend-next-ghidra-cluster-selection-clusters.csv`
- Parent Ghidra bridge candidate gate: `docs/reverse/generated/re310-ghidra-bridge-candidate-readiness-gate-candidates.csv`

## Progress tracker

- [x] RE-387 effects/lighting cluster exhaustion validated.
- [x] RE-369 parent Ghidra bridge cluster queue re-opened.
- [x] Collision/switch/door, platform/frontend, and effects/lighting clusters marked closed.
- [x] Next deferred cluster selected in parent order.
- [x] Source/domain readiness kept blocked pending a narrow export.

## Generated artifacts

- `docs/reverse/generated/re388-post-effects-lighting-next-ghidra-cluster-selection-clusters.csv`
- `docs/reverse/generated/re388-post-effects-lighting-next-ghidra-cluster-selection-candidates.csv`
- `docs/reverse/generated/re388-post-effects-lighting-next-ghidra-cluster-selection-summary.csv`
- `docs/reverse/generated/re388-post-effects-lighting-next-ghidra-cluster-selection-handoff.csv`
- `docs/reverse/functions/re388-post-effects-lighting-next-ghidra-cluster-selection.md`

## Findings

- Parent scope: `ghidra-bridge-candidate-clusters`
- Closed clusters: `collision-switch-door-cluster;platform-frontend-service-cluster;effects-lighting-cluster`
- Deferred clusters: `4`
- Selected follow-up cluster: `maths-render-cluster`
- Selected candidate count: `3`
- Ready to reopen domain selection: `0`
- Source patch authorized rows: `0`

## Readiness decision

The next safe hypothesis is `maths-render-cluster`, but it remains source-symbolic. Domain and pivot stay `none` / `none`, and code readiness remains `blocked` until a narrow export and gate establish candidate-level proof.

## Follow-up ticket breakdown

- `RE-389` / `ghidra-maths-render-cluster-narrow-export`: generate a metadata-only narrow source-symbolic export for `maths-render-cluster`.
  - Inputs: RE-388 selected candidates and the local Ghidra/repo maps.
  - Deliverables: cluster-specific narrowed candidates, summary/handoff, and readiness-preserving story.
  - Stop condition: if the export still lacks candidate-level proof, keep source/code readiness blocked and hand off to a readiness gate.

## Validation commands

- `python -m pytest tests/reverse/test_re388_post_effects_lighting_next_ghidra_cluster_selection.py -q`
- `python scripts/reverse/re388_post_effects_lighting_next_ghidra_cluster_selection.py --repo .`
- `python -m pytest tests/reverse -q`
