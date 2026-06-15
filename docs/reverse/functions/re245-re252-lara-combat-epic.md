# RE-245..RE-252 lara-combat epic

Domain: `lara-combat`
Pivot: `DoProperDetection`
Outcome: `documentation-only-terminal-blocker`
Blocker: `missing-lara-combat-source-contract-and-non-raw-equivalence-proof`
Raw priority rows: `10`
Parser artifacts excluded: `3`
Candidates closed/documented: `7` / `7`

## Progress tracker

- [x] RE-244 handoff consumed.
- [x] Proof-first audit emitted.
- [x] Parser artifacts excluded before function-scope closure.
- [x] Target detection, target acquisition, and weapon fire-control subclusters documented.
- [x] State/equivalence and patch gates denied with zero ready rows.
- [x] Next proof domain selected from the remaining ranked backlog.

## Subcluster closures

- `RE-246` `target-detection`: 2 candidate(s), top `DoProperDetection`, outcome `blocked-no-patch`.
- `RE-247` `target-acquisition`: 3 candidate(s), top `LaraGetNewTarget`, outcome `blocked-no-patch`.
- `RE-248` `weapon-fire-control`: 2 candidate(s), top `FireWeapon`, outcome `blocked-no-patch`.

## Terminal decision

This is a documentation-only terminal blocker for lara-combat. No production source or marker change is authorized.

## Next domain

Next proof domain: `inventory`
Selected pivot: `S_CallInventory2`
Recommended next ticket: `RE-253`
