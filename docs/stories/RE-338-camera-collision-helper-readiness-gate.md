# RE-338 camera-collision helper readiness gate

## Goal

Gate the RE-337 selected camera-collision helper subcluster before reopening any proof domain or authorizing source/marker changes.

## Inputs

- Upstream handoff: `docs/reverse/generated/re337-collision-switch-door-post-door-save-next-subcluster-selection-handoff.csv`
- RE-337 candidates: `docs/reverse/generated/re337-collision-switch-door-post-door-save-next-subcluster-selection-candidates.csv`
- RE-311 candidates: `docs/reverse/generated/re311-ghidra-collision-switch-door-narrow-candidates.csv`

## Progress tracker

- [x] RE-337 camera-collision helper handoff validated.
- [x] Selected candidate set checked fail-closed against RE-311 metadata.
- [x] Candidate-level readiness row emitted without raw identity columns.
- [x] Domain/pivot/source-patch readiness kept blocked.
- [x] Still-narrower follow-up export selected.

## Generated artifacts

- `docs/reverse/generated/re338-camera-collision-helper-readiness-gate-candidates.csv`
- `docs/reverse/generated/re338-camera-collision-helper-readiness-gate-gates.csv`
- `docs/reverse/generated/re338-camera-collision-helper-readiness-gate-summary.csv`
- `docs/reverse/generated/re338-camera-collision-helper-readiness-gate-handoff.csv`
- `docs/reverse/functions/re338-camera-collision-helper-readiness-gate.md`

## Findings

- Selected narrow subcluster: `camera-collision-helper`
- Input candidates: `1`
- Candidate gate rows: `1`
- Ready to reopen domain selection: `0`
- Source patch authorized rows: `0`
- Selected domain: `none`
- Selected pivot: `none`
- Follow-up candidate id: `95c41ac597d6`

## Readiness decision

The camera-collision helper remains blocked because the current metadata only proves source-symbolic context, not candidate-level proof. Domain and pivot remain `none`, and code readiness remains blocked.

## Follow-up ticket breakdown

- `RE-339` / `camera-collision-helper-candidate-proof-export`: produce a still narrower metadata-only proof export for candidate `95c41ac597d6`.
  - Inputs: RE-338 candidate readiness rows plus local source-symbolic maps.
  - Deliverables: candidate-scoped source-symbolic proof metadata, proof/blocker rows, and a handoff that either names a proof-first domain/pivot or stays blocked.
  - Stop condition: if candidate-level proof is still absent, keep source/code readiness blocked and defer to the next camera-collision candidate action.

## Validation commands

- `python -m pytest tests/reverse/test_re338_camera_collision_helper_readiness_gate.py -q`
- `python scripts/reverse/re338_camera_collision_helper_readiness_gate.py --repo .`
- `python -m pytest tests/reverse -q`
