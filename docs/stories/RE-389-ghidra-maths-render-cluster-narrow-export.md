# RE-389 Ghidra maths/render cluster narrow export

## Goal

Produce a metadata-only narrow export for the RE-388 maths/render Ghidra bridge cluster and select the next readiness-gate subcluster.

## Inputs

- Upstream handoff: `docs/reverse/generated/re388-post-effects-lighting-next-ghidra-cluster-selection-handoff.csv`
- Selected candidates: `docs/reverse/generated/re388-post-effects-lighting-next-ghidra-cluster-selection-candidates.csv`

## Progress tracker

- [x] RE-388 maths/render cluster selection validated.
- [x] Maths/render candidate rows grouped into narrow service subclusters.
- [x] Matrix transform core selected for the next readiness gate.
- [x] Domain and pivot selection kept blocked.
- [x] Source/code patch authorization denied.

## Generated artifacts

- `docs/reverse/generated/re389-ghidra-maths-render-cluster-narrow-subclusters.csv`
- `docs/reverse/generated/re389-ghidra-maths-render-cluster-narrow-candidates.csv`
- `docs/reverse/generated/re389-ghidra-maths-render-cluster-narrow-summary.csv`
- `docs/reverse/generated/re389-ghidra-maths-render-cluster-narrow-handoff.csv`
- `docs/reverse/functions/re389-ghidra-maths-render-cluster-narrow-export.md`

## Findings

- Focus cluster: `maths-render-cluster`
- Focus candidate count: `3`
- Narrow subcluster count: `1`
- Selected narrow subcluster: `matrix-transform-core`
- Selected candidate count: `3`
- Ready to reopen domain selection: `0`
- Source patch authorized rows: `0`

## Readiness decision

The selected service subcluster is source-symbolic only. Domain and pivot stay `none` / `none`, and code readiness remains `blocked` pending candidate-level proof.

## Follow-up ticket breakdown

- `RE-390` / `matrix-transform-core-readiness-gate`: gate `matrix-transform-core` and decide whether any candidate can reopen a proof domain.
  - Inputs: RE-389 narrowed subcluster/candidate CSVs.
  - Deliverables: candidate-level readiness rows, summary/handoff, story.
  - Stop condition: if every row lacks candidate-level proof, keep source/code readiness blocked and continue to the next deferred bridge cluster.

## Validation commands

- `python -m pytest tests/reverse/test_re389_ghidra_maths_render_cluster_narrow_export.py -q`
- `python scripts/reverse/re389_ghidra_maths_render_cluster_narrow_export.py --repo .`
- `python -m pytest tests/reverse -q`
