# RE-346 cd-load-audio service candidate callsite map

## Goal

Build a source-backed metadata-only callsite map for candidate `1e35f3f4fb97` using RE-345 context rows.

## Inputs

- Upstream handoff: `docs/reverse/generated/re345-cd-load-audio-service-candidate-proof-handoff.csv`
- Candidate context rows: `docs/reverse/generated/re345-cd-load-audio-service-candidate-proof-contexts.csv`
- Source files referenced by the context rows.

## Progress tracker

- [x] RE-345 proof-export handoff validated.
- [x] Caller context function set verified fail-closed.
- [x] Function spans and source-backed callsite line metadata emitted.
- [x] Raw line text and local reverse identity omitted from generated artifacts.
- [x] Callsite readiness gate follow-up selected.

## Generated artifacts

- `docs/reverse/generated/re346-cd-load-audio-service-candidate-callsite-functions.csv`
- `docs/reverse/generated/re346-cd-load-audio-service-candidate-callsite-map.csv`
- `docs/reverse/generated/re346-cd-load-audio-service-candidate-callsite-gate.csv`
- `docs/reverse/generated/re346-cd-load-audio-service-candidate-callsite-summary.csv`
- `docs/reverse/generated/re346-cd-load-audio-service-candidate-callsite-handoff.csv`
- `docs/reverse/functions/re346-cd-load-audio-service-candidate-callsite-map.md`

## Findings

- Source context functions: `34`
- Source-backed callsite rows: `266`
- Implemented context functions: `32`
- Stub context functions: `0`
- No-callsite context functions: `2`
- Candidate-level proof rows: `0`
- Ready to reopen domain selection: `0`
- Source patch authorized rows: `0`

## Readiness decision

The callsite map is source-backed and metadata-ready, but it is not yet a proof-domain decision. Domain and pivot stay `none`; code readiness remains blocked.

## Follow-up ticket breakdown

- `RE-347` / `cd-load-audio-service-callsite-readiness-gate`: gate the source-backed callsite map and decide whether any cd/load/audio callsite family can become a proof pivot.
  - Inputs: RE-346 function/callsite/gate rows.
  - Deliverables: readiness gate rows, selected or denied pivot, and handoff for either source-patch denial or candidate/subcluster exhaustion.
  - Stop condition: if source-backed callsites still do not prove candidate-level behavior, keep source/code readiness blocked.

## Validation commands

- `python -m pytest tests/reverse/test_re346_cd_load_audio_service_candidate_callsite_map.py -q`
- `python scripts/reverse/re346_cd_load_audio_service_candidate_callsite_map.py --repo .`
- `python -m pytest tests/reverse -q`
