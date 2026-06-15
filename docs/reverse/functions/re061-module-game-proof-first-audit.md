# RE-061 — Module-game proof-first audit

Domain: `module-game`
Pivot: `ShatterObject`
Status: `module-game-proof-first-audit-published`
Decision: `module-game-domain-scoped-for-proof-chain`
Code-change readiness: `blocked`
Recommended next ticket: `RE-062`

## Progress tracker

- [x] RE-060 handoff loaded.
- [x] RE-044 module-game row consumed.
- [x] Module-game candidates classified.
- [x] Proof-first blockers recorded.
- [x] Forbidden raw evidence excluded.

## Summary

- candidates: `52`
- mapped candidates: `52`
- ND candidates: `3`
- runtime-focus candidates: `14`
- clusters: `7`
- Selected initial cluster: `debris-object-breakage`
- code-change-ready candidates: `0`
- marker-ready candidates: `0`

## Cluster shortlist

- `debris-object-breakage`
  - candidates: `2`; mapped: `2`; ND: `0`; runtime: `0`
  - top: `ShatterObject`
  - representative functions: `ShatterObject; TriggerDebris`
  - readiness: `best-initial-proof-cluster`
  - blocker: ShatterObject/TriggerDebris side effects and callers need metadata-only proof before source or marker changes
  - recommended next ticket: `RE-062`
- `lara-movement-support`
  - candidates: `18`; mapped: `18`; ND: `0`; runtime: `1`
  - top: `TestLaraSlide`
  - representative functions: `TestLaraSlide; TestLaraVault; CreateFlare; LaraHangRightCornerTest; LaraHangLeftCornerTest`
  - readiness: `proof-needed`
  - blocker: cluster needs source-level contract and non-raw binary equivalence proof
  - recommended next ticket: `defer`
- `gameflow-runtime-control`
  - candidates: `12`; mapped: `12`; ND: `2`; runtime: `3`
  - top: `DoTitle`
  - representative functions: `DoTitle; LaraControl; QuickControlPhase; DoGameflow; FlameTorchControl`
  - readiness: `nd-marker-audit-later`
  - blocker: ND marker rows require dedicated behavior proof after the initial module-game cluster
  - recommended next ticket: `after-RE-062`
- `gameplay-mixed`
  - candidates: `11`; mapped: `11`; ND: `0`; runtime: `6`
  - top: `Load_and_Init_Cutseq`
  - representative functions: `Load_and_Init_Cutseq; CreateZone; special4_init; init_water_table; InitialiseSqrtTable`
  - readiness: `proof-needed`
  - blocker: cluster needs source-level contract and non-raw binary equivalence proof
  - recommended next ticket: `defer`
- `object-interaction`
  - candidates: `6`; mapped: `6`; ND: `0`; runtime: `4`
  - top: `FindPlinth`
  - representative functions: `FindPlinth; CollectCarriedItems; BaddyObjects; InitialiseObjects; TrapObjects`
  - readiness: `proof-needed`
  - blocker: cluster needs source-level contract and non-raw binary equivalence proof
  - recommended next ticket: `defer`
- `item-lighting-interaction`
  - candidates: `2`; mapped: `2`; ND: `0`; runtime: `0`
  - top: `DoFlameTorch`
  - representative functions: `DoFlameTorch; TriggerAlertLight`
  - readiness: `proof-needed`
  - blocker: cluster needs source-level contract and non-raw binary equivalence proof
  - recommended next ticket: `defer`
- `ui-text-support`
  - candidates: `1`; mapped: `1`; ND: `1`; runtime: `0`
  - top: `InitFont`
  - representative functions: `InitFont`
  - readiness: `nd-marker-audit-later`
  - blocker: ND marker rows require dedicated behavior proof after the initial module-game cluster
  - recommended next ticket: `after-RE-062`

## Multi-ticket plan

- `RE-062` `debris-object-breakage-caller-side-effect-map`
  - goal: Map ShatterObject/TriggerDebris callers, callees, globals, and side-effect surfaces as metadata only.
  - scope: `debris-object-breakage initial cluster`
  - readiness: `blocked-until-proof`
  - exit: caller/side-effect matrix published or terminal proof blocker recorded
- `RE-063` `debris-object-breakage-argument-data-taxonomy`
  - goal: Classify source-level argument shapes, structure fields, object/item dependencies, and write targets for the selected cluster.
  - scope: `ShatterObject/TriggerDebris source contract`
  - readiness: `blocked-until-proof`
  - exit: taxonomy distinguishes source-backed fields from candidate-only fields
- `RE-064` `debris-object-breakage-comparison-gate`
  - goal: Decide whether non-raw binary/source equivalence evidence is sufficient for any source or marker change.
  - scope: `comparison readiness gate`
  - readiness: `blocked-until-proof`
  - exit: patch-ready rows identified or explicit no-patch blocker published
- `RE-065` `debris-object-breakage-reconstruction-plan`
  - goal: Convert any ready rows into a minimal reconstruction plan with tests, guards, and rollback boundaries.
  - scope: `only rows admitted by RE-064`
  - readiness: `blocked-until-proof`
  - exit: source patch plan exists or chain remains documentation-only
- `RE-066` `debris-object-breakage-source-patch-gate`
  - goal: Apply the smallest safe source/marker patch only if RE-064/RE-065 made rows patch-ready; otherwise publish the denial gate.
  - scope: `conditional source patch gate`
  - readiness: `blocked-until-proof`
  - exit: patch validated or no-source-change decision recorded
- `RE-067` `debris-object-breakage-validation-regression`
  - goal: Run build/tests/guards for the selected cluster and record exact validation status.
  - scope: `validation and regression evidence`
  - readiness: `blocked-until-proof`
  - exit: validation log published with pass/fail and remaining blockers
- `RE-068` `module-game-closure-or-next-cluster-handoff`
  - goal: Close the initial module-game cluster or hand off to the next best module-game cluster with a refreshed plan.
  - scope: `closure and reprioritization`
  - readiness: `blocked-until-proof`
  - exit: domain closure, next-cluster handoff, or terminal blocker recorded

## Readiness decision

RE-061 is a proof-first audit gate. It selects `debris-object-breakage` as the first module-game cluster because `ShatterObject` is the RE-044 top module-game candidate and `TriggerDebris` gives a compact adjacent support row. No source patch or completion-marker change is safe until a caller/side-effect map and non-raw equivalence proof exist.

## Generated artifacts

- `docs/reverse/generated/re061-module-game-proof-first-audit.csv`
- `docs/reverse/generated/re061-module-game-clusters.csv`
- `docs/reverse/generated/re061-module-game-ticket-plan.csv`
- `docs/reverse/functions/re061-module-game-proof-first-audit.md`

## Next step

RE-062: build the debris/object-breakage caller and side-effect map for `ShatterObject`/`TriggerDebris` before any source reconstruction or marker update.
