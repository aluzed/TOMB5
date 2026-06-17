# RE-327 collision-switch-door post-switch-door next subcluster selection

## Goal

Consume the RE-326 switch-door-control candidate queue exhaustion and select the next deferred collision/switch/door subcluster from the parent queue.

## Inputs

- Exhausted selected-subcluster handoff: `docs/reverse/generated/re326-switch-door-control-helper-callsite-readiness-handoff.csv`
- Parent subcluster queue: `docs/reverse/generated/re322-collision-switch-door-next-subcluster-selection-subclusters.csv`
- Candidate metadata: `docs/reverse/generated/re311-ghidra-collision-switch-door-narrow-candidates.csv`

## Progress tracker

- [x] RE-326 switch-door candidate queue exhaustion validated.
- [x] Parent collision/switch/door subcluster queue verified fail-closed.
- [x] Closed subclusters excluded: `collision-geometry-helper;switch-door-control-helper`.
- [x] Next deferred subcluster selected: `weapon-switch-effect-helper`.
- [x] Readiness gate handoff emitted for `RE-328`.

## Generated artifacts

- `docs/reverse/generated/re327-collision-switch-door-post-switch-door-next-subcluster-selection-subclusters.csv`
- `docs/reverse/generated/re327-collision-switch-door-post-switch-door-next-subcluster-selection-candidates.csv`
- `docs/reverse/generated/re327-collision-switch-door-post-switch-door-next-subcluster-selection-summary.csv`
- `docs/reverse/generated/re327-collision-switch-door-post-switch-door-next-subcluster-selection-handoff.csv`
- `docs/reverse/functions/re327-collision-switch-door-post-switch-door-next-subcluster-selection.md`

## Findings

- Parent scope: `collision-switch-door-cluster`
- Closed subclusters: `collision-geometry-helper;switch-door-control-helper`
- Input subclusters: `5`
- Remaining deferred subclusters: `3`
- Selected subcluster: `weapon-switch-effect-helper`
- Selected candidate: `1ddbda046e37`
- Ready to reopen domain selection: `0`
- Source patch authorized rows: `0`

## Readiness decision

The selected weapon/switch/effect subcluster is only ready for a readiness gate. Domain and pivot stay `none`; source/code readiness remains `blocked`.

## Follow-up ticket breakdown

- `RE-328` / `weapon-switch-effect-helper-readiness-gate`: gate candidate `1ddbda046e37` before any proof-domain selection.
  - Inputs: RE-327 selected subcluster/candidate rows plus the parent queue metadata.
  - Deliverables: candidate readiness rows, selected/denied follow-up proof export, and handoff.
  - Stop condition: if candidate-level source-symbolic proof is still missing, keep source/code readiness blocked.

## Validation commands

- `python -m pytest tests/reverse/test_re327_collision_switch_door_post_switch_door_next_subcluster_selection.py -q`
- `python scripts/reverse/re327_collision_switch_door_post_switch_door_next_subcluster_selection.py --repo .`
- `python -m pytest tests/reverse -q`
