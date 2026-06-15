# RE-040 — RestoreLevelData group 4 terminal blocker

Status: Done

## Goal

Publish the terminal metadata-only decision for `group4-terminal-blocker`.

## Scope

- depends on: `RE-033, RE-038`
- target save groups: `4`
- safety contract: `metadata-only; symbolic blocker labels only; no opcodes; no machine words; no payload coordinates; no branch or call targets; no copied dump records`

## Progress

- [x] Input artifacts loaded.
- [x] Terminal decision published.
- [x] Source patch rejected or deferred.
- [x] Forbidden raw evidence excluded.

## Findings

- blocker: `anim-state byte-vs-word restore predicate`
- blocker: `split restore groups 4+5`

## Terminal decision

- decision: `terminal-blocked-without-new-non-raw-evidence`
- safe next action: `pause group 4 until split active-item and anim width proofs exist`
- code change readiness: `blocked`

Do not patch `GAME/SAVEGAME.C` or add `(F)`, `(D)`, or `(**)` markers from this story.

## Validation

- `pytest tests/reverse/test_restoreleveldata_terminal_closure.py -q`
- metadata-only guard over terminal closure outputs

## Next step

RE-041: continue terminal closure sequencing.
