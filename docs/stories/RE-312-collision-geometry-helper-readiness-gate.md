# RE-312 collision geometry helper readiness gate

## Goal

Gate the RE-311 selected collision-geometry helper subcluster before reopening any proof domain or authorizing source/marker changes.

## Inputs

- Upstream handoff: `docs/reverse/generated/re311-ghidra-collision-switch-door-narrow-handoff.csv`
- RE-311 candidates: `docs/reverse/generated/re311-ghidra-collision-switch-door-narrow-candidates.csv`

## Progress tracker

- [x] RE-311 collision-geometry helper handoff validated.
- [x] Selected candidate set checked fail-closed.
- [x] Candidate-level readiness rows emitted without raw identity columns.
- [x] Domain/pivot/source-patch readiness kept blocked.
- [x] Still-narrower follow-up export selected.

## Generated artifacts

- `docs/reverse/generated/re312-collision-geometry-helper-readiness-gate-candidates.csv`
- `docs/reverse/generated/re312-collision-geometry-helper-readiness-gate-gates.csv`
- `docs/reverse/generated/re312-collision-geometry-helper-readiness-gate-summary.csv`
- `docs/reverse/generated/re312-collision-geometry-helper-readiness-gate-handoff.csv`
- `docs/reverse/functions/re312-collision-geometry-helper-readiness-gate.md`

## Findings

- Selected narrow subcluster: `collision-geometry-helper`
- Input candidates: `3`
- Candidate gate rows: `3`
- Ready to reopen domain selection: `0`
- Source patch authorized rows: `0`
- Selected domain: `none`
- Selected pivot: `none`
- Follow-up candidate id: `5e99f39fd8ef`

## Readiness decision

All collision-geometry helper candidates remain blocked because the current metadata only proves broad source-symbolic context, not candidate-level proof. Domain and pivot remain `none`, and code readiness remains blocked.

## Follow-up ticket breakdown

- `RE-313` / `collision-geometry-helper-candidate-proof-export`: produce a still narrower metadata-only proof export for candidate `5e99f39fd8ef`.
  - Inputs: RE-312 candidate readiness rows plus local Ghidra/repo maps.
  - Deliverables: candidate-scoped source-symbolic proof metadata, proof/blocker rows, and a handoff that either names a proof-first domain/pivot or stays blocked.
  - Stop condition: if candidate-level proof is still absent, keep source/code readiness blocked and defer the remaining collision-geometry candidates.

## Validation commands

- `python -m pytest tests/reverse/test_re312_collision_geometry_helper_readiness_gate.py -q`
- `python scripts/reverse/re312_collision_geometry_helper_readiness_gate.py --repo .`
- `python -m pytest tests/reverse -q`
