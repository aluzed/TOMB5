# RE-034 — Non-raw RestoreLevelData assignment identity method

Status: Done

## Goal

Publish a metadata-only decision for `non-raw-restore-assignment-identity-method` without source patch claims or raw reverse-engineering evidence.

## Scope

- depends on: `RE-030, RE-031`
- target save groups: `5`
- safety contract: `metadata-only; no raw opcodes; no machine words; no payload coordinates; no branch or call targets; no copied dump records`

## Progress

- [x] Input artifacts loaded.
- [x] Metadata-only decision published.
- [x] Source patch readiness evaluated.
- [x] Forbidden raw evidence excluded.

## Findings

- blocker: `restore target names absent`
- blocker: `source restore body unavailable`
- blocker: `raw-evidence publication forbidden`

## Readiness decision

- decision: `method-defined-but-no-identities-recovered`
- safe next action: `allow only symbolic field names, counts, statuses, and dependency labels in assignment proofs`
- code change readiness: `blocked`

Do not patch `GAME/SAVEGAME.C` or add `(F)`, `(D)`, or `(**)` markers from this story alone.

## Validation

- `pytest tests/reverse/test_restoreleveldata_reconstruction_backlog.py -q`
- metadata-only guard over generated/story outputs

## Next step

RE-035: continue proof-first blocker reduction before any source reconstruction.
