# RE-322 collision-switch-door next subcluster selection

## Goal

After RE-321 exhausted the collision-geometry helper candidate queue, select the next deferred RE-311 collision/switch/door subcluster without reopening a proof domain or authorizing source changes.

## Inputs

- Upstream handoff: `docs/reverse/generated/re321-collision-geometry-helper-final-candidate-callsite-readiness-handoff.csv`
- Parent subcluster queue: `docs/reverse/generated/re311-ghidra-collision-switch-door-narrow-subclusters.csv`
- Parent candidate rows: `docs/reverse/generated/re311-ghidra-collision-switch-door-narrow-candidates.csv`

## Progress tracker

- [x] RE-321 collision-geometry queue exhaustion validated.
- [x] RE-311 parent subcluster queue checked fail-closed.
- [x] Closed `collision-geometry-helper` excluded from next selection.
- [x] Next deferred subcluster selected in source order.
- [x] Domain/pivot/source-patch readiness kept blocked.

## Generated artifacts

- `docs/reverse/generated/re322-collision-switch-door-next-subcluster-selection-subclusters.csv`
- `docs/reverse/generated/re322-collision-switch-door-next-subcluster-selection-candidates.csv`
- `docs/reverse/generated/re322-collision-switch-door-next-subcluster-selection-summary.csv`
- `docs/reverse/generated/re322-collision-switch-door-next-subcluster-selection-handoff.csv`
- `docs/reverse/functions/re322-collision-switch-door-next-subcluster-selection.md`

## Findings

- Parent scope: `collision-switch-door-cluster`
- Closed subcluster: `collision-geometry-helper`
- Deferred subclusters remaining: `4`
- Selected subcluster: `switch-door-control-helper`
- Selected candidates: `8d1fc6fc3cfc`
- Ready to reopen domain selection: `0`
- Source patch authorized rows: `0`

## Readiness decision

The next subcluster is selected only for a readiness gate. It does not prove a domain or authorize source changes.

## Follow-up ticket breakdown

- `RE-323` / `switch-door-control-helper-readiness-gate`: gate candidate `8d1fc6fc3cfc` in `switch-door-control-helper` before any proof-domain selection.
  - Inputs: RE-322 handoff plus RE-311 source-symbolic candidate metadata.
  - Deliverables: candidate readiness rows, gate decision, and handoff to either a still-narrower candidate export or the next deferred subcluster.
  - Stop condition: if candidate-level proof remains absent, keep source/code readiness blocked.

## Validation commands

- `python -m pytest tests/reverse/test_re322_collision_switch_door_next_subcluster_selection.py -q`
- `python scripts/reverse/re322_collision_switch_door_next_subcluster_selection.py --repo .`
- `python -m pytest tests/reverse -q`
