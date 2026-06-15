# RE-032 — RestoreLevelData group 10 room byte order/layout predicate

Status: Done

## Goal

Publish a metadata-only decision for `group10-room-byte-order-layout-predicate` without source patch claims or raw reverse-engineering evidence.

## Scope

- depends on: `RE-024, RE-027, RE-031`
- target save groups: `10`
- safety contract: `metadata-only; no raw opcodes; no machine words; no payload coordinates; no branch or call targets; no copied dump records`

## Progress

- [x] Input artifacts loaded.
- [x] Metadata-only decision published.
- [x] Source patch readiness evaluated.
- [x] Forbidden raw evidence excluded.

## Findings

- blocker: `room byte order/layout predicate`

## Readiness decision

- decision: `group10-remains-blocked-until-room-placement-proof`
- safe next action: `prove room byte placement/order as metadata-only rows before source reconstruction`
- code change readiness: `blocked`

Do not patch `GAME/SAVEGAME.C` or add `(F)`, `(D)`, or `(**)` markers from this story alone.

## Validation

- `pytest tests/reverse/test_restoreleveldata_reconstruction_backlog.py -q`
- metadata-only guard over generated/story outputs

## Next step

RE-033: continue proof-first blocker reduction before any source reconstruction.
