# RE-101 — Pickup search control proof-first audit

Status: Done

## Goal

Open `pickup-search-control` from the RE-100 handoff as a metadata-only proof-first audit.

## Progress tracker

- [x] Upstream handoff verified.
- [x] Pivot and sibling controls selected.
- [x] Readiness and blockers recorded.
- [x] Follow-up ticket plan published.

## Readiness decision

- decision: `proof-first-audit-blocked`
- code change readiness: `blocked`
- next ticket: `RE-102`

## Validation

- `python3 -m pytest tests/reverse/test_re101_pickup_search_audit.py -q`
- `python3 -m pytest tests/reverse -q`
- metadata-only guard over RE-101 artifacts
