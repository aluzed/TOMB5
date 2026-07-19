# RE-391 post maths-render next Ghidra cluster selection

## Goal

After RE-390 exhausted the maths/render matrix-transform-core queue, select the next deferred parent Ghidra bridge cluster autonomously instead of stopping at an exhausted topic.

## Inputs

- Exhaustion handoff: `docs/reverse/generated/re390-matrix-transform-core-readiness-gate-handoff.csv`
- Parent Ghidra bridge cluster queue: `docs/reverse/generated/re388-post-effects-lighting-next-ghidra-cluster-selection-clusters.csv`
- Parent Ghidra bridge candidate gate: `docs/reverse/generated/re310-ghidra-bridge-candidate-readiness-gate-candidates.csv`

## Progress tracker

- [x] RE-390 maths/render exhaustion validated.
- [x] RE-388 parent Ghidra bridge cluster queue re-opened.
- [x] Prior collision/switch/door, platform/frontend, effects/lighting, and maths/render clusters marked closed.
- [x] Next deferred cluster selected in parent order.
- [x] Source/domain readiness kept blocked pending a narrow export.

## Generated artifacts

- `docs/reverse/generated/re391-post-maths-render-next-ghidra-cluster-selection-clusters.csv`
- `docs/reverse/generated/re391-post-maths-render-next-ghidra-cluster-selection-candidates.csv`
- `docs/reverse/generated/re391-post-maths-render-next-ghidra-cluster-selection-summary.csv`
- `docs/reverse/generated/re391-post-maths-render-next-ghidra-cluster-selection-handoff.csv`
- `docs/reverse/functions/re391-post-maths-render-next-ghidra-cluster-selection.md`

## Findings

- Parent scope: `ghidra-bridge-candidate-clusters`
- Closed clusters: `collision-switch-door-cluster;platform-frontend-service-cluster;effects-lighting-cluster;maths-render-cluster`
- Deferred clusters: `3`
- Selected follow-up cluster: `lara-combat-camera-cluster`
- Selected candidate count: `2`
- Ready to reopen domain selection: `0`
- Source patch authorized rows: `0`

## Readiness decision

The next safe hypothesis is `lara-combat-camera-cluster`, but it remains source-symbolic. Domain and pivot stay `none` / `none`, and code readiness remains `blocked` until a narrow export and gate establish candidate-level proof.

## Follow-up ticket breakdown

- `RE-392` / `ghidra-lara-combat-camera-cluster-narrow-export`: generate a metadata-only narrow source-symbolic export for `lara-combat-camera-cluster`.
  - Inputs: RE-391 selected candidates and the local repo maps.
  - Deliverables: cluster-specific narrowed candidates, summary/handoff, and readiness-preserving story.
  - Stop condition: if the export still lacks candidate-level proof, keep source/code readiness blocked and hand off to a readiness gate.

## Validation commands

- `python -m pytest tests/reverse/test_re391_post_maths_render_next_ghidra_cluster_selection.py -q`
- `python scripts/reverse/re391_post_maths_render_next_ghidra_cluster_selection.py --repo .`
- `python -m pytest tests/reverse -q`
