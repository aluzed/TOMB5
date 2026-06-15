# RE-035 — RestoreLevelData group 5 safe assignment identity retry

Status: Done

## Goal

Publish a metadata-only decision for `group5-safe-assignment-identity-retry` without source patch claims or raw reverse-engineering evidence.

## Scope

- depends on: `RE-028, RE-029, RE-030, RE-034`
- target save groups: `5`
- safety contract: `metadata-only; no raw opcodes; no machine words; no payload coordinates; no branch or call targets; no copied dump records`

## Progress

- [x] Input artifacts loaded.
- [x] Metadata-only decision published.
- [x] Source patch readiness evaluated.
- [x] Forbidden raw evidence excluded.

## Findings

- blocker: `packed-status-flags assignment identity`
- blocker: `item_flags[0..3] assignment identity and body order`
- blocker: `timer assignment identity`
- blocker: `trigger_flags assignment identity`
- blocker: `object-extension target fields and assignment order`

## Readiness decision

- decision: `group5-still-excluded-from-source-scope`
- safe next action: `retry only if RE-034 can name assignments without raw evidence leakage`
- code change readiness: `blocked`

Do not patch `GAME/SAVEGAME.C` or add `(F)`, `(D)`, or `(**)` markers from this story alone.

## Validation

- `pytest tests/reverse/test_restoreleveldata_reconstruction_backlog.py -q`
- metadata-only guard over generated/story outputs

## Next step

RE-036: continue proof-first blocker reduction before any source reconstruction.
