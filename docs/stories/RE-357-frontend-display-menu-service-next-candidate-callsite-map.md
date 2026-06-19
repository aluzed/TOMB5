# RE-357 frontend display/menu service next candidate callsite map

## Goal

Build a source-backed metadata-only callsite map for next candidate `4c90c6af8f9d` using RE-356 context rows.

## Inputs

- Upstream handoff: `docs/reverse/generated/re356-frontend-display-menu-service-next-candidate-proof-handoff.csv`
- Candidate context rows: `docs/reverse/generated/re356-frontend-display-menu-service-next-candidate-proof-contexts.csv`
- Source files referenced by the context rows.

## Progress tracker

- [x] RE-356 next-candidate proof-export handoff validated.
- [x] Caller context function set verified fail-closed.
- [x] Function spans and source-backed callsite line metadata emitted.
- [x] Raw line text and local reverse identity omitted from generated artifacts.
- [x] Next-candidate callsite readiness gate follow-up selected.

## Generated artifacts

- `docs/reverse/generated/re357-frontend-display-menu-service-next-candidate-callsite-functions.csv`
- `docs/reverse/generated/re357-frontend-display-menu-service-next-candidate-callsite-map.csv`
- `docs/reverse/generated/re357-frontend-display-menu-service-next-candidate-callsite-gate.csv`
- `docs/reverse/generated/re357-frontend-display-menu-service-next-candidate-callsite-summary.csv`
- `docs/reverse/generated/re357-frontend-display-menu-service-next-candidate-callsite-handoff.csv`
- `docs/reverse/functions/re357-frontend-display-menu-service-next-candidate-callsite-map.md`

## Findings

- Source context functions: `18`
- Source-backed callsite rows: `126`
- Implemented context functions: `17`
- Stub context functions: `0`
- No-callsite context functions: `1`
- Candidate-level proof rows: `0`
- Ready to reopen domain selection: `0`
- Source patch authorized rows: `0`

## Readiness decision

The next-candidate callsite map is source-backed and metadata-ready, but it is not yet a proof-domain decision. Domain and pivot stay `none`; code readiness remains blocked.

## Follow-up ticket breakdown

- `RE-358` / `frontend-display-menu-service-next-candidate-callsite-readiness-gate`: gate the next-candidate source-backed callsite map and decide whether any frontend display/menu callsite family can become a proof pivot.
  - Inputs: RE-357 function/callsite/gate rows.
  - Deliverables: readiness gate rows, selected or denied pivot, and handoff for either source-patch denial or candidate/subcluster exhaustion.
  - Stop condition: if source-backed callsites still do not prove candidate-level behavior, keep source/code readiness blocked.

## Validation commands

- `python -m pytest tests/reverse/test_re357_frontend_display_menu_service_next_candidate_callsite_map.py -q`
- `python scripts/reverse/re357_frontend_display_menu_service_next_candidate_callsite_map.py --repo .`
- `python -m pytest tests/reverse -q`
