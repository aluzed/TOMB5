# RE-377 dynamic-lighting service next candidate callsite readiness gate

## Goal

Gate the RE-376 next-candidate source-backed callsite map, close the dynamic-lighting service queue if no family proves candidate-level behavior, and hand off to the next deferred parent subcluster.

## Inputs

- Upstream handoff: `docs/reverse/generated/re376-dynamic-lighting-service-next-candidate-callsite-handoff.csv`
- Source-backed callsite map: `docs/reverse/generated/re376-dynamic-lighting-service-next-candidate-callsite-map.csv`
- Source context functions: `docs/reverse/generated/re376-dynamic-lighting-service-next-candidate-callsite-functions.csv`
- dynamic-lighting candidate queue: `docs/reverse/generated/re371-dynamic-lighting-service-readiness-gate-candidates.csv`
- Parent effects/lighting subcluster queue: `docs/reverse/generated/re370-ghidra-effects-lighting-narrow-subclusters.csv`

## Progress tracker

- [x] RE-376 next-candidate callsite handoff validated.
- [x] RE-371 dynamic-lighting candidate queue verified exhausted after the second candidate.
- [x] Parent RE-370 deferred subcluster queue checked.
- [x] Next-candidate callsite families grouped and readiness-gated.
- [x] Candidate-level proof and source-patch authorization denied for every family.
- [x] Next parent subcluster selection follow-up emitted.

## Generated artifacts

- `docs/reverse/generated/re377-dynamic-lighting-service-next-candidate-callsite-readiness-families.csv`
- `docs/reverse/generated/re377-dynamic-lighting-service-next-candidate-callsite-readiness-decision.csv`
- `docs/reverse/generated/re377-dynamic-lighting-service-next-candidate-callsite-readiness-summary.csv`
- `docs/reverse/generated/re377-dynamic-lighting-service-next-candidate-callsite-readiness-handoff.csv`
- `docs/reverse/functions/re377-dynamic-lighting-service-next-candidate-callsite-readiness-gate.md`

## Findings

- Source context functions: `21`
- Source-backed callsite rows: `40`
- Callsite families: `6`
- Implemented callsite families: `5`
- Stub-only callsite families: `1`
- Candidate-level proof rows: `0`
- Ready to reopen domain selection: `0`
- Source patch authorized rows: `0`
- Next deferred candidate: `none`
- Next deferred subcluster: `explosion-flare-effect-service`

## Readiness decision

The second dynamic-lighting candidate's source-backed callsite map still does not prove candidate-level behavior. Domain and pivot remain `none`; code readiness remains `blocked`. The dynamic-lighting candidate queue is exhausted.

## Follow-up ticket breakdown

- `RE-378` / `effects-lighting-cluster-post-dynamic-lighting-next-subcluster-selection`: close `dynamic-lighting-service` and select `explosion-flare-effect-service` from the parent RE-370 deferred subcluster queue.
  - Inputs: RE-377 handoff plus RE-370 subcluster queue.
  - Deliverables: metadata-only selected subcluster/candidate rows, summary, and handoff to that subcluster readiness gate.
  - Stop condition: keep source/code readiness blocked until the next selected subcluster has candidate-level proof.

## Validation commands

- `python -m pytest tests/reverse/test_re377_dynamic_lighting_service_next_candidate_callsite_readiness_gate.py -q`
- `python scripts/reverse/re377_dynamic_lighting_service_next_candidate_callsite_readiness_gate.py --repo .`
- `python -m pytest tests/reverse -q`
