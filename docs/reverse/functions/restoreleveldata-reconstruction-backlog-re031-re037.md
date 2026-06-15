# RestoreLevelData reconstruction backlog RE-031..RE-037

Status: Generated
Stories: `docs/stories/RE-031` through `docs/stories/RE-037`

## Progress tracker

- [x] Input artifacts loaded.
- [x] Metadata-only decisions published.
- [x] Source patch readiness evaluated.
- [x] Forbidden raw evidence excluded.

## Summary

- status: `restoreleveldata-reconstruction-backlog-blocked`
- patch scope decision: `documentation-only-no-source-patch`
- tickets covered: `7`
- code-change-ready tickets: `0`

## Ticket matrix

### RE-031 — Limited RestoreLevelData reconstruction scope

- topic: `limited-restoreleveldata-reconstruction-scope`
- depends on: `RE-027, RE-030`
- target save groups: `4, 5, 8, 10`
- blockers: `anim-state byte-vs-word restore predicate;split restore groups 4+5; item_flags[0..3] payload bodies;timer payload body;trigger_flags payload body;object-extension field identity; subtype/extra byte predicate;layout block 20;room/rotation ordering;item data word;item flag payload bodies; room byte order/layout predicate`
- decision: `exclude-blocked-groups-from-source-scope`
- safe next action: `publish explicit ready/blocked/excluded scope before any source patch`
- code change readiness: `blocked`
- next ticket: `RE-032`

### RE-032 — RestoreLevelData group 10 room byte order/layout predicate

- topic: `group10-room-byte-order-layout-predicate`
- depends on: `RE-024, RE-027, RE-031`
- target save groups: `10`
- blockers: `room byte order/layout predicate`
- decision: `group10-remains-blocked-until-room-placement-proof`
- safe next action: `prove room byte placement/order as metadata-only rows before source reconstruction`
- code change readiness: `blocked`
- next ticket: `RE-033`

### RE-033 — RestoreLevelData group 4 active-item split restore predicates

- topic: `group4-active-item-split-restore-predicates`
- depends on: `RE-024, RE-027, RE-031`
- target save groups: `4`
- blockers: `anim-state byte-vs-word restore predicate; split restore groups 4+5`
- decision: `group4-remains-blocked-by-split-and-width-predicate`
- safe next action: `prove active-item split restore groups and anim-state width before source reconstruction`
- code change readiness: `blocked`
- next ticket: `RE-034`

### RE-034 — Non-raw RestoreLevelData assignment identity method

- topic: `non-raw-restore-assignment-identity-method`
- depends on: `RE-030, RE-031`
- target save groups: `5`
- blockers: `restore target names absent; source restore body unavailable; raw-evidence publication forbidden`
- decision: `method-defined-but-no-identities-recovered`
- safe next action: `allow only symbolic field names, counts, statuses, and dependency labels in assignment proofs`
- code change readiness: `blocked`
- next ticket: `RE-035`

### RE-035 — RestoreLevelData group 5 safe assignment identity retry

- topic: `group5-safe-assignment-identity-retry`
- depends on: `RE-028, RE-029, RE-030, RE-034`
- target save groups: `5`
- blockers: `packed-status-flags assignment identity; item_flags[0..3] assignment identity and body order; timer assignment identity; trigger_flags assignment identity; object-extension target fields and assignment order`
- decision: `group5-still-excluded-from-source-scope`
- safe next action: `retry only if RE-034 can name assignments without raw evidence leakage`
- code change readiness: `blocked`
- next ticket: `RE-036`

### RE-036 — RestoreLevelData group 8 subtype/layout/fanout readiness

- topic: `group8-subtype-layout-fanout-readiness`
- depends on: `RE-026, RE-031, RE-035`
- target save groups: `8`
- blockers: `subtype extra byte; position layout block; room rotation ordering; speed fallspeed; item data word; item_flags[3,0,1]; anim state payload; group5 item flag payload dependency`
- decision: `group8-remains-blocked-by-fanout-layout-and-group5-dependency`
- safe next action: `prove subtype fanout and layout field identities after group5 dependency is resolved or excluded`
- code change readiness: `blocked`
- next ticket: `RE-037`

### RE-037 — RestoreLevelData partial patch readiness matrix

- topic: `partial-patch-readiness-matrix`
- depends on: `RE-031, RE-032, RE-033, RE-035, RE-036`
- target save groups: `4, 5, 8, 10`
- blockers: `no target save group has code-change-ready evidence; source RestoreLevelData patch remains unsafe`
- decision: `no-partial-patch-ready`
- safe next action: `defer RE-038 source patch until at least one proof row becomes code-change-ready`
- code change readiness: `blocked`
- next ticket: `RE-038`

## Verdict

Do not patch `GAME/SAVEGAME.C` from this backlog. No RE-031..RE-037 ticket makes a code-change-ready claim; all outputs are documentation/proof scope only.

Recommended next ticket: RE-038 — source patch only after a later proof row becomes code-change-ready; otherwise continue proof-first blocker reduction.
