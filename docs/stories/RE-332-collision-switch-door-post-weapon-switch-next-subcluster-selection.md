# RE-332 collision-switch-door post-weapon-switch next subcluster selection

## Goal

Consume the RE-331 weapon-switch-effect candidate queue exhaustion and select the next deferred collision/switch/door subcluster from the parent queue.

## Inputs

- Exhausted selected-subcluster handoff: `docs/reverse/generated/re331-weapon-switch-effect-helper-callsite-readiness-handoff.csv`
- Parent subcluster queue: `docs/reverse/generated/re327-collision-switch-door-post-switch-door-next-subcluster-selection-subclusters.csv`
- Parent selection handoff: `docs/reverse/generated/re327-collision-switch-door-post-switch-door-next-subcluster-selection-handoff.csv`
- Candidate metadata: `docs/reverse/generated/re311-ghidra-collision-switch-door-narrow-candidates.csv`

## Progress tracker

- [x] RE-331 weapon-switch candidate queue exhaustion validated.
- [x] Parent collision/switch/door subcluster queue verified fail-closed.
- [x] Closed subclusters excluded: `collision-geometry-helper;switch-door-control-helper;weapon-switch-effect-helper`.
- [x] Next deferred subcluster selected: `door-save-runtime-helper`.
- [x] Readiness gate handoff emitted for `RE-333`.

## Generated artifacts

- `docs/reverse/generated/re332-collision-switch-door-post-weapon-switch-next-subcluster-selection-subclusters.csv`
- `docs/reverse/generated/re332-collision-switch-door-post-weapon-switch-next-subcluster-selection-candidates.csv`
- `docs/reverse/generated/re332-collision-switch-door-post-weapon-switch-next-subcluster-selection-summary.csv`
- `docs/reverse/generated/re332-collision-switch-door-post-weapon-switch-next-subcluster-selection-handoff.csv`
- `docs/reverse/functions/re332-collision-switch-door-post-weapon-switch-next-subcluster-selection.md`

## Findings

- Parent scope: `collision-switch-door-cluster`
- Closed subclusters: `collision-geometry-helper;switch-door-control-helper;weapon-switch-effect-helper`
- Input subclusters: `5`
- Remaining deferred subclusters: `2`
- Selected subcluster: `door-save-runtime-helper`
- Selected candidate: `f457f2772655`
- Ready to reopen domain selection: `0`
- Source patch authorized rows: `0`

## Readiness decision

The selected door/save/runtime subcluster is only ready for a readiness gate. Domain and pivot stay `none`; source/code readiness remains `blocked`.

## Follow-up ticket breakdown

- `RE-333` / `door-save-runtime-helper-readiness-gate`: gate candidate `f457f2772655` before any proof-domain selection.
  - Inputs: RE-332 selected subcluster/candidate rows plus the parent queue metadata.
  - Deliverables: candidate readiness rows, selected/denied follow-up proof export, and handoff.
  - Stop condition: if candidate-level source-symbolic proof is still missing, keep source/code readiness blocked.

## Validation commands

- `python -m pytest tests/reverse/test_re332_collision_switch_door_post_weapon_switch_next_subcluster_selection.py -q`
- `python scripts/reverse/re332_collision_switch_door_post_weapon_switch_next_subcluster_selection.py --repo .`
- `python -m pytest tests/reverse -q`
