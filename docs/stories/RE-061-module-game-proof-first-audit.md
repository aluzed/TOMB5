# RE-061 — Module-game proof-first audit

Status: Done

## Goal

Open the module-game reconstruction chain after the collision handoff by scoping a metadata-only proof-first audit.

## Scope

- depends on: `RE-060`, `RE-044`
- source priority input: `docs/reverse/generated/function-priority.csv`
- upstream handoff input: `docs/reverse/generated/re053-re060-collision-chain.csv`
- upstream domain gate: `docs/reverse/generated/re044-domain-reprioritization.csv`
- safety contract: `metadata-only; no opcodes; no machine words; no payload coordinates; no branch or call targets; no copied dump records; no raw addresses in generated outputs`

## Progress

- [x] RE-060 handoff loaded.
- [x] RE-044 module-game row consumed.
- [x] Module-game candidates classified.
- [x] Proof-first blockers recorded.
- [x] Forbidden raw evidence excluded.

## Generated artifacts

- `docs/reverse/generated/re061-module-game-proof-first-audit.csv`
- `docs/reverse/generated/re061-module-game-clusters.csv`
- `docs/reverse/generated/re061-module-game-ticket-plan.csv`
- `docs/reverse/functions/re061-module-game-proof-first-audit.md`

## Findings

- module-game candidates: `52`
- selected initial cluster: `debris-object-breakage`
- pivot function: `ShatterObject`
- code-change-ready candidates: `0`
- marker-ready candidates: `0`

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

- decision: `module-game-domain-scoped-for-proof-chain`
- safe next action: `open RE-062 debris/object-breakage caller and side-effect map`
- code change readiness: `blocked`
- next ticket: `RE-062`

Do not patch production source or add `(F)`, `(D)`, or `(**)` markers from this story alone.

## Validation

- `python3 -m pytest tests/reverse/test_re061_module_game_audit.py -q`
- metadata-only guard over RE-061 outputs

## Next step

RE-062: build a metadata-only caller/side-effect map for `ShatterObject` and `TriggerDebris` before any source reconstruction or marker update.
