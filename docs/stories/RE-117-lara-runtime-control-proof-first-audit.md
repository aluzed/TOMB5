# RE-117 — Lara runtime control proof-first audit

Status: Done

## Goal

Open `lara-runtime-control` after the RE-116 scripted-runtime handoff as a metadata-only proof-first audit.

## Progress tracker

- [x] RE-116 handoff consumed.
- [x] Lara runtime pivot selected.
- [x] Readiness and blockers recorded.
- [x] Follow-up ticket plan published.

## Readiness decision

- decision: `proof-first-audit-blocked`
- code change readiness: `blocked`
- next ticket: `RE-118`

## Validation

- `python3 -m pytest tests/reverse/test_re117_lara_runtime_audit.py -q`
- `python3 -m pytest tests/reverse -q`
- metadata-only guard over RE-117 artifacts
