# RE-288..RE-290 global function-priority exhaustion epic

## Progress tracker

- [x] RE-287 final domain handoff consumed.
- [x] All function-priority rows classified into closed or proof-blocked domains.
- [x] Parser-artifact keyword rows reconciled globally.
- [x] Final no-next-domain handoff emitted.

## Decision

- Total priority rows: `348`
- Closed/proof-blocked domains: `15`
- Parser artifacts reconciled: `16`
- Remaining candidate rows: `0`
- Outcome: `function-priority-backlog-exhausted`
- Recommended next ticket: `TBD`

No production source or marker change is authorized by this epic.

## Domain coverage

- `maths-render-support`: 92 rows; status `closed-or-proof-blocked`; remaining `0`.
- `module-game`: 54 rows; status `closed-or-proof-blocked`; remaining `0`.
- `collision`: 32 rows; status `closed-or-proof-blocked`; remaining `0`.
- `animation-items`: 31 rows; status `closed-or-proof-blocked`; remaining `0`.
- `module-spec_psxpc`: 28 rows; status `closed-or-proof-blocked`; remaining `0`.
- `module-spec_psxpc_n`: 27 rows; status `closed-or-proof-blocked`; remaining `0`.
- `traps-switches-doors`: 20 rows; status `closed-or-proof-blocked`; remaining `0`.
- `audio-effects`: 19 rows; status `closed-or-proof-blocked`; remaining `0`.
- `module-spec_psx`: 12 rows; status `closed-or-proof-blocked`; remaining `0`.
- `inventory`: 11 rows; status `closed-or-proof-blocked`; remaining `0`.
- `lara-combat`: 10 rows; status `closed-or-proof-blocked`; remaining `0`.
- `camera`: 4 rows; status `closed-or-proof-blocked`; remaining `0`.
- `savegame`: 3 rows; status `closed-or-proof-blocked`; remaining `0`.
- `input`: 3 rows; status `closed-or-proof-blocked`; remaining `0`.
- `module-spec_pc_n`: 2 rows; status `closed-or-proof-blocked`; remaining `0`.

## Handoff

- Next topic: `function-priority-backlog-exhausted`
- Stop condition: `refresh upstream function-priority inputs or add new non-raw proof evidence before opening another epic`
