# RE-036 — RestoreLevelData group 8 subtype/layout/fanout readiness

Status: Done

## Goal

Publish a metadata-only decision for `group8-subtype-layout-fanout-readiness` without source patch claims or raw reverse-engineering evidence.

## Scope

- depends on: `RE-026, RE-031, RE-035`
- target save groups: `8`
- safety contract: `metadata-only; no raw opcodes; no machine words; no payload coordinates; no branch or call targets; no copied dump records`

## Progress

- [x] Input artifacts loaded.
- [x] Metadata-only decision published.
- [x] Source patch readiness evaluated.
- [x] Forbidden raw evidence excluded.

## Findings

- blocker: `subtype extra byte`
- blocker: `position layout block`
- blocker: `room rotation ordering`
- blocker: `speed fallspeed`
- blocker: `item data word`
- blocker: `item_flags[3,0,1]`
- blocker: `anim state payload`
- blocker: `group5 item flag payload dependency`

## Readiness decision

- decision: `group8-remains-blocked-by-fanout-layout-and-group5-dependency`
- safe next action: `prove subtype fanout and layout field identities after group5 dependency is resolved or excluded`
- code change readiness: `blocked`

Do not patch `GAME/SAVEGAME.C` or add `(F)`, `(D)`, or `(**)` markers from this story alone.

## Validation

- `pytest tests/reverse/test_restoreleveldata_reconstruction_backlog.py -q`
- metadata-only guard over generated/story outputs

## Next step

RE-037: continue proof-first blocker reduction before any source reconstruction.
