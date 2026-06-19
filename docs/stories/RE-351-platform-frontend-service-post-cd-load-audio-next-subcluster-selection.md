# RE-351 platform/frontend service post cd/load/audio next subcluster selection

## Goal

Consume the RE-350 cd/load/audio queue exhaustion and select the next deferred platform/frontend service subcluster from the parent queue.

## Inputs

- Exhausted selected-subcluster handoff: `docs/reverse/generated/re350-cd-load-audio-service-next-candidate-callsite-readiness-handoff.csv`
- Parent selection handoff: `docs/reverse/generated/re343-ghidra-platform-frontend-service-narrow-handoff.csv`
- Parent subcluster queue: `docs/reverse/generated/re343-ghidra-platform-frontend-service-narrow-subclusters.csv`
- Candidate metadata: `docs/reverse/generated/re343-ghidra-platform-frontend-service-narrow-candidates.csv`

## Progress tracker

- [x] RE-350 cd/load/audio queue exhaustion validated.
- [x] Parent platform/frontend service subcluster queue verified fail-closed.
- [x] Closed subclusters excluded: `cd-load-audio-service`.
- [x] Next deferred subcluster selected: `frontend-display-menu-service`.
- [x] Readiness gate handoff emitted for `RE-352`.

## Generated artifacts

- `docs/reverse/generated/re351-platform-frontend-service-post-cd-load-audio-next-subcluster-selection-subclusters.csv`
- `docs/reverse/generated/re351-platform-frontend-service-post-cd-load-audio-next-subcluster-selection-candidates.csv`
- `docs/reverse/generated/re351-platform-frontend-service-post-cd-load-audio-next-subcluster-selection-summary.csv`
- `docs/reverse/generated/re351-platform-frontend-service-post-cd-load-audio-next-subcluster-selection-handoff.csv`
- `docs/reverse/functions/re351-platform-frontend-service-post-cd-load-audio-next-subcluster-selection.md`

## Findings

- Parent scope: `platform-frontend-service-cluster`
- Closed subclusters: `cd-load-audio-service`
- Input subclusters: `4`
- Remaining deferred subclusters: `3`
- Selected subcluster: `frontend-display-menu-service`
- Selected candidates: `de919274685f;4c90c6af8f9d`
- Ready to reopen domain selection: `0`
- Source patch authorized rows: `0`

## Readiness decision

The selected frontend display/menu subcluster is only ready for a readiness gate. Domain and pivot stay `none`; source/code readiness remains `blocked`.

## Follow-up ticket breakdown

- `RE-352` / `frontend-display-menu-service-readiness-gate`: gate candidates `de919274685f;4c90c6af8f9d` before any proof-domain selection.
  - Inputs: RE-351 selected subcluster/candidate rows plus parent queue metadata.
  - Deliverables: candidate readiness rows, selected/denied follow-up proof export, and handoff.
  - Stop condition: if candidate-level source-symbolic proof is still missing, keep source/code readiness blocked.

## Validation commands

- `python -m pytest tests/reverse/test_re351_platform_frontend_service_post_cd_load_audio_next_subcluster_selection.py -q`
- `python scripts/reverse/re351_platform_frontend_service_post_cd_load_audio_next_subcluster_selection.py --repo .`
- `python -m pytest tests/reverse -q`
