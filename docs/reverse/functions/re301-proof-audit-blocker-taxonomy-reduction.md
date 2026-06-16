# RE-301 proof-audit blocker taxonomy reduction

## Progress tracker

- [x] RE-300 proof-audit handoff validated.
- [x] RE-296 proof-audits candidate validated as safe metadata work.
- [x] Proof-audit CSV blockers normalized into reusable metadata classes.
- [x] Evidence rows emitted as fingerprints only, with no blocker text.
- [x] Code/source readiness remains blocked.

## Summary

- Proof CSV files scanned: `34`
- Evidence rows reduced: `384`
- Normalized classes: `8`
- Metadata-ready classes: `8`
- Domain-selection-ready classes: `0`
- Raw/asset sources admitted: `0`

## Taxonomy rows

### source-contract-and-non-raw-equivalence-missing

- Evidence count: `164`
- Proof CSV files: `6`
- Unique blocker fingerprints/classes: `6`
- Description: Proof-audit rows needing source-contract and non-raw equivalence evidence.
- Domain selection ready: `no`

### backlog-context-not-selected

- Evidence count: `82`
- Proof CSV files: `4`
- Unique blocker fingerprints/classes: `6`
- Description: Proof-audit rows retained as backlog/support context rather than selected proof pivots.
- Domain selection ready: `no`

### proof-evidence-missing

- Evidence count: `70`
- Proof CSV files: `12`
- Unique blocker fingerprints/classes: `12`
- Description: Proof-audit rows with generic missing proof or proof-first readiness blockers.
- Domain selection ready: `no`

### state-contract-and-symbolic-equivalence-missing

- Evidence count: `30`
- Proof CSV files: `9`
- Unique blocker fingerprints/classes: `11`
- Description: Rows needing state contracts plus symbolic equivalence proof.
- Domain selection ready: `no`

### generic-proof-audit-blocker

- Evidence count: `23`
- Proof CSV files: `6`
- Unique blocker fingerprints/classes: `2`
- Description: Rows with nonstandard or empty blocker fields reduced to a generic proof-audit class for later gating.
- Domain selection ready: `no`

### marker-behavior-proof-needed

- Evidence count: `13`
- Proof CSV files: `4`
- Unique blocker fingerprints/classes: `5`
- Description: Rows where ND marker or marker changes need behavior proof first.
- Domain selection ready: `no`

### non-raw-equivalence-proof-missing

- Evidence count: `1`
- Proof CSV files: `1`
- Unique blocker fingerprints/classes: `1`
- Description: Rows specifically blocked on missing non-raw equivalence proof.
- Domain selection ready: `no`

### symbolic-equivalence-proof-missing

- Evidence count: `1`
- Proof CSV files: `1`
- Unique blocker fingerprints/classes: `1`
- Description: Rows specifically blocked on symbolic equivalence proof.
- Domain selection ready: `no`

## Readiness

- Metadata work readiness: `ready`
- Code/source readiness: `blocked`
- Next ticket: `RE-302`
- Next topic: `proof-audit-blocker-taxonomy-readiness-gate`
- Selected domain: `none`
- Selected pivot: `none`
- Stop condition: `gate proof-audit taxonomy before proof-domain selection can reopen`

No production source or marker change is authorized by this reduction.
