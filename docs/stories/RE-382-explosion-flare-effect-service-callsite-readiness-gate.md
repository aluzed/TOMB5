# RE-382 explosion/flare effect service callsite readiness gate

## Goal

Gate the RE-381 source-backed callsite map, close the explosion/flare effect service queue if no family proves candidate-level behavior, and hand off to the next deferred parent subcluster.

## Inputs

- Upstream handoff: `docs/reverse/generated/re381-explosion-flare-effect-service-candidate-callsite-handoff.csv`
- Source-backed callsite map: `docs/reverse/generated/re381-explosion-flare-effect-service-candidate-callsite-map.csv`
- Source context functions: `docs/reverse/generated/re381-explosion-flare-effect-service-candidate-callsite-functions.csv`
- explosion/flare candidate queue: `docs/reverse/generated/re379-explosion-flare-effect-service-readiness-gate-candidates.csv`
- Parent effects/lighting subcluster queue: `docs/reverse/generated/re370-ghidra-effects-lighting-narrow-subclusters.csv`

## Progress tracker

- [x] RE-381 callsite-map handoff validated.
- [x] RE-379 explosion/flare candidate queue verified exhausted after the selected candidate.
- [x] Parent RE-370 deferred subcluster queue checked.
- [x] Explosion/flare callsite families grouped and readiness-gated.
- [x] Candidate-level proof and source-patch authorization denied for every family.
- [x] Next parent subcluster selection follow-up emitted.

## Generated artifacts

- `docs/reverse/generated/re382-explosion-flare-effect-service-callsite-readiness-families.csv`
- `docs/reverse/generated/re382-explosion-flare-effect-service-callsite-readiness-decision.csv`
- `docs/reverse/generated/re382-explosion-flare-effect-service-callsite-readiness-summary.csv`
- `docs/reverse/generated/re382-explosion-flare-effect-service-callsite-readiness-handoff.csv`
- `docs/reverse/functions/re382-explosion-flare-effect-service-callsite-readiness-gate.md`

## Findings

- Source context functions: `18`
- Source-backed callsite rows: `121`
- Callsite families: `7`
- Implemented callsite families: `6`
- Stub-only callsite families: `1`
- Candidate-level proof rows: `0`
- Ready to reopen domain selection: `0`
- Source patch authorized rows: `0`
- Next deferred candidate: `none`
- Next deferred subcluster: `spotcam-projectile-effect-service`

## Readiness decision

The only explosion/flare candidate's source-backed callsite map still does not prove candidate-level behavior. Domain and pivot remain `none`; code readiness remains `blocked`. The explosion/flare candidate queue is exhausted.

## Follow-up ticket breakdown

- `RE-383` / `effects-lighting-cluster-post-explosion-flare-next-subcluster-selection`: close `explosion-flare-effect-service` and select `spotcam-projectile-effect-service` from the parent RE-370 deferred subcluster queue.
  - Inputs: RE-382 handoff plus RE-370 subcluster queue.
  - Deliverables: metadata-only selected subcluster/candidate rows, summary, and handoff to that subcluster readiness gate.
  - Stop condition: keep source/code readiness blocked until the next selected subcluster has candidate-level proof.

## Validation commands

- `python -m pytest tests/reverse/test_re382_explosion_flare_effect_service_callsite_readiness_gate.py -q`
- `python scripts/reverse/re382_explosion_flare_effect_service_callsite_readiness_gate.py --repo .`
- `python -m pytest tests/reverse -q`
