# RE-033 — RestoreLevelData group 4 active-item split restore predicates

Status: Done

## Goal

Publish a metadata-only decision for `group4-active-item-split-restore-predicates` without source patch claims or raw reverse-engineering evidence.

## Scope

- depends on: `RE-024, RE-027, RE-031`
- target save groups: `4`
- safety contract: `metadata-only; no raw opcodes; no machine words; no payload coordinates; no branch or call targets; no copied dump records`

## Progress

- [x] Input artifacts loaded.
- [x] Metadata-only decision published.
- [x] Source patch readiness evaluated.
- [x] Forbidden raw evidence excluded.

## Findings

- blocker: `anim-state byte-vs-word restore predicate`
- blocker: `split restore groups 4+5`

## Readiness decision

- decision: `group4-remains-blocked-by-split-and-width-predicate`
- safe next action: `prove active-item split restore groups and anim-state width before source reconstruction`
- code change readiness: `blocked`

Do not patch `GAME/SAVEGAME.C` or add `(F)`, `(D)`, or `(**)` markers from this story alone.

## Validation

- `pytest tests/reverse/test_restoreleveldata_reconstruction_backlog.py -q`
- metadata-only guard over generated/story outputs

## Next step

RE-034: continue proof-first blocker reduction before any source reconstruction.
