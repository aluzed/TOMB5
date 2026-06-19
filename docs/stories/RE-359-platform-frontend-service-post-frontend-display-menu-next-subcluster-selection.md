# RE-359 platform/frontend service post frontend display/menu next subcluster selection

## Goal

Consume the RE-358 frontend display/menu queue exhaustion and select the next deferred platform/frontend service subcluster from the parent queue.

## Inputs

- Exhausted selected-subcluster handoff: `docs/reverse/generated/re358-frontend-display-menu-service-next-candidate-callsite-readiness-handoff.csv`
- Parent selection handoff: `docs/reverse/generated/re343-ghidra-platform-frontend-service-narrow-handoff.csv`
- Parent subcluster queue: `docs/reverse/generated/re343-ghidra-platform-frontend-service-narrow-subclusters.csv`
- Candidate metadata: `docs/reverse/generated/re343-ghidra-platform-frontend-service-narrow-candidates.csv`

## Progress tracker

- [x] RE-358 frontend display/menu queue exhaustion validated.
- [x] Parent platform/frontend service subcluster queue verified fail-closed.
- [x] Closed subclusters excluded: `cd-load-audio-service;frontend-display-menu-service`.
- [x] Next deferred subcluster selected: `gpu-fmv-mainloop-service`.
- [x] Readiness gate handoff emitted for `RE-360`.

## Generated artifacts

- `docs/reverse/generated/re359-platform-frontend-service-post-frontend-display-menu-next-subcluster-selection-subclusters.csv`
- `docs/reverse/generated/re359-platform-frontend-service-post-frontend-display-menu-next-subcluster-selection-candidates.csv`
- `docs/reverse/generated/re359-platform-frontend-service-post-frontend-display-menu-next-subcluster-selection-summary.csv`
- `docs/reverse/generated/re359-platform-frontend-service-post-frontend-display-menu-next-subcluster-selection-handoff.csv`
- `docs/reverse/functions/re359-platform-frontend-service-post-frontend-display-menu-next-subcluster-selection.md`

## Findings

- Parent scope: `platform-frontend-service-cluster`
- Closed subclusters: `cd-load-audio-service;frontend-display-menu-service`
- Input subclusters: `4`
- Remaining deferred subclusters: `2`
- Selected subcluster: `gpu-fmv-mainloop-service`
- Selected candidates: `1b3534d34062`
- Ready to reopen domain selection: `0`
- Source patch authorized rows: `0`

## Readiness decision

The selected gpu/fmv mainloop subcluster is only ready for a readiness gate. Domain and pivot stay `none`; source/code readiness remains `blocked`.

## Follow-up ticket breakdown

- `RE-360` / `gpu-fmv-mainloop-service-readiness-gate`: gate candidates `1b3534d34062` before any proof-domain selection.
  - Inputs: RE-359 selected subcluster/candidate rows plus parent queue metadata.
  - Deliverables: candidate readiness rows, selected/denied follow-up proof export, and handoff.
  - Stop condition: if candidate-level source-symbolic proof is still missing, keep source/code readiness blocked.

## Validation commands

- `python -m pytest tests/reverse/test_re359_platform_frontend_service_post_frontend_display_menu_next_subcluster_selection.py -q`
- `python scripts/reverse/re359_platform_frontend_service_post_frontend_display_menu_next_subcluster_selection.py --repo .`
- `python -m pytest tests/reverse -q`
