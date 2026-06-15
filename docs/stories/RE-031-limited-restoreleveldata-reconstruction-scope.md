# RE-031 — Limited RestoreLevelData reconstruction scope

Status: Done

## Goal

Publish a metadata-only decision for `limited-restoreleveldata-reconstruction-scope` without source patch claims or raw reverse-engineering evidence.

## Scope

- depends on: `RE-027, RE-030`
- target save groups: `4, 5, 8, 10`
- safety contract: `metadata-only; no raw opcodes; no machine words; no payload coordinates; no branch or call targets; no copied dump records`

## Progress

- [x] Input artifacts loaded.
- [x] Metadata-only decision published.
- [x] Source patch readiness evaluated.
- [x] Forbidden raw evidence excluded.

## Findings

- blocker: `anim-state byte-vs-word restore predicate;split restore groups 4+5`
- blocker: `item_flags[0..3] payload bodies;timer payload body;trigger_flags payload body;object-extension field identity`
- blocker: `subtype/extra byte predicate;layout block 20;room/rotation ordering;item data word;item flag payload bodies`
- blocker: `room byte order/layout predicate`

## Readiness decision

- decision: `exclude-blocked-groups-from-source-scope`
- safe next action: `publish explicit ready/blocked/excluded scope before any source patch`
- code change readiness: `blocked`

Do not patch `GAME/SAVEGAME.C` or add `(F)`, `(D)`, or `(**)` markers from this story alone.

## Validation

- `pytest tests/reverse/test_restoreleveldata_reconstruction_backlog.py -q`
- metadata-only guard over generated/story outputs

## Next step

RE-032: continue proof-first blocker reduction before any source reconstruction.
