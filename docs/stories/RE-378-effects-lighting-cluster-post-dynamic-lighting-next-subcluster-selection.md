# RE-378 effects/lighting cluster post dynamic-lighting next subcluster selection

## Goal

Consume the RE-377 dynamic-lighting queue exhaustion and select the next deferred effects/lighting cluster subcluster from the parent queue.

## Inputs

- Exhausted selected-subcluster handoff: `docs/reverse/generated/re377-dynamic-lighting-service-next-candidate-callsite-readiness-handoff.csv`
- Parent selection handoff: `docs/reverse/generated/re370-ghidra-effects-lighting-narrow-handoff.csv`
- Parent subcluster queue: `docs/reverse/generated/re370-ghidra-effects-lighting-narrow-subclusters.csv`
- Candidate metadata: `docs/reverse/generated/re370-ghidra-effects-lighting-narrow-candidates.csv`

## Progress tracker

- [x] RE-377 dynamic-lighting queue exhaustion validated.
- [x] Parent effects/lighting cluster subcluster queue verified fail-closed.
- [x] Closed subclusters excluded: `dynamic-lighting-service`.
- [x] Next deferred subcluster selected: `explosion-flare-effect-service`.
- [x] Readiness gate handoff emitted for `RE-379`.

## Generated artifacts

- `docs/reverse/generated/re378-effects-lighting-cluster-post-dynamic-lighting-next-subcluster-selection-subclusters.csv`
- `docs/reverse/generated/re378-effects-lighting-cluster-post-dynamic-lighting-next-subcluster-selection-candidates.csv`
- `docs/reverse/generated/re378-effects-lighting-cluster-post-dynamic-lighting-next-subcluster-selection-summary.csv`
- `docs/reverse/generated/re378-effects-lighting-cluster-post-dynamic-lighting-next-subcluster-selection-handoff.csv`
- `docs/reverse/functions/re378-effects-lighting-cluster-post-dynamic-lighting-next-subcluster-selection.md`

## Findings

- Parent scope: `effects-lighting-cluster`
- Closed subclusters: `dynamic-lighting-service`
- Input subclusters: `3`
- Remaining deferred subclusters: `2`
- Selected subcluster: `explosion-flare-effect-service`
- Selected candidates: `87d9c8a62335`
- Ready to reopen domain selection: `0`
- Source patch authorized rows: `0`

## Readiness decision

The selected explosion/flare effect subcluster is only ready for a readiness gate. Domain and pivot stay `none`; source/code readiness remains `blocked`.

## Follow-up ticket breakdown

- `RE-379` / `explosion-flare-effect-service-readiness-gate`: gate candidates `87d9c8a62335` before any proof-domain selection.
  - Inputs: RE-378 selected subcluster/candidate rows plus parent queue metadata.
  - Deliverables: candidate readiness rows, selected/denied follow-up proof export, and handoff.
  - Stop condition: if candidate-level source-symbolic proof is still missing, keep source/code readiness blocked.

## Validation commands

- `python -m pytest tests/reverse/test_re378_effects_lighting_cluster_post_dynamic_lighting_next_subcluster_selection.py -q`
- `python scripts/reverse/re378_effects_lighting_cluster_post_dynamic_lighting_next_subcluster_selection.py --repo .`
- `python -m pytest tests/reverse -q`
