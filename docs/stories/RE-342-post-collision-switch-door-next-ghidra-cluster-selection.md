# RE-342 post collision-switch-door next Ghidra cluster selection

## Goal

After RE-341 exhausted the final collision/switch/door subcluster, select the next deferred parent Ghidra bridge cluster autonomously instead of stopping at an exhausted topic.

## Inputs

- Exhaustion handoff: `docs/reverse/generated/re341-camera-collision-helper-callsite-readiness-handoff.csv`
- Parent Ghidra bridge cluster gate: `docs/reverse/generated/re310-ghidra-bridge-candidate-readiness-gate-clusters.csv`
- Parent Ghidra bridge candidate gate: `docs/reverse/generated/re310-ghidra-bridge-candidate-readiness-gate-candidates.csv`

## Progress tracker

- [x] RE-341 camera-collision exhaustion validated.
- [x] RE-310 parent Ghidra bridge cluster queue re-opened.
- [x] Collision/switch/door cluster marked closed.
- [x] Next deferred cluster selected in parent order.
- [x] Source/domain readiness kept blocked pending a narrow export.

## Generated artifacts

- `docs/reverse/generated/re342-post-collision-switch-door-next-ghidra-cluster-selection-clusters.csv`
- `docs/reverse/generated/re342-post-collision-switch-door-next-ghidra-cluster-selection-candidates.csv`
- `docs/reverse/generated/re342-post-collision-switch-door-next-ghidra-cluster-selection-summary.csv`
- `docs/reverse/generated/re342-post-collision-switch-door-next-ghidra-cluster-selection-handoff.csv`
- `docs/reverse/functions/re342-post-collision-switch-door-next-ghidra-cluster-selection.md`

## Findings

- Parent scope: `ghidra-bridge-candidate-clusters`
- Closed clusters: `collision-switch-door-cluster`
- Deferred clusters: `6`
- Selected follow-up cluster: `platform-frontend-service-cluster`
- Selected candidate count: `6`
- Ready to reopen domain selection: `0`
- Source patch authorized rows: `0`

## Readiness decision

The next safe hypothesis is `platform-frontend-service-cluster`, but it remains source-symbolic. Domain and pivot stay `none` / `none`, and code readiness remains `blocked` until a narrow export and gate establish candidate-level proof.

## Follow-up ticket breakdown

- `RE-343` / `ghidra-platform-frontend-service-cluster-narrow-export`: generate a metadata-only narrow source-symbolic export for `platform-frontend-service-cluster`.
  - Inputs: RE-342 selected candidates and the local Ghidra/repo maps.
  - Deliverables: cluster-specific narrowed candidates, summary/handoff, and readiness-preserving story.
  - Stop condition: if the export still lacks candidate-level proof, keep source/code readiness blocked and hand off to a readiness gate.

## Validation commands

- `python -m pytest tests/reverse/test_re342_post_collision_switch_door_next_ghidra_cluster_selection.py -q`
- `python scripts/reverse/re342_post_collision_switch_door_next_ghidra_cluster_selection.py --repo .`
- `python -m pytest tests/reverse -q`
