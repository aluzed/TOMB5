# RestoreLevelData group 5 restore assignment identity map

Status: Generated
Story: `docs/stories/RE-030-restoreleveldata-group5-restore-assignment-identity-map.md`

## Progress tracker

- [x] Load RE-028 group 5 source-field checklist.
- [x] Load RE-029 item_flags body proof.
- [x] Load RE-025 payload-family metadata and RE-022 reconciliation status.
- [x] Load RE-019 restore group `6` size context without publishing raw coordinates.
- [x] Inspect current source for `RestoreLevelData` body availability.
- [x] Publish restore assignment identity state per group 5 payload family.
- [x] Keep raw opcode text, machine words, payload coordinates, addresses, and branch/call targets out of versioned outputs.

## Inputs

- RE-028 checklist CSV: `docs/reverse/generated/restoreleveldata-group5-source-field-identity-checklist.csv`
- RE-029 item flags CSV: `docs/reverse/generated/restoreleveldata-group5-item-flags-body-proof.csv`
- RE-025 payload CSV: `docs/reverse/generated/restoreleveldata-group5-payload-predicate-proof.csv`
- RE-019 read map CSV: `docs/reverse/generated/restoreleveldata-read-call-map.csv`
- RE-022 reconciliation CSV: `docs/reverse/generated/restoreleveldata-field-predicate-reconciliation.csv`
- Source file inspected: `GAME/SAVEGAME.C`

## Summary

- source inputs: `RE-019, RE-022, RE-025, RE-028, RE-029, GAME/SAVEGAME.C`
- target save group: `5`
- restore group: `6`
- restore source state: `RestoreLevelData source body is UNIMPLEMENTED`
- group 5 decision: `defer-group5-from-source-reconstruction`
- map rows: `5`
- assignment-identity-ready rows: `0`
- patch-ready rows: `0`
- status: `restoreleveldata-group5-restore-assignment-identity-map-blocked`

## Assignment identity rows

### packed-status-flags

- prior body proof: `source-backed-anchor-only; readiness=blocked`
- restore candidate profile: `restore group 6 compact branch payload cluster; rare anchor widths present`
- restore assignment evidence: `no versioned restore assignment identity; current source restore body absent`
- assignment identity state: `missing-restore-assignment-map`
- required assignment evidence: `named restore assignment for packed status word and independence proof for following payload bodies`
- assignment identity readiness: `blocked`
- code change readiness: `blocked`
- safe next action: `defer group 5 or recover assignment identities before source reconstruction`
- recommended next ticket: `RE-031`

### item_flags[0..3]

- prior body proof: `candidate-width-only; 4 rows; patch-ready=0`
- restore candidate profile: `restore group 6 compact branch payload cluster; rare anchor widths present`
- restore assignment evidence: `no versioned restore assignment identity; current source restore body absent`
- assignment identity state: `missing-restore-assignment-map`
- required assignment evidence: `four named restore assignments; per-flag body order; source/restore field identity`
- assignment identity readiness: `blocked`
- code change readiness: `blocked`
- safe next action: `defer group 5 or recover assignment identities before source reconstruction`
- recommended next ticket: `RE-031`

### timer

- prior body proof: `payload-body-predicate-unproven; readiness=blocked`
- restore candidate profile: `restore group 6 compact branch payload cluster; rare anchor widths present`
- restore assignment evidence: `no versioned restore assignment identity; current source restore body absent`
- assignment identity state: `missing-restore-assignment-map`
- required assignment evidence: `named restore timer assignment and predicate identity`
- assignment identity readiness: `blocked`
- code change readiness: `blocked`
- safe next action: `defer group 5 or recover assignment identities before source reconstruction`
- recommended next ticket: `RE-031`

### trigger_flags

- prior body proof: `payload-body-predicate-unproven; readiness=blocked`
- restore candidate profile: `restore group 6 compact branch payload cluster; rare anchor widths present`
- restore assignment evidence: `no versioned restore assignment identity; current source restore body absent`
- assignment identity state: `missing-restore-assignment-map`
- required assignment evidence: `named restore trigger_flags assignment and predicate identity`
- assignment identity readiness: `blocked`
- code change readiness: `blocked`
- safe next action: `defer group 5 or recover assignment identities before source reconstruction`
- recommended next ticket: `RE-031`

### object-extension

- prior body proof: `object-extension-predicate-unproven; readiness=blocked`
- restore candidate profile: `restore group 6 compact branch payload cluster; rare anchor widths present`
- restore assignment evidence: `no versioned restore assignment identity; current source restore body absent`
- assignment identity state: `missing-restore-assignment-map`
- required assignment evidence: `object-specific restore target fields; object predicate map; block assignment order`
- assignment identity readiness: `blocked`
- code change readiness: `blocked`
- safe next action: `defer group 5 or recover assignment identities before source reconstruction`
- recommended next ticket: `RE-031`

## Verdict

RE-030 does not recover a versionable restore assignment identity map for group `5`. The restore group `6` metadata remains a candidate payload cluster only, and the current `RestoreLevelData` source body is absent. Group `5` should therefore be deferred from source reconstruction scope unless a future proof can name restore target fields without publishing raw dump payloads.

Do not add `(F)`, `(D)`, or `(**)` markers; do not patch `GAME/SAVEGAME.C` from this map alone.

Recommended next ticket: RE-031 — define a limited RestoreLevelData reconstruction scope that explicitly excludes group `5`, or produce a non-raw assignment extraction method that can unlock group `5` safely.
