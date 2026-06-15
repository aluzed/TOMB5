# RE-042 — RestoreLevelData group 8 terminal blocker

Status: Done

## Goal

Publish the terminal metadata-only decision for `group8-terminal-blocker`.

## Scope

- depends on: `RE-036, RE-038, RE-041`
- target save groups: `8`
- safety contract: `metadata-only; symbolic blocker labels only; no opcodes; no machine words; no payload coordinates; no branch or call targets; no copied dump records`

## Progress

- [x] Input artifacts loaded.
- [x] Terminal decision published.
- [x] Source patch rejected or deferred.
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

## Terminal decision

- decision: `terminal-blocked-by-layout-and-group5-dependency`
- safe next action: `pause group 8 until subtype/layout proofs and group 5 dependency are safe`
- code change readiness: `blocked`

Do not patch `GAME/SAVEGAME.C` or add `(F)`, `(D)`, or `(**)` markers from this story.

## Validation

- `pytest tests/reverse/test_restoreleveldata_terminal_closure.py -q`
- metadata-only guard over terminal closure outputs

## Next step

RE-043: continue terminal closure sequencing.
