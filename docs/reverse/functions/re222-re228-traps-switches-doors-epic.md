# RE-222..RE-228 traps-switches-doors epic

Domain: `traps-switches-doors`
Pivot: `ControlRollingBall`
Outcome: `documentation-only-terminal-blocker`
Blocker: `missing-traps-switches-doors-source-contract-and-non-raw-equivalence-proof`
Candidates closed/documented: `20` / `20`

## Progress tracker

- [x] RE-221 handoff consumed.
- [x] Proof-first audit emitted.
- [x] Trap, door, and switch subclusters documented.
- [x] Trigger/state reconciliation and patch gates denied with zero ready rows.
- [x] Next proof domain selected from the remaining ranked backlog.

## Subcluster closures

- `RE-223` `trap-hazard-control`: 11 candidate(s), top `ControlRollingBall`, outcome `blocked-no-patch`.
- `RE-224` `door-control`: 4 candidate(s), top `DoorControl`, outcome `blocked-no-patch`.
- `RE-225` `switch-control`: 5 candidate(s), top `TurnSwitchControl`, outcome `blocked-no-patch`.

## Terminal decision

This is a documentation-only terminal blocker for traps-switches-doors. No production source or marker change is authorized.

## Next domain

Next proof domain: `module-spec_psxpc`
Selected pivot: `PrintString`
Recommended next ticket: `RE-229`
