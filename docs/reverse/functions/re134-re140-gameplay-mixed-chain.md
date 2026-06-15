# RE-134..RE-140 — Gameplay mixed chain

Domain: `module-game`
Cluster: `gameplay-mixed`
Subcluster: `gameplay-mixed`
Status: `gameplay-mixed-chain-closed-with-proof-blocker`
Decision: `documentation-only-terminal-blocker`
Next ticket: `RE-141`

## Progress tracker

- [x] RE-133 ticket plan consumed.
- [x] RE-134 caller and side-effect map published.
- [x] RE-135 argument/state taxonomy published.
- [x] RE-136 comparison gate evaluated.
- [x] RE-137 reconstruction plan reduced to documentation-only blocker.
- [x] RE-138 source patch gate denied safely.
- [x] RE-139 validation/regression metadata recorded.
- [x] RE-140 closure/handoff recorded.

## Readiness

- code-change-ready rows: `0`
- marker-ready rows: `0`
- source-patch-ready rows: `0`
- terminal blocker: `missing gameplay mixed state contract and symbolic equivalence proof`
- source line numbers in generated maps are source-navigation metadata only.

## Scope rows

- `Load_and_Init_Cutseq` — `implemented-source` / `platform-gated-source-needs-equivalence-proof` / patch-ready `no` / blocker `missing-gameplay-mixed-state-contract-and-symbolic-equivalence-proof`
- `CreateZone` — `unimplemented-stub` / `source-body-missing` / patch-ready `no` / blocker `missing-gameplay-mixed-state-contract-and-symbolic-equivalence-proof`
- `special4_init` — `implemented-source` / `platform-gated-source-needs-equivalence-proof` / patch-ready `no` / blocker `missing-gameplay-mixed-state-contract-and-symbolic-equivalence-proof`
- `init_water_table` — `platform-gated-source` / `platform-gated-source-needs-equivalence-proof` / patch-ready `no` / blocker `missing-gameplay-mixed-state-contract-and-symbolic-equivalence-proof`
- `InitialiseSqrtTable` — `implemented-source` / `platform-gated-source-needs-equivalence-proof` / patch-ready `no` / blocker `missing-gameplay-mixed-state-contract-and-symbolic-equivalence-proof`
- `InitTarget` — `implemented-source` / `platform-gated-source-needs-equivalence-proof` / patch-ready `no` / blocker `missing-gameplay-mixed-state-contract-and-symbolic-equivalence-proof`
- `InitBinoculars` — `implemented-source` / `platform-gated-source-needs-equivalence-proof` / patch-ready `no` / blocker `missing-gameplay-mixed-state-contract-and-symbolic-equivalence-proof`
- `InitialiseFootPrints` — `implemented-source` / `platform-gated-source-needs-equivalence-proof` / patch-ready `no` / blocker `missing-gameplay-mixed-state-contract-and-symbolic-equivalence-proof`
- `LoadLevel` — `unimplemented-stub` / `source-body-missing` / patch-ready `no` / blocker `missing-gameplay-mixed-state-contract-and-symbolic-equivalence-proof`
- `EscapeBox` — `implemented-source` / `platform-gated-source-needs-equivalence-proof` / patch-ready `no` / blocker `missing-gameplay-mixed-state-contract-and-symbolic-equivalence-proof`
- `InitPackNodes` — `implemented-source` / `platform-gated-source-needs-equivalence-proof` / patch-ready `no` / blocker `missing-gameplay-mixed-state-contract-and-symbolic-equivalence-proof`

## Argument/state shapes

- `shape-gameplay-mixed-1-arg` — sites `12`, source-backed `yes`, patch-ready `no`, blocker `missing-symbolic-equivalence-proof`
- `shape-gameplay-mixed-cutseq-number` — sites `5`, source-backed `yes`, patch-ready `no`, blocker `missing-symbolic-equivalence-proof`
- `shape-gameplay-mixed-void-setup` — sites `5`, source-backed `yes`, patch-ready `no`, blocker `missing-symbolic-equivalence-proof`
- `shape-gameplay-mixed-item-pointer` — sites `2`, source-backed `yes`, patch-ready `no`, blocker `missing-symbolic-equivalence-proof`

## Handoff

- next ticket: `RE-141`
- next subcluster: `object-interaction`
- reason: `gameplay-mixed closed with proof blocker; next RE-061 module-game cluster is object-interaction with FindPlinth pivot`

No production source or proof marker change is made by this chain.
