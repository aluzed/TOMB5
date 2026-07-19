# RE-390 matrix transform core readiness gate

## Goal

Gate the RE-389 `matrix-transform-core` candidates and decide whether any can reopen proof-domain selection or authorize a source patch.

## Inputs

- Upstream handoff: `docs/reverse/generated/re389-ghidra-maths-render-cluster-narrow-handoff.csv`
- Candidate rows: `docs/reverse/generated/re389-ghidra-maths-render-cluster-narrow-candidates.csv`

## Progress tracker

- [x] RE-389 matrix-transform-core handoff validated.
- [x] Three matrix-transform-core candidates checked for drift.
- [x] Candidate-level proof requirement evaluated.
- [x] Domain/source-patch authorization denied.
- [x] Next deferred bridge-cluster selection handoff emitted.

## Generated artifacts

- `docs/reverse/generated/re390-matrix-transform-core-readiness-gate-candidates.csv`
- `docs/reverse/generated/re390-matrix-transform-core-readiness-gate-gates.csv`
- `docs/reverse/generated/re390-matrix-transform-core-readiness-gate-summary.csv`
- `docs/reverse/generated/re390-matrix-transform-core-readiness-gate-handoff.csv`
- `docs/reverse/functions/re390-matrix-transform-core-readiness-gate.md`

## Findings

- Selected narrow subcluster: `matrix-transform-core`
- Input candidates: `3`
- Gate rows: `1`
- Candidate-level proof rows: `0`
- Ready to reopen domain selection: `0`
- Source patch authorized rows: `0`

## Readiness decision

The `matrix-transform-core` rows remain source-symbolic. Domain and pivot stay `none` / `none`, and code readiness remains `blocked`.

## Follow-up ticket breakdown

- `RE-391` / `post-maths-render-next-ghidra-cluster-selection`: close the maths/render branch and select the next deferred parent bridge cluster.
  - Inputs: RE-390 candidate/gate CSVs plus the parent cluster queue.
  - Deliverables: next-cluster selection rows, summary/handoff, story.
  - Stop condition: if the selected cluster also lacks proof-domain readiness, keep source/code readiness blocked and continue via a narrow export.

## Validation commands

- `python -m pytest tests/reverse/test_re390_matrix_transform_core_readiness_gate.py -q`
- `python scripts/reverse/re390_matrix_transform_core_readiness_gate.py --repo .`
- `python -m pytest tests/reverse -q`
