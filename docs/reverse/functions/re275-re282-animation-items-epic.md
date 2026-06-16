# RE-275..RE-282 animation-items epic

## Progress tracker

- [x] RE-274 post-camera handoff consumed.
- [x] Remaining domains reprioritized from source-backed function-priority metadata.
- [x] Animation-items source functions grouped into bounded proof subclusters.
- [x] Equivalence/source-patch/marker gates denied with explicit blocker.

## Decision

- Domain: `animation-items`
- Pivot: `CalcAnimatingItem_ASM`
- Raw priority rows: `31`
- Runtime rows: `3`
- ND rows: `1`
- Outcome: `documentation-only-terminal-blocker` — documentation-only terminal blocker
- Blocker: `missing-animation-item-state-contract-and-non-raw-equivalence-proof`
- Recommended next ticket: `TBD`

No production source or marker change is authorized by this epic.

## Subclusters

- `runtime-reload`: 4 candidates; top `ReloadAnims`; readiness `blocked`.
- `animitem-core`: 4 candidates; top `CalcAnimatingItem_ASM`; readiness `blocked`.
- `matrix-transform`: 21 candidates; top `GetBounds_AI`; readiness `blocked`.
- `texture-object-animation`: 2 candidates; top `AnimateWaterfalls`; readiness `blocked`.

## Next handoff

- Selected domain: `module-spec_pc_n`
- Selected pivot: `if`
- Stop condition: `open a post-animation-items selection/reconciliation gate before source changes`
