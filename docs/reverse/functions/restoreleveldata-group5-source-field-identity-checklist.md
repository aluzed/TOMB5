# RestoreLevelData group 5 source-field identity checklist

Status: Generated
Story: `docs/stories/RE-028-restoreleveldata-group5-source-field-identity-checklist.md`

## Progress tracker

- [x] Select save group `5` as the highest-value blocked family from RE-027.
- [x] Load RE-025 payload predicate metadata.
- [x] Load RE-017 field-width reconciliation metadata for save group `5`.
- [x] Inspect current source text only for named field/predicate presence.
- [x] Publish required source-field identity evidence per payload family.
- [x] Keep all rows blocked until restore assignment identity and source write bodies exist.
- [x] Keep raw opcode text, machine words, payload coordinates, addresses, and branch/call targets out of versioned outputs.

## Inputs

- RE-025 payload CSV: `docs/reverse/generated/restoreleveldata-group5-payload-predicate-proof.csv`
- RE-017 field-width CSV: `docs/reverse/generated/saveleveldata-item-field-width-audit.csv`
- Source file inspected: `GAME/SAVEGAME.C`

## Summary

- source inputs: `RE-017, RE-025, GAME/SAVEGAME.C`
- target save group: `5`
- restore group: `6`
- checklist rows: `5`
- patch-ready checklist rows: `0`
- status: `restoreleveldata-group5-source-field-identity-checklist-blocked`

## Checklist rows

### packed-status-flags

- field-width summary: `exact-field-width-match=1;bytes=4`
- source identity state: `source-backed packed word; payload cluster anchor only`
- restore identity state: `restore group 6 has compact branch/payload anchor but no versioned assignment identity`
- required evidence: `restore packed-word assignment map; proof that following payload bodies are independent`
- current blocker: `packed status word exists, but it is only an anchor for this payload cluster`
- checklist status: `anchor-only`
- safe next action: `do not patch; use packed flags only as an anchor while proving dependent payload bodies`
- code change readiness: `blocked`
- recommended next ticket: `RE-029`

### item_flags[0..3]

- field-width summary: `source-missing-field=4;bytes=8`
- source identity state: `header predicates present; separate payload writes absent`
- restore identity state: `restore group 6 has compact branch/payload anchor but no versioned assignment identity`
- required evidence: `four source write sites; four restore assignments; body order predicate`
- current blocker: `item flag header bits do not prove the four item flag payload words or restore body order`
- checklist status: `payload-body-identity-missing`
- safe next action: `do not patch; prove item_flags[0..3] payload bodies from source identity first`
- code change readiness: `blocked`
- recommended next ticket: `RE-029`

### timer

- field-width summary: `source-missing-field=1;bytes=2`
- source identity state: `header predicate present; separate payload write absent`
- restore identity state: `restore group 6 has compact branch/payload anchor but no versioned assignment identity`
- required evidence: `source write site; restore assignment; timer predicate identity`
- current blocker: `timer header bit does not prove a separate timer payload body or restore assignment`
- checklist status: `payload-body-identity-missing`
- safe next action: `do not patch; prove timer payload body and restore assignment from source identity first`
- code change readiness: `blocked`
- recommended next ticket: `RE-029`

### trigger_flags

- field-width summary: `source-missing-field=1;bytes=2`
- source identity state: `header predicate present; separate payload write absent`
- restore identity state: `restore group 6 has compact branch/payload anchor but no versioned assignment identity`
- required evidence: `source write site; restore assignment; trigger_flags predicate identity`
- current blocker: `trigger_flags header bit does not prove a separate trigger_flags payload body or restore assignment`
- checklist status: `payload-body-identity-missing`
- safe next action: `do not patch; prove trigger_flags payload body and restore assignment from source identity first`
- code change readiness: `blocked`
- recommended next ticket: `RE-029`

### object-extension

- field-width summary: `source-missing-field=8;bytes=56;rare-blocks=24,20`
- source identity state: `no named source field identities for object-specific short/block payloads`
- restore identity state: `restore group 6 has compact branch/payload anchor but no versioned assignment identity`
- required evidence: `object predicate map; named source fields for short/24-byte/20-byte payloads; restore assignment order`
- current blocker: `object-specific short and block payloads lack source field identity and object predicate mapping`
- checklist status: `source-field-identity-missing`
- safe next action: `do not patch; map object-specific predicates and fields before reconstruction scope`
- code change readiness: `blocked`
- recommended next ticket: `RE-029`

## Verdict

RE-028 defines the source-field identity checklist for the save group `5` payload cluster. The packed status word is only an anchor. The item flag, timer, trigger flag, and object-extension bodies still lack enough source write and restore assignment identity for a source reconstruction patch.

Do not add `(F)`, `(D)`, or `(**)` markers; do not patch `GAME/SAVEGAME.C` from this checklist alone.

Recommended next ticket: RE-029 — prove one group 5 payload-body family end-to-end, starting with `item_flags[0..3]` if source identities can be recovered without publishing raw dump payloads.
