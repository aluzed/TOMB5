# RE-053..RE-060 — Collision chain closure

Domain: `collision`
Pivot: `GetCollisionInfo`
Status: `collision-chain-terminal-no-safe-marker-or-source-patch`
Final decision: `handoff-to-module-game-domain`
code-change-ready tickets: `0`
marker-ready tickets: `0`
source-patch-ready tickets: `0`
Recommended next ticket: `RE-061`

## Progress tracker

- [x] RE-053 domain scope published.
- [x] RE-054 caller map published.
- [x] RE-055 argument/data taxonomy published.
- [x] RE-056 comparison gate blocked source/marker changes.
- [x] RE-057 cluster proof stayed metadata-only.
- [x] RE-058 marker/source patch gate denied changes.
- [x] RE-059 terminal blocker published.
- [x] RE-060 next-domain handoff selected module-game.

## Summary

- collision candidates: `31`
- GetCollisionInfo mapped rows: `1`
- GetCollisionInfo callers classified: `19`
- GetCollisionInfo callees counted: `7`
- source callsites classified by shape: `22`
- argument shapes: `4`
- selected proof cluster: `lara-movement-collision`

## Tickets

- `RE-053` `collision-domain-scope`
  - decision: `getcollisioninfo-selected-as-pivot`
  - readiness: `blocked`
  - next: `RE-054`
- `RE-054` `getcollisioninfo-caller-map`
  - decision: `caller-clusters-published`
  - readiness: `blocked`
  - next: `RE-055`
- `RE-055` `collision-argument-data-taxonomy`
  - decision: `argument-and-data-shapes-published`
  - readiness: `blocked`
  - next: `RE-056`
- `RE-056` `collision-comparison-gate`
  - decision: `blocked-by-missing-non-raw-binary-equivalence-proof`
  - readiness: `blocked`
  - next: `RE-057`
- `RE-057` `collision-proof-cluster`
  - decision: `selected-cluster-remains-proof-needed`
  - readiness: `blocked`
  - next: `RE-058`
- `RE-058` `collision-marker-source-patch-gate`
  - decision: `no-safe-marker-or-source-patch`
  - readiness: `blocked`
  - next: `RE-059`
- `RE-059` `collision-terminal-blocker`
  - decision: `terminal-blocked-without-new-non-raw-equivalence-proof`
  - readiness: `blocked`
  - next: `RE-060`
- `RE-060` `collision-closure-next-domain-handoff`
  - decision: `handoff-to-module-game-domain`
  - readiness: `blocked`
  - next: `RE-061`

## Caller clusters

- `lara-movement-collision`
  - callers: `18`; functions: `18`; readiness: `best-initial-cluster`
  - blocker: movement collision side effects still need non-raw equivalence proof
- `gameplay-mixed`
  - callers: `1`; functions: `1`; readiness: `proof-needed`
  - blocker: caller intent and collision side effects are not proven against binary evidence

## Terminal decision

No production source patch and no `(F)`, `(D)`, or `(**)` marker is safe from the current evidence. The next useful chain is `module-game`, starting at RE-061, because RE-044 ranked it as the highest remaining candidate after the closed audio/effects and collision chains.
