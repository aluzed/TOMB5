# RE-392 Ghidra lara/combat/camera cluster narrow export

## Goal

Produce a metadata-only narrow export for the RE-391 lara/combat/camera Ghidra bridge cluster and select the next readiness-gate subcluster.

## Inputs

- Upstream handoff: `docs/reverse/generated/re391-post-maths-render-next-ghidra-cluster-selection-handoff.csv`
- Selected candidates: `docs/reverse/generated/re391-post-maths-render-next-ghidra-cluster-selection-candidates.csv`

## Progress tracker

- [x] RE-391 lara/combat/camera cluster selection validated.
- [x] Lara/combat/camera candidate rows grouped into narrow service subclusters.
- [x] Lara control service selected for the next readiness gate.
- [x] Domain and pivot selection kept blocked.
- [x] Source/code patch authorization denied.

## Generated artifacts

- `docs/reverse/generated/re392-ghidra-lara-combat-camera-cluster-narrow-subclusters.csv`
- `docs/reverse/generated/re392-ghidra-lara-combat-camera-cluster-narrow-candidates.csv`
- `docs/reverse/generated/re392-ghidra-lara-combat-camera-cluster-narrow-summary.csv`
- `docs/reverse/generated/re392-ghidra-lara-combat-camera-cluster-narrow-handoff.csv`
- `docs/reverse/functions/re392-ghidra-lara-combat-camera-cluster-narrow-export.md`

## Findings

- Focus cluster: `lara-combat-camera-cluster`
- Focus candidate count: `2`
- Narrow subcluster count: `2`
- Selected narrow subcluster: `lara-control-service`
- Selected candidate count: `1`
- Ready to reopen domain selection: `0`
- Source patch authorized rows: `0`

## Readiness decision

The selected service subcluster is source-symbolic only. Domain and pivot stay `none` / `none`, and code readiness remains `blocked` pending candidate-level proof.

## Follow-up ticket breakdown

- `RE-393` / `lara-control-service-readiness-gate`: gate `lara-control-service` and decide whether any candidate can reopen a proof domain.
  - Inputs: RE-392 narrowed subcluster/candidate CSVs.
  - Deliverables: candidate-level readiness rows, summary/handoff, story.
  - Stop condition: if every row lacks candidate-level proof, keep source/code readiness blocked and continue to the next deferred bridge cluster.

## Validation commands

- `python -m pytest tests/reverse/test_re392_ghidra_lara_combat_camera_cluster_narrow_export.py -q`
- `python scripts/reverse/re392_ghidra_lara_combat_camera_cluster_narrow_export.py --repo .`
- `python -m pytest tests/reverse -q`
