# RE-199..RE-205 platform-memory epic

status: `platform-memory-epic-closed-with-proof-blocker`
final decision: `documentation-only-terminal-blocker`
source-patch-ready rows: `0`
marker-ready rows: `0`
next ticket: `RE-206`
next cluster: `platform-main-lifecycle` / `main`

## Scope
- `game_malloc` — source-scope-inventory-only; blocker `missing-platform-memory-caller-state-and-non-raw-equivalence-proof`
- `init_game_malloc` — source-scope-inventory-only; blocker `missing-platform-memory-caller-state-and-non-raw-equivalence-proof`
- `game_free` — source-scope-inventory-only; blocker `missing-platform-memory-caller-state-and-non-raw-equivalence-proof`

## Gate result
No source or marker patch is authorized because the non-raw binary equivalence proof is still missing.
