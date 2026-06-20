# RE-370 Ghidra effects/lighting narrow export

## Goal

Produce a metadata-only narrow export for the RE-369 effects/lighting Ghidra bridge cluster and select the next readiness-gate subcluster.

## Inputs

- Upstream handoff: `docs/reverse/generated/re369-post-platform-frontend-next-ghidra-cluster-selection-handoff.csv`
- Selected candidates: `docs/reverse/generated/re369-post-platform-frontend-next-ghidra-cluster-selection-candidates.csv`

## Progress tracker

- [x] RE-369 effects/lighting cluster selection validated.
- [x] Effects/lighting candidate rows grouped into narrow service subclusters.
- [x] Dynamic lighting service selected for the next readiness gate.
- [x] Domain and pivot selection kept blocked.
- [x] Source/code patch authorization denied.

## Generated artifacts

- `docs/reverse/generated/re370-ghidra-effects-lighting-narrow-subclusters.csv`
- `docs/reverse/generated/re370-ghidra-effects-lighting-narrow-candidates.csv`
- `docs/reverse/generated/re370-ghidra-effects-lighting-narrow-summary.csv`
- `docs/reverse/generated/re370-ghidra-effects-lighting-narrow-handoff.csv`
- `docs/reverse/functions/re370-ghidra-effects-lighting-narrow-export.md`

## Findings

- Focus cluster: `effects-lighting-cluster`
- Focus candidate count: `4`
- Narrow subcluster count: `3`
- Selected narrow subcluster: `dynamic-lighting-service`
- Selected candidate count: `2`
- Ready to reopen domain selection: `0`
- Source patch authorized rows: `0`

## Readiness decision

The selected service subcluster is source-symbolic only. Domain and pivot stay `none` / `none`, and code readiness remains `blocked` pending candidate-level proof.

## Follow-up ticket breakdown

- `RE-371` / `dynamic-lighting-service-readiness-gate`: gate `dynamic-lighting-service` and decide whether any candidate can reopen a proof domain.
  - Inputs: RE-370 narrowed subcluster/candidate CSVs.
  - Deliverables: candidate-level readiness rows, summary/handoff, story.
  - Stop condition: if every row lacks candidate-level proof, keep source/code readiness blocked and continue to the next deferred service subcluster.

## Validation commands

- `python -m pytest tests/reverse/test_re370_ghidra_effects_lighting_narrow_export.py -q`
- `python scripts/reverse/re370_ghidra_effects_lighting_narrow_export.py --repo .`
- `python -m pytest tests/reverse -q`
