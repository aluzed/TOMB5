# RE-261..RE-267 input epic

Domain: `input`
Pivot: `S_UpdateInput`
Outcome: `documentation-only-terminal-blocker`
Blocker: `missing-input-cross-platform-state-contract-and-non-raw-equivalence-proof`
Raw priority rows: `3`
Runtime rows: `2`
Candidates closed/documented: `3` / `3`

## Progress tracker

- [x] RE-260 handoff consumed.
- [x] Proof-first audit emitted.
- [x] Cross-platform input variants scoped separately.
- [x] State/equivalence and patch gates denied with zero ready rows.
- [x] Next proof domain selected from the remaining ranked backlog.

## Subcluster closures

- `RE-262` `psxpc-n-runtime`: 1 candidate(s), top `S_UpdateInput`, outcome `blocked-no-patch`.
- `RE-263` `psx-runtime`: 1 candidate(s), top `S_UpdateInput`, outcome `blocked-no-patch`.
- `RE-264` `psxpc-service`: 1 candidate(s), top `S_UpdateInput`, outcome `blocked-no-patch`.

## Terminal decision

This is a documentation-only terminal blocker for input. No production source or marker change is authorized.

## Next domain

Next proof domain: `camera`
Selected pivot: `CalculateSpotCams`
Recommended next ticket: `RE-268`
