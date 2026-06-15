# RE-069 — Lara movement proof-first audit

Status: Done

## Goal

Open the next module-game proof chain from the RE-068 handoff by scoping the lara movement support cluster.

## Scope

- depends on: `RE-068`, `RE-061`
- upstream handoff input: `docs/reverse/generated/re068-module-game-handoff.csv`
- upstream candidate input: `docs/reverse/generated/re061-module-game-proof-first-audit.csv`
- safety contract: `metadata-only symbolic classifications; forbidden raw evidence excluded`

## Progress tracker

- [x] RE-068 handoff consumed.
- [x] RE-061 lara movement candidates loaded.
- [x] Lara movement subclusters classified.
- [x] Proof-first blockers recorded.
- [x] Follow-up ticket plan published.
- [x] Forbidden raw evidence excluded.

## Generated artifacts

- `docs/reverse/generated/re069-lara-movement-proof-first-audit.csv`
- `docs/reverse/generated/re069-lara-movement-subclusters.csv`
- `docs/reverse/generated/re069-lara-movement-ticket-plan.csv`
- `docs/reverse/functions/re069-lara-movement-proof-first-audit.md`

## Findings

- selected cluster: `lara-movement-support`
- selected subcluster: `ledge-and-vault-tests`
- pivot function: `TestLaraSlide`
- candidates: `18`
- code-change-ready candidates: `0`
- marker-ready candidates: `0`

## Multi-ticket plan

- `RE-070` `lara-movement-caller-side-effect-map`
  - goal: Map TestLaraSlide/TestLaraVault/ledge-hang callers, callees, state writes, and predicate surfaces.
  - scope: `ledge-and-vault-tests initial subcluster`
  - readiness: `blocked-until-proof`
  - exit: caller/side-effect matrix published or terminal proof blocker recorded
- `RE-071` `lara-movement-argument-state-taxonomy`
  - goal: Classify movement predicate arguments, Lara state fields, item/collision dependencies, and write targets.
  - scope: `selected lara movement source contract`
  - readiness: `blocked-until-proof`
  - exit: taxonomy separates source-backed fields from candidate-only fields
- `RE-072` `lara-movement-comparison-gate`
  - goal: Decide whether non-raw binary/source equivalence evidence is sufficient for any source or marker change.
  - scope: `comparison readiness gate`
  - readiness: `blocked-until-proof`
  - exit: patch-ready rows identified or explicit no-patch blocker published
- `RE-073` `lara-movement-reconstruction-plan`
  - goal: Convert ready rows into a minimal reconstruction plan with tests, guards, and rollback boundaries.
  - scope: `only rows admitted by RE-072`
  - readiness: `blocked-until-proof`
  - exit: source patch plan exists or chain remains documentation-only
- `RE-074` `lara-movement-source-patch-gate`
  - goal: Apply the smallest safe source/marker patch only if RE-072/RE-073 made rows patch-ready; otherwise publish denial gate.
  - scope: `conditional source patch gate`
  - readiness: `blocked-until-proof`
  - exit: patch validated or no-source-change decision recorded
- `RE-075` `lara-movement-validation-regression`
  - goal: Run build/tests/guards for the selected movement subcluster and record validation status.
  - scope: `validation and regression evidence`
  - readiness: `blocked-until-proof`
  - exit: validation log published with pass/fail and remaining blockers
- `RE-076` `lara-movement-closure-or-handoff`
  - goal: Close the lara movement subcluster or hand off to the next module-game cluster with a refreshed plan.
  - scope: `closure and reprioritization`
  - readiness: `blocked-until-proof`
  - exit: domain closure, next-subcluster handoff, or terminal blocker recorded

## Readiness decision

- decision: `lara-movement-cluster-scoped-for-proof-chain`
- code change readiness: `blocked`
- next ticket: `RE-070`

Do not patch production source or add/remove proof markers from this story alone.

## Validation

- `python3 -m pytest tests/reverse/test_re069_lara_movement_audit.py -q`
- `python3 -m pytest tests/reverse -q`
- metadata-only guard over generated RE-069 artifacts
