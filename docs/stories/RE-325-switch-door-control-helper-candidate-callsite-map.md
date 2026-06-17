# RE-325 switch-door-control helper candidate callsite map

## Goal

Build a source-backed metadata-only callsite map for candidate `8d1fc6fc3cfc` using RE-324 context rows.

## Inputs

- Upstream handoff: `docs/reverse/generated/re324-switch-door-control-helper-candidate-proof-handoff.csv`
- Candidate context rows: `docs/reverse/generated/re324-switch-door-control-helper-candidate-proof-contexts.csv`
- Source files referenced by the context rows.

## Progress tracker

- [x] RE-324 callsite-map handoff validated.
- [x] Caller context function set verified fail-closed.
- [x] Function spans and source-backed callsite line metadata emitted.
- [x] Raw line text and local reverse identity omitted from generated artifacts.
- [x] Callsite readiness gate follow-up selected.

## Generated artifacts

- `docs/reverse/generated/re325-switch-door-control-helper-candidate-callsite-functions.csv`
- `docs/reverse/generated/re325-switch-door-control-helper-candidate-callsite-map.csv`
- `docs/reverse/generated/re325-switch-door-control-helper-candidate-callsite-gate.csv`
- `docs/reverse/generated/re325-switch-door-control-helper-candidate-callsite-summary.csv`
- `docs/reverse/generated/re325-switch-door-control-helper-candidate-callsite-handoff.csv`
- `docs/reverse/functions/re325-switch-door-control-helper-candidate-callsite-map.md`

## Findings

- Source context functions: `22`
- Source-backed callsite rows: `39`
- Implemented context functions: `7`
- Stub context functions: `13`
- No-callsite context functions: `2`
- Candidate-level proof rows: `0`
- Ready to reopen domain selection: `0`
- Source patch authorized rows: `0`

## Readiness decision

The callsite map is source-backed and metadata-ready, but it is not yet a proof-domain decision. Domain and pivot stay `none`; code readiness remains blocked.

## Follow-up ticket breakdown

- `RE-326` / `switch-door-control-helper-callsite-readiness-gate`: gate the source-backed callsite map and decide whether any callsite family can become a proof pivot.
  - Inputs: RE-325 function/callsite/gate rows.
  - Deliverables: readiness gate rows, selected or denied pivot, handoff for either source-patch denial or remaining candidate deferral.
  - Stop condition: if implemented source callsites still do not prove candidate-level behavior, keep source/code readiness blocked.

## Validation commands

- `python -m pytest tests/reverse/test_re325_switch_door_control_helper_candidate_callsite_map.py -q`
- `python scripts/reverse/re325_switch_door_control_helper_candidate_callsite_map.py --repo .`
- `python -m pytest tests/reverse -q`
