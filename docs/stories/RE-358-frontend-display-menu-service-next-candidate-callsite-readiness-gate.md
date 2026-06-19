# RE-358 frontend display/menu service next candidate callsite readiness gate

## Goal

Gate the RE-357 next-candidate source-backed callsite map, close the frontend display/menu service queue if no family proves candidate-level behavior, and hand off to the next deferred parent subcluster.

## Inputs

- Upstream handoff: `docs/reverse/generated/re357-frontend-display-menu-service-next-candidate-callsite-handoff.csv`
- Source-backed callsite map: `docs/reverse/generated/re357-frontend-display-menu-service-next-candidate-callsite-map.csv`
- Source context functions: `docs/reverse/generated/re357-frontend-display-menu-service-next-candidate-callsite-functions.csv`
- frontend display/menu candidate queue: `docs/reverse/generated/re352-frontend-display-menu-service-readiness-gate-candidates.csv`
- Parent platform/frontend subcluster queue: `docs/reverse/generated/re343-ghidra-platform-frontend-service-narrow-subclusters.csv`

## Progress tracker

- [x] RE-357 next-candidate callsite handoff validated.
- [x] RE-352 frontend display/menu candidate queue verified exhausted after the second candidate.
- [x] Parent RE-343 deferred subcluster queue checked.
- [x] Next-candidate callsite families grouped and readiness-gated.
- [x] Candidate-level proof and source-patch authorization denied for every family.
- [x] Next parent subcluster selection follow-up emitted.

## Generated artifacts

- `docs/reverse/generated/re358-frontend-display-menu-service-next-candidate-callsite-readiness-families.csv`
- `docs/reverse/generated/re358-frontend-display-menu-service-next-candidate-callsite-readiness-decision.csv`
- `docs/reverse/generated/re358-frontend-display-menu-service-next-candidate-callsite-readiness-summary.csv`
- `docs/reverse/generated/re358-frontend-display-menu-service-next-candidate-callsite-readiness-handoff.csv`
- `docs/reverse/functions/re358-frontend-display-menu-service-next-candidate-callsite-readiness-gate.md`

## Findings

- Source context functions: `18`
- Source-backed callsite rows: `126`
- Callsite families: `5`
- Implemented callsite families: `5`
- Stub-only callsite families: `0`
- Candidate-level proof rows: `0`
- Ready to reopen domain selection: `0`
- Source patch authorized rows: `0`
- Next deferred candidate: `none`
- Next deferred subcluster: `gpu-fmv-mainloop-service`

## Readiness decision

The second frontend display/menu candidate's source-backed callsite map still does not prove candidate-level behavior. Domain and pivot remain `none`; code readiness remains `blocked`. The frontend display/menu candidate queue is exhausted.

## Follow-up ticket breakdown

- `RE-359` / `platform-frontend-service-post-frontend-display-menu-next-subcluster-selection`: close `frontend-display-menu-service` and select `gpu-fmv-mainloop-service` from the parent RE-343 deferred subcluster queue.
  - Inputs: RE-358 handoff plus RE-343 subcluster queue.
  - Deliverables: metadata-only selected subcluster/candidate rows, summary, and handoff to that subcluster readiness gate.
  - Stop condition: keep source/code readiness blocked until the next selected subcluster has candidate-level proof.

## Validation commands

- `python -m pytest tests/reverse/test_re358_frontend_display_menu_service_next_candidate_callsite_readiness_gate.py -q`
- `python scripts/reverse/re358_frontend_display_menu_service_next_candidate_callsite_readiness_gate.py --repo .`
- `python -m pytest tests/reverse -q`
