# RE-383 effects/lighting cluster post explosion/flare next subcluster selection

## Goal

Consume the RE-382 explosion/flare queue exhaustion and select the next deferred effects/lighting cluster subcluster from the parent queue.

## Inputs

- Exhausted selected-subcluster handoff: `docs/reverse/generated/re382-explosion-flare-effect-service-callsite-readiness-handoff.csv`
- Parent selection handoff: `docs/reverse/generated/re370-ghidra-effects-lighting-narrow-handoff.csv`
- Parent subcluster queue: `docs/reverse/generated/re370-ghidra-effects-lighting-narrow-subclusters.csv`
- Candidate metadata: `docs/reverse/generated/re370-ghidra-effects-lighting-narrow-candidates.csv`

## Progress tracker

- [x] RE-382 explosion/flare queue exhaustion validated.
- [x] Parent effects/lighting cluster subcluster queue verified fail-closed.
- [x] Closed subclusters excluded: `dynamic-lighting-service;explosion-flare-effect-service`.
- [x] Next deferred subcluster selected: `spotcam-projectile-effect-service`.
- [x] Readiness gate handoff emitted for `RE-384`.

## Generated artifacts

- `docs/reverse/generated/re383-effects-lighting-cluster-post-explosion-flare-next-subcluster-selection-subclusters.csv`
- `docs/reverse/generated/re383-effects-lighting-cluster-post-explosion-flare-next-subcluster-selection-candidates.csv`
- `docs/reverse/generated/re383-effects-lighting-cluster-post-explosion-flare-next-subcluster-selection-summary.csv`
- `docs/reverse/generated/re383-effects-lighting-cluster-post-explosion-flare-next-subcluster-selection-handoff.csv`
- `docs/reverse/functions/re383-effects-lighting-cluster-post-explosion-flare-next-subcluster-selection.md`

## Findings

- Parent scope: `effects-lighting-cluster`
- Closed subclusters: `dynamic-lighting-service;explosion-flare-effect-service`
- Input subclusters: `3`
- Remaining deferred subclusters: `1`
- Selected subcluster: `spotcam-projectile-effect-service`
- Selected candidates: `b6d128932004`
- Ready to reopen domain selection: `0`
- Source patch authorized rows: `0`

## Readiness decision

The selected spotcam/projectile effect subcluster is only ready for a readiness gate. Domain and pivot stay `none`; source/code readiness remains `blocked`.

## Follow-up ticket breakdown

- `RE-384` / `spotcam-projectile-effect-service-readiness-gate`: gate candidates `b6d128932004` before any proof-domain selection.
  - Inputs: RE-383 selected subcluster/candidate rows plus parent queue metadata.
  - Deliverables: candidate readiness rows, selected/denied follow-up proof export, and handoff.
  - Stop condition: if candidate-level source-symbolic proof is still missing, keep source/code readiness blocked.

## Validation commands

- `python -m pytest tests/reverse/test_re383_effects_lighting_cluster_post_explosion_flare_next_subcluster_selection.py -q`
- `python scripts/reverse/re383_effects_lighting_cluster_post_explosion_flare_next_subcluster_selection.py --repo .`
- `python -m pytest tests/reverse -q`
