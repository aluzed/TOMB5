# RE-343 Ghidra platform/frontend service narrow export

## Goal

Produce a metadata-only narrow export for the RE-342 platform/frontend Ghidra bridge cluster and select the next readiness-gate subcluster.

## Inputs

- Upstream handoff: `docs/reverse/generated/re342-post-collision-switch-door-next-ghidra-cluster-selection-handoff.csv`
- Selected candidates: `docs/reverse/generated/re342-post-collision-switch-door-next-ghidra-cluster-selection-candidates.csv`

## Progress tracker

- [x] RE-342 platform/frontend cluster selection validated.
- [x] Platform/frontend candidate rows grouped into narrow service subclusters.
- [x] CD/load/audio service selected for the next readiness gate.
- [x] Domain and pivot selection kept blocked.
- [x] Source/code patch authorization denied.

## Generated artifacts

- `docs/reverse/generated/re343-ghidra-platform-frontend-service-narrow-subclusters.csv`
- `docs/reverse/generated/re343-ghidra-platform-frontend-service-narrow-candidates.csv`
- `docs/reverse/generated/re343-ghidra-platform-frontend-service-narrow-summary.csv`
- `docs/reverse/generated/re343-ghidra-platform-frontend-service-narrow-handoff.csv`
- `docs/reverse/functions/re343-ghidra-platform-frontend-service-narrow-export.md`

## Findings

- Focus cluster: `platform-frontend-service-cluster`
- Focus candidate count: `6`
- Narrow subcluster count: `4`
- Selected narrow subcluster: `cd-load-audio-service`
- Selected candidate count: `2`
- Ready to reopen domain selection: `0`
- Source patch authorized rows: `0`

## Readiness decision

The selected service subcluster is source-symbolic only. Domain and pivot stay `none` / `none`, and code readiness remains `blocked` pending candidate-level proof.

## Follow-up ticket breakdown

- `RE-344` / `cd-load-audio-service-readiness-gate`: gate `cd-load-audio-service` and decide whether any candidate can reopen a proof domain.
  - Inputs: RE-343 narrowed subcluster/candidate CSVs.
  - Deliverables: candidate-level readiness rows, summary/handoff, story.
  - Stop condition: if every row lacks candidate-level proof, keep source/code readiness blocked and continue to the next deferred service subcluster.

## Validation commands

- `python -m pytest tests/reverse/test_re343_ghidra_platform_frontend_service_narrow_export.py -q`
- `python scripts/reverse/re343_ghidra_platform_frontend_service_narrow_export.py --repo .`
- `python -m pytest tests/reverse -q`
