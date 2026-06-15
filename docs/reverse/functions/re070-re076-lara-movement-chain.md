# RE-070..RE-076 — Lara movement chain

Domain: `module-game`
Cluster: `lara-movement-support`
Subcluster: `ledge-and-vault-tests`
Status: `lara-movement-chain-closed-with-proof-blocker`
Decision: `documentation-only-terminal-blocker`
Next ticket: `RE-077`

## Progress tracker

- [x] RE-069 ticket plan consumed.
- [x] RE-070 caller and side-effect map published.
- [x] RE-071 argument/state taxonomy published.
- [x] RE-072 comparison gate evaluated.
- [x] RE-073 reconstruction plan reduced to documentation-only blocker.
- [x] RE-074 source patch gate denied safely.
- [x] RE-075 validation/regression metadata recorded.
- [x] RE-076 closure/handoff recorded.

## Readiness

- code-change-ready rows: `0`
- marker-ready rows: `0`
- source-patch-ready rows: `0`
- terminal blocker: `missing non-raw binary equivalence proof`

## Scope rows

- `TestLaraSlide` — `implemented-source` / `source-contract-visible` / blocker `missing-non-raw-binary-equivalence`
- `LaraHangLeftCornerTest` — `unimplemented-stub` / `source-body-missing` / blocker `missing-non-raw-binary-equivalence`
- `LaraHangRightCornerTest` — `unimplemented-stub` / `source-body-missing` / blocker `missing-non-raw-binary-equivalence`
- `LaraTestClimbStance` — `implemented-source` / `source-contract-visible` / blocker `missing-non-raw-binary-equivalence`
- `TestLaraVault` — `implemented-source` / `source-contract-visible` / blocker `missing-non-raw-binary-equivalence`
- `LaraClimbLeftCornerTest` — `unimplemented-stub` / `source-body-missing` / blocker `missing-non-raw-binary-equivalence`
- `LaraClimbRightCornerTest` — `implemented-source` / `source-contract-visible` / blocker `missing-non-raw-binary-equivalence`
- `LaraTestClimb` — `implemented-source` / `source-contract-visible` / blocker `missing-non-raw-binary-equivalence`
- `LaraTestWaterClimbOut` — `implemented-source` / `source-contract-visible` / blocker `missing-non-raw-binary-equivalence`

## Argument shapes

- `shape-item-coll-predicate` — sites `39`, patch-ready `no`, blocker `missing-non-raw-binary-equivalence`
- `shape-movement-predicate` — sites `2`, patch-ready `no`, blocker `missing-non-raw-binary-equivalence`

## Handoff

- next ticket: `RE-077`
- next cluster: `gameflow-runtime-control`
- reason: `initial-subcluster-terminal-blocker`

No production source or proof marker change is made by this chain.
