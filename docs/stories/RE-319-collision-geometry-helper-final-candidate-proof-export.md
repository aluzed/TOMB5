# RE-319 collision geometry helper final candidate proof export

## Goal

Produce a metadata-only proof export for deferred collision-geometry helper candidate `61d55bb1809b` after `d96359c1d9f3` was denied by RE-318.

## Inputs

- Upstream handoff: `docs/reverse/generated/re318-collision-geometry-helper-next-candidate-callsite-readiness-handoff.csv`
- RE-312 candidates: `docs/reverse/generated/re312-collision-geometry-helper-readiness-gate-candidates.csv`
- Local function export: `docs/reverse/generated/ghidra-functions.csv`
- Local repo function map: `docs/reverse/generated/repo-function-map.csv`

## Progress tracker

- [x] RE-318 final-candidate handoff validated.
- [x] Selected candidate context reconstructed inside the generator only.
- [x] Candidate-scoped source-symbolic rows emitted without raw identity columns.
- [x] Domain/pivot/source-patch readiness kept blocked.
- [x] Source-backed final-candidate callsite-map follow-up selected.

## Generated artifacts

- `docs/reverse/generated/re319-collision-geometry-helper-final-candidate-proof-contexts.csv`
- `docs/reverse/generated/re319-collision-geometry-helper-final-candidate-proof-gate.csv`
- `docs/reverse/generated/re319-collision-geometry-helper-final-candidate-proof-summary.csv`
- `docs/reverse/generated/re319-collision-geometry-helper-final-candidate-proof-handoff.csv`
- `docs/reverse/functions/re319-collision-geometry-helper-final-candidate-proof-export.md`

## Findings

- Selected candidate id: `61d55bb1809b`
- Previous denied candidate id: `d96359c1d9f3`
- Source-symbolic context rows: `21`
- Caller context rows: `20`
- Callee context rows: `1`
- Direct repo symbol rows: `0`
- Candidate-level proof rows: `0`
- Ready to reopen domain selection: `0`
- Source patch authorized rows: `0`

## Readiness decision

The deferred candidate has useful source-symbolic caller/callee context, but no direct source-backed candidate proof. Domain and pivot remain `none`, and code readiness remains blocked.

## Follow-up ticket breakdown

- `RE-320` / `collision-geometry-helper-final-candidate-callsite-map`: build a source-backed callsite map for candidate `61d55bb1809b`.
  - Inputs: RE-319 context/proof rows plus local source files and repo map metadata.
  - Deliverables: source-backed callsite rows with real file/line references, proof/blocker rows, and a handoff that either selects a proof pivot or stays blocked.
  - Stop condition: if source-backed callsites cannot prove candidate-level behavior without raw evidence, keep source/code readiness blocked and gate final-candidate callsite families before declaring the candidate queue exhausted.

## Validation commands

- `python -m pytest tests/reverse/test_re319_collision_geometry_helper_final_candidate_proof_export.py -q`
- `python scripts/reverse/re319_collision_geometry_helper_final_candidate_proof_export.py --repo .`
- `python -m pytest tests/reverse -q`
