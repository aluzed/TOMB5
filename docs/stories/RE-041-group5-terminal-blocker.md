# RE-041 — RestoreLevelData group 5 terminal blocker

Status: Done

## Goal

Publish the terminal metadata-only decision for `group5-terminal-blocker`.

## Scope

- depends on: `RE-035, RE-038`
- target save groups: `5`
- safety contract: `metadata-only; symbolic blocker labels only; no opcodes; no machine words; no payload coordinates; no branch or call targets; no copied dump records`

## Progress

- [x] Input artifacts loaded.
- [x] Terminal decision published.
- [x] Source patch rejected or deferred.
- [x] Forbidden raw evidence excluded.

## Findings

- blocker: `packed-status-flags assignment identity`
- blocker: `item_flags[0..3] assignment identity and body order`
- blocker: `timer assignment identity`
- blocker: `trigger_flags assignment identity`
- blocker: `object-extension target fields and assignment order`

## Terminal decision

- decision: `terminal-excluded-no-assignment-identities`
- safe next action: `keep group 5 excluded unless future evidence names restore assignments safely`
- code change readiness: `blocked`

Do not patch `GAME/SAVEGAME.C` or add `(F)`, `(D)`, or `(**)` markers from this story.

## Validation

- `pytest tests/reverse/test_restoreleveldata_terminal_closure.py -q`
- metadata-only guard over terminal closure outputs

## Next step

RE-042: continue terminal closure sequencing.
