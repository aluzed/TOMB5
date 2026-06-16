# RE-316 collision geometry helper next candidate proof export

## Goal

Produce a metadata-only proof export for deferred collision-geometry helper candidate `d96359c1d9f3` after `5e99f39fd8ef` was denied by RE-315.

## Inputs

- Upstream handoff: `docs/reverse/generated/re315-collision-geometry-helper-callsite-readiness-handoff.csv`
- RE-312 candidates: `docs/reverse/generated/re312-collision-geometry-helper-readiness-gate-candidates.csv`
- Local function export: `docs/reverse/generated/ghidra-functions.csv`
- Local repo function map: `docs/reverse/generated/repo-function-map.csv`

## Progress tracker

- [x] RE-315 next-candidate handoff validated.
- [x] Selected candidate context reconstructed inside the generator only.
- [x] Candidate-scoped source-symbolic rows emitted without raw identity columns.
- [x] Domain/pivot/source-patch readiness kept blocked.
- [x] Source-backed next-candidate callsite-map follow-up selected.

## Generated artifacts

- `docs/reverse/generated/re316-collision-geometry-helper-next-candidate-proof-contexts.csv`
- `docs/reverse/generated/re316-collision-geometry-helper-next-candidate-proof-gate.csv`
- `docs/reverse/generated/re316-collision-geometry-helper-next-candidate-proof-summary.csv`
- `docs/reverse/generated/re316-collision-geometry-helper-next-candidate-proof-handoff.csv`
- `docs/reverse/functions/re316-collision-geometry-helper-next-candidate-proof-export.md`

## Findings

- Selected candidate id: `d96359c1d9f3`
- Previous denied candidate id: `5e99f39fd8ef`
- Source-symbolic context rows: `27`
- Caller context rows: `23`
- Callee context rows: `4`
- Direct repo symbol rows: `0`
- Candidate-level proof rows: `0`
- Ready to reopen domain selection: `0`
- Source patch authorized rows: `0`

## Readiness decision

The deferred candidate has useful source-symbolic caller/callee context, but no direct source-backed candidate proof. Domain and pivot remain `none`, and code readiness remains blocked.

## Follow-up ticket breakdown

- `RE-317` / `collision-geometry-helper-next-candidate-callsite-map`: build a source-backed callsite map for candidate `d96359c1d9f3`.
  - Inputs: RE-316 context/proof rows plus local source files and repo map metadata.
  - Deliverables: source-backed callsite rows with real file/line references, proof/blocker rows, and a handoff that either selects a proof pivot or stays blocked.
  - Stop condition: if source-backed callsites cannot prove candidate-level behavior without raw evidence, keep source/code readiness blocked and defer the remaining candidates.

## Validation commands

- `python -m pytest tests/reverse/test_re316_collision_geometry_helper_next_candidate_proof_export.py -q`
- `python scripts/reverse/re316_collision_geometry_helper_next_candidate_proof_export.py --repo .`
- `python -m pytest tests/reverse -q`
