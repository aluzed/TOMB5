# RE-311 Ghidra collision/switch/door narrow export

## Goal

Produce a narrower metadata-only source-symbolic export for the RE-310 collision/switch/door focus cluster without committing raw Ghidra identity.

## Inputs

- Upstream handoff: `docs/reverse/generated/re310-ghidra-bridge-candidate-readiness-gate-handoff.csv`
- RE-310 candidates: `docs/reverse/generated/re310-ghidra-bridge-candidate-readiness-gate-candidates.csv`
- Local Ghidra export: `docs/reverse/generated/ghidra-functions.csv`
- Local repo function map: `docs/reverse/generated/repo-function-map.csv`

## Progress tracker

- [x] RE-310 focus cluster validated.
- [x] Local raw Ghidra identity resolved only inside the generator.
- [x] Narrow source-symbolic subclusters emitted without raw identity columns.
- [x] Collision-geometry helper subcluster selected for a readiness gate.
- [x] Source/domain readiness kept blocked.

## Generated artifacts

- `docs/reverse/generated/re311-ghidra-collision-switch-door-narrow-subclusters.csv`
- `docs/reverse/generated/re311-ghidra-collision-switch-door-narrow-candidates.csv`
- `docs/reverse/generated/re311-ghidra-collision-switch-door-narrow-summary.csv`
- `docs/reverse/generated/re311-ghidra-collision-switch-door-narrow-handoff.csv`
- `docs/reverse/functions/re311-ghidra-collision-switch-door-narrow-export.md`

## Findings

- Focus cluster: `collision-switch-door-cluster`
- Focus candidates: `7`
- Local identities resolved inside generator: `7`
- Narrow subclusters: `5`
- Selected narrow subcluster: `collision-geometry-helper`
- Selected candidate count: `3`
- Ready to reopen domain selection: `0`
- Source patch authorized rows: `0`

## Readiness decision

This export narrows the candidate space but still does not select a proof domain. Domain/pivot remain `none`, and code readiness remains blocked.

## Follow-up ticket breakdown

- `RE-312` / `collision-geometry-helper-readiness-gate`: gate the selected collision-geometry helper subcluster and decide whether it can produce a proof-first pivot.
  - Inputs: RE-311 subcluster and candidate CSVs plus local Ghidra/repo maps.
  - Deliverables: candidate-level readiness rows and a handoff that either names a proof-first pivot or keeps domain/pivot `none`.
  - Stop condition: if every row still lacks candidate-level source-symbolic proof, keep source/code readiness blocked and request a still narrower export.

## Validation commands

- `python -m pytest tests/reverse/test_re311_ghidra_collision_switch_door_narrow_export.py -q`
- `python scripts/reverse/re311_ghidra_collision_switch_door_narrow_export.py --repo .`
- `python -m pytest tests/reverse -q`
