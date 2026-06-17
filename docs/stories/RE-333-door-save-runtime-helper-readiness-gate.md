# RE-333 door-save-runtime helper readiness gate

## Goal

Gate the RE-332 selected door-save-runtime helper subcluster before reopening any proof domain or authorizing source/marker changes.

## Inputs

- Upstream handoff: `docs/reverse/generated/re332-collision-switch-door-post-weapon-switch-next-subcluster-selection-handoff.csv`
- RE-311 candidates: `docs/reverse/generated/re311-ghidra-collision-switch-door-narrow-candidates.csv`

## Progress tracker

- [x] RE-332 door-save-runtime helper handoff validated.
- [x] Selected candidate set checked fail-closed.
- [x] Candidate-level readiness row emitted without raw identity columns.
- [x] Domain/pivot/source-patch readiness kept blocked.
- [x] Still-narrower follow-up export selected.

## Generated artifacts

- `docs/reverse/generated/re333-door-save-runtime-helper-readiness-gate-candidates.csv`
- `docs/reverse/generated/re333-door-save-runtime-helper-readiness-gate-gates.csv`
- `docs/reverse/generated/re333-door-save-runtime-helper-readiness-gate-summary.csv`
- `docs/reverse/generated/re333-door-save-runtime-helper-readiness-gate-handoff.csv`
- `docs/reverse/functions/re333-door-save-runtime-helper-readiness-gate.md`

## Findings

- Selected narrow subcluster: `door-save-runtime-helper`
- Input candidates: `1`
- Candidate gate rows: `1`
- Ready to reopen domain selection: `0`
- Source patch authorized rows: `0`
- Selected domain: `none`
- Selected pivot: `none`
- Follow-up candidate id: `f457f2772655`

## Readiness decision

The door-save-runtime helper remains blocked because the current metadata only proves source-symbolic context, not candidate-level proof. Domain and pivot remain `none`, and code readiness remains blocked.

## Follow-up ticket breakdown

- `RE-334` / `door-save-runtime-helper-candidate-proof-export`: produce a still narrower metadata-only proof export for candidate `f457f2772655`.
  - Inputs: RE-333 candidate readiness rows plus local Ghidra/repo maps.
  - Deliverables: candidate-scoped source-symbolic proof metadata, proof/blocker rows, and a handoff that either names a proof-first domain/pivot or stays blocked.
  - Stop condition: if candidate-level proof is still absent, keep source/code readiness blocked and defer to the next door/save/runtime candidate action.

## Validation commands

- `python -m pytest tests/reverse/test_re333_door_save_runtime_helper_readiness_gate.py -q`
- `python scripts/reverse/re333_door_save_runtime_helper_readiness_gate.py --repo .`
- `python -m pytest tests/reverse -q`
