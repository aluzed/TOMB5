# RE-157 — UI text support proof-first audit

Status: Done

## Goal

Open `ui-text-support` after the prior module-game handoff as a metadata-only proof-first audit.

## Progress tracker

- [x] RE-156 item-lighting handoff consumed.
- [x] RE-061 ui-text-support row selected.
- [x] InitFont UI text pivot selected.
- [x] Readiness and blockers recorded.
- [x] RE-158..RE-161 ticket plan emitted.

## Generated artifacts

- `docs/reverse/generated/re157-ui-text-support-proof-first-audit.csv`
- `docs/reverse/generated/re157-ui-text-support-clusters.csv`
- `docs/reverse/generated/re157-ui-text-support-ticket-plan.csv`
- `docs/reverse/functions/re157-ui-text-support-proof-first-audit.md`

## Readiness decision

- decision: `proof-first-audit-blocked`
- code change readiness: `blocked`
- marker readiness: `blocked`
- next ticket: `RE-158`
- blocker: `InitFont ND marker needs behavior proof before marker or source changes`

## Follow-up ticket breakdown

- `RE-158` — `ui-text-support-caller-side-effect-map`: Map InitFont callers, marker status, and text/font state surfaces.
- `RE-159` — `ui-text-support-argument-state-taxonomy`: Classify InitFont arguments, global font shade state, and marker proof needs.
- `RE-160` — `ui-text-support-comparison-gate`: Decide whether InitFont has enough non-raw equivalence proof for marker or source changes.
- `RE-161` — `ui-text-support-closure-or-handoff`: Close ui-text-support or hand off to the next module-game backlog domain.

## Validation

- `python3 -m pytest tests/reverse/test_re157_ui_text_support_audit.py -q`
- `python3 -m pytest tests/reverse -q`
- metadata-only guard over RE-157 artifacts
