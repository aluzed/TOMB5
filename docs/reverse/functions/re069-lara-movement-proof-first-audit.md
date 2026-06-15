# RE-069 — Lara movement proof-first audit

Domain: `module-game`
Cluster: `lara-movement-support`
Pivot: `TestLaraSlide`
Status: `lara-movement-proof-first-audit-published`
Decision: `lara-movement-cluster-scoped-for-proof-chain`
Code-change readiness: `blocked`
Recommended next ticket: `RE-070`

## Progress tracker

- [x] RE-068 handoff consumed.
- [x] RE-061 lara movement candidates loaded.
- [x] Lara movement subclusters classified.
- [x] Proof-first blockers recorded.
- [x] Follow-up ticket plan published.
- [x] Forbidden raw evidence excluded.

## Summary

- candidates: `18`
- source-backed candidates: `18`
- runtime-focus candidates: `1`
- subclusters: `4`
- selected subcluster: `ledge-and-vault-tests`
- code-change-ready rows: `0`
- marker-ready rows: `0`

## Subclusters

- `ledge-and-vault-tests` — candidates `9`, top `TestLaraSlide`, readiness `best-initial-proof-subcluster`
- `lara-control-context` — candidates `5`, top `UpdateRopeSwing`, readiness `proof-needed`
- `flare-movement-support` — candidates `2`, top `CreateFlare`, readiness `proof-needed`
- `water-movement-support` — candidates `2`, top `LaraWaterCurrent`, readiness `proof-needed`

## Ticket plan

- `RE-070` `lara-movement-caller-side-effect-map` — Map TestLaraSlide/TestLaraVault/ledge-hang callers, callees, state writes, and predicate surfaces.
- `RE-071` `lara-movement-argument-state-taxonomy` — Classify movement predicate arguments, Lara state fields, item/collision dependencies, and write targets.
- `RE-072` `lara-movement-comparison-gate` — Decide whether non-raw binary/source equivalence evidence is sufficient for any source or marker change.
- `RE-073` `lara-movement-reconstruction-plan` — Convert ready rows into a minimal reconstruction plan with tests, guards, and rollback boundaries.
- `RE-074` `lara-movement-source-patch-gate` — Apply the smallest safe source/marker patch only if RE-072/RE-073 made rows patch-ready; otherwise publish denial gate.
- `RE-075` `lara-movement-validation-regression` — Run build/tests/guards for the selected movement subcluster and record validation status.
- `RE-076` `lara-movement-closure-or-handoff` — Close the lara movement subcluster or hand off to the next module-game cluster with a refreshed plan.

## Readiness decision

- decision: `lara-movement-cluster-scoped-for-proof-chain`
- source/marker patch: `blocked`
- blocker: `caller intent, Lara state writes, and non-raw equivalence proof are not yet established`

No production source or proof marker change is made by this audit.
