# RE-169 module SPEC_PSXPC_N next-cluster selection

## Progress tracker

- [x] RE-168 no-patch handoff consumed.
- [x] UI text rendering cluster excluded from the remaining cluster shortlist.
- [x] Remaining SPEC_PSXPC_N clusters ranked with metadata-only criteria.
- [x] Next cluster and RE-170 handoff emitted without source or marker changes.

## Decision

- upstream outcome: `ui-text-rendering-source-patch-denied`
- selected next cluster: `geometry-support`
- selected pivot: `GetBoundsAccurate`
- next ticket: `RE-170` `module-spec-psxpc-n-closure-or-handoff`
- code-change readiness: `documentation-only-selection-gate`

No production source or marker change is authorized by this selection gate.

## Ranked remaining clusters

- #1 `geometry-support` / `GetBoundsAccurate`: `selected`; readiness `blocked`; next `RE-170`.
- #2 `frontend-sequence` / `S_PlayFMV`: `deferred-after-selected-cluster`; readiness `blocked`; next `TBD`.
- #3 `frontend-loadsave` / `SaveGame`: `deferred-after-selected-cluster`; readiness `blocked`; next `TBD`.
- #4 `platform-gpu-display` / `clear_a_rect`: `deferred-nd-marker-audit`; readiness `blocked`; next `TBD`.
- #5 `platform-memory` / `game_malloc`: `deferred-nd-marker-audit`; readiness `blocked`; next `TBD`.
- #6 `platform-main-lifecycle` / `main`: `deferred-nd-marker-audit`; readiness `blocked`; next `TBD`.

## Next proof

`RE-170` should use `geometry-support` / `GetBoundsAccurate` to either emit a bounded proof handoff or close the module SPEC_PSXPC_N domain.
