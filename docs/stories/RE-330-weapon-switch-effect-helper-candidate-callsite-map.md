# RE-330 weapon-switch-effect helper candidate callsite map

## Goal

Build a source-backed metadata-only callsite map for candidate `1ddbda046e37` using RE-329 context rows.

## Inputs

- Upstream handoff: `docs/reverse/generated/re329-weapon-switch-effect-helper-candidate-proof-handoff.csv`
- Candidate context rows: `docs/reverse/generated/re329-weapon-switch-effect-helper-candidate-proof-contexts.csv`
- Source files referenced by the context rows.

## Progress tracker

- [x] RE-329 callsite-map handoff validated.
- [x] Caller context function set verified fail-closed.
- [x] Function spans and source-backed callsite line metadata emitted.
- [x] Raw line text and local reverse identity omitted from generated artifacts.
- [x] Callsite readiness gate follow-up selected.

## Generated artifacts

- `docs/reverse/generated/re330-weapon-switch-effect-helper-candidate-callsite-functions.csv`
- `docs/reverse/generated/re330-weapon-switch-effect-helper-candidate-callsite-map.csv`
- `docs/reverse/generated/re330-weapon-switch-effect-helper-candidate-callsite-gate.csv`
- `docs/reverse/generated/re330-weapon-switch-effect-helper-candidate-callsite-summary.csv`
- `docs/reverse/generated/re330-weapon-switch-effect-helper-candidate-callsite-handoff.csv`
- `docs/reverse/functions/re330-weapon-switch-effect-helper-candidate-callsite-map.md`

## Findings

- Source context functions: `1`
- Source-backed callsite rows: `1`
- Implemented context functions: `0`
- Stub context functions: `1`
- No-callsite context functions: `0`
- Candidate-level proof rows: `0`
- Ready to reopen domain selection: `0`
- Source patch authorized rows: `0`

## Readiness decision

The callsite map is source-backed and metadata-ready, but it is not yet a proof-domain decision. Domain and pivot stay `none`; code readiness remains blocked.

## Follow-up ticket breakdown

- `RE-331` / `weapon-switch-effect-helper-callsite-readiness-gate`: gate the source-backed callsite map and decide whether any callsite family can become a proof pivot.
  - Inputs: RE-330 function/callsite/gate rows.
  - Deliverables: readiness gate rows, selected or denied pivot, handoff for either source-patch denial or remaining candidate deferral.
  - Stop condition: if implemented source callsites still do not prove candidate-level behavior, keep source/code readiness blocked.

## Validation commands

- `python -m pytest tests/reverse/test_re330_weapon_switch_effect_helper_candidate_callsite_map.py -q`
- `python scripts/reverse/re330_weapon_switch_effect_helper_candidate_callsite_map.py --repo .`
- `python -m pytest tests/reverse -q`
