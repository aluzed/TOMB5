# RE-394 lara combat camera post lara control next subcluster selection

## Goal

After RE-393 closed lara-control-service without candidate-level proof, select the remaining deferred RE-392 lara/combat/camera subcluster.

## Inputs

- Exhaustion handoff: `docs/reverse/generated/re393-lara-control-service-readiness-gate-handoff.csv`
- Parent narrow handoff: `docs/reverse/generated/re392-ghidra-lara-combat-camera-cluster-narrow-handoff.csv`
- Parent subcluster queue: `docs/reverse/generated/re392-ghidra-lara-combat-camera-cluster-narrow-subclusters.csv`
- Parent candidates: `docs/reverse/generated/re392-ghidra-lara-combat-camera-cluster-narrow-candidates.csv`

## Progress tracker

- [x] RE-393 lara-control exhaustion handoff validated.
- [x] RE-392 parent narrow handoff and deterministic queue re-opened.
- [x] lara-control-service marked closed.
- [x] Next deferred subcluster selected in parent order.
- [x] Domain, pivot, and source/code readiness kept blocked.

## Generated artifacts

- `docs/reverse/generated/re394-lara-combat-camera-post-lara-control-next-subcluster-selection-subclusters.csv`
- `docs/reverse/generated/re394-lara-combat-camera-post-lara-control-next-subcluster-selection-candidates.csv`
- `docs/reverse/generated/re394-lara-combat-camera-post-lara-control-next-subcluster-selection-summary.csv`
- `docs/reverse/generated/re394-lara-combat-camera-post-lara-control-next-subcluster-selection-handoff.csv`
- `docs/reverse/functions/re394-lara-combat-camera-post-lara-control-next-subcluster-selection.md`

## Findings

- Parent scope: `lara-combat-camera-cluster-narrow-subclusters`
- Closed subclusters: `lara-control-service`
- Deferred subclusters: `1`
- Selected follow-up subcluster: `combat-camera-service`
- Selected candidate IDs: `0aaa76206517`
- Ready to reopen domain selection: `0`
- Source patch authorized rows: `0`

## Readiness decision

The selected combat/camera queue remains source-symbolic only. Domain and pivot stay `none` / `none`, and code readiness remains `blocked` until its readiness gate establishes candidate-level proof.

## Follow-up ticket breakdown

- `RE-395` / `combat-camera-service-readiness-gate`: gate `combat-camera-service` before proof-domain selection.
  - Inputs: RE-394 selected candidate and source-symbolic context.
  - Deliverables: candidate gate, summary/handoff, and story with tracker.
  - Stop condition: if candidate-level proof remains absent, keep source/code readiness blocked and select a safe follow-up.

## Validation commands

- `python -m pytest tests/reverse/test_re394_lara_combat_camera_post_lara_control_next_subcluster_selection.py -q`
- `python scripts/reverse/re394_lara_combat_camera_post_lara_control_next_subcluster_selection.py --repo .`
- `python -m pytest tests/reverse -q`
