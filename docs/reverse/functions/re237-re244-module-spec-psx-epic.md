# RE-237..RE-244 module-spec_psx epic

Domain: `module-spec_psx`
Pivot: `main`
Outcome: `documentation-only-terminal-blocker`
Blocker: `missing-module-spec-psx-source-contract-and-non-raw-equivalence-proof`
Candidates closed/documented: `12` / `12`
Runtime-focused rows: `4`

## Progress tracker

- [x] RE-236 handoff consumed.
- [x] Proof-first audit emitted.
- [x] Lifecycle, frontend/loadsave, and memory subclusters documented.
- [x] Runtime/cross-platform reconciliation and patch gates denied with zero ready rows.
- [x] Next proof domain selected from the remaining ranked backlog.

## Subcluster closures

- `RE-238` `platform-main-lifecycle`: 3 candidate(s), top `main`, outcome `blocked-no-patch`.
- `RE-239` `frontend-loadsave-flow`: 5 candidate(s), top `S_PlayFMV`, outcome `blocked-no-patch`.
- `RE-240` `platform-memory`: 4 candidate(s), top `game_malloc`, outcome `blocked-no-patch`.

## Terminal decision

This is a documentation-only terminal blocker for module-spec_psx. No production source or marker change is authorized.

## Next domain

Next proof domain: `lara-combat`
Selected pivot: `DoProperDetection`
Recommended next ticket: `RE-245`
