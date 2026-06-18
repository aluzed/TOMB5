# RE-337 collision-switch-door post-door-save next subcluster selection

## Goal

Consume the RE-336 door-save-runtime candidate queue exhaustion and select the final deferred collision/switch/door subcluster from the parent queue.

## Inputs

- Exhausted selected-subcluster handoff: `docs/reverse/generated/re336-door-save-runtime-helper-callsite-readiness-handoff.csv`
- Parent selection handoff: `docs/reverse/generated/re332-collision-switch-door-post-weapon-switch-next-subcluster-selection-handoff.csv`
- Parent subcluster queue: `docs/reverse/generated/re332-collision-switch-door-post-weapon-switch-next-subcluster-selection-subclusters.csv`
- Candidate metadata: `docs/reverse/generated/re311-ghidra-collision-switch-door-narrow-candidates.csv`

## Progress tracker

- [x] RE-336 door-save candidate queue exhaustion validated.
- [x] Parent collision/switch/door subcluster queue verified fail-closed.
- [x] Closed subclusters excluded: `collision-geometry-helper;switch-door-control-helper;weapon-switch-effect-helper;door-save-runtime-helper`.
- [x] Final deferred subcluster selected: `camera-collision-helper`.
- [x] Readiness gate handoff emitted for `RE-338`.

## Generated artifacts

- `docs/reverse/generated/re337-collision-switch-door-post-door-save-next-subcluster-selection-subclusters.csv`
- `docs/reverse/generated/re337-collision-switch-door-post-door-save-next-subcluster-selection-candidates.csv`
- `docs/reverse/generated/re337-collision-switch-door-post-door-save-next-subcluster-selection-summary.csv`
- `docs/reverse/generated/re337-collision-switch-door-post-door-save-next-subcluster-selection-handoff.csv`
- `docs/reverse/functions/re337-collision-switch-door-post-door-save-next-subcluster-selection.md`

## Findings

- Parent scope: `collision-switch-door-cluster`
- Closed subclusters: `collision-geometry-helper;switch-door-control-helper;weapon-switch-effect-helper;door-save-runtime-helper`
- Input subclusters: `5`
- Remaining deferred subclusters: `1`
- Selected subcluster: `camera-collision-helper`
- Selected candidate: `95c41ac597d6`
- Ready to reopen domain selection: `0`
- Source patch authorized rows: `0`

## Readiness decision

The selected camera/collision subcluster is only ready for a readiness gate. Domain and pivot stay `none`; source/code readiness remains `blocked`.

## Follow-up ticket breakdown

- `RE-338` / `camera-collision-helper-readiness-gate`: gate candidate `95c41ac597d6` before any proof-domain selection.
  - Inputs: RE-337 selected subcluster/candidate rows plus the parent queue metadata.
  - Deliverables: candidate readiness rows, selected/denied follow-up proof export, and handoff.
  - Stop condition: if candidate-level source-symbolic proof is still missing, keep source/code readiness blocked.

## Validation commands

- `python -m pytest tests/reverse/test_re337_collision_switch_door_post_door_save_next_subcluster_selection.py -q`
- `python scripts/reverse/re337_collision_switch_door_post_door_save_next_subcluster_selection.py --repo .`
- `python -m pytest tests/reverse -q`
