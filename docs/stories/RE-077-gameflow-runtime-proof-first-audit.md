# RE-077 — Gameflow runtime proof-first audit

Status: Done

## Goal

Open the next module-game proof chain from the RE-076 handoff by scoping the gameflow runtime control cluster.

## Scope

- depends on: `RE-076`, `RE-061`
- upstream handoff input: `docs/reverse/generated/re076-lara-movement-handoff.csv`
- upstream candidate input: `docs/reverse/generated/re061-module-game-proof-first-audit.csv`
- safety contract: `metadata-only symbolic classifications; forbidden raw evidence excluded`

## Progress tracker

- [x] RE-076 handoff consumed.
- [x] RE-061 gameflow runtime candidates loaded.
- [x] Gameflow runtime subclusters classified.
- [x] ND marker blockers recorded.
- [x] Follow-up ticket plan published.
- [x] Forbidden raw evidence excluded.

## Generated artifacts

- `docs/reverse/generated/re077-gameflow-runtime-proof-first-audit.csv`
- `docs/reverse/generated/re077-gameflow-runtime-subclusters.csv`
- `docs/reverse/generated/re077-gameflow-runtime-ticket-plan.csv`
- `docs/reverse/functions/re077-gameflow-runtime-proof-first-audit.md`

## Findings

- selected cluster: `gameflow-runtime-control`
- selected subcluster: `title-and-control-phase`
- pivot function: `DoTitle`
- candidates: `12`
- ND candidates: `2`
- code-change-ready candidates: `0`
- marker-ready candidates: `0`

## Multi-ticket plan

- `RE-078` `gameflow-runtime-caller-side-effect-map`
  - goal: Map DoTitle/QuickControlPhase/DoGameflow callers, callees, globals, and runtime side-effect surfaces.
  - scope: `title-and-control-phase initial subcluster`
  - readiness: `blocked-until-proof`
  - exit: caller/side-effect matrix published or terminal proof blocker recorded
- `RE-079` `gameflow-runtime-argument-state-taxonomy`
  - goal: Classify gameflow runtime arguments, global state dependencies, mode transitions, and write targets.
  - scope: `selected gameflow runtime source contract`
  - readiness: `blocked-until-proof`
  - exit: taxonomy separates source-backed state from candidate-only state
- `RE-080` `gameflow-runtime-comparison-gate`
  - goal: Decide whether non-raw binary/source equivalence evidence is sufficient for any source or marker change.
  - scope: `comparison readiness gate`
  - readiness: `blocked-until-proof`
  - exit: patch-ready rows identified or explicit no-patch blocker published
- `RE-081` `gameflow-runtime-reconstruction-plan`
  - goal: Convert ready rows into a minimal reconstruction plan with tests, guards, and rollback boundaries.
  - scope: `only rows admitted by RE-080`
  - readiness: `blocked-until-proof`
  - exit: source patch plan exists or chain remains documentation-only
- `RE-082` `gameflow-runtime-source-patch-gate`
  - goal: Apply the smallest safe source/marker patch only if RE-080/RE-081 made rows patch-ready; otherwise publish denial gate.
  - scope: `conditional source patch gate`
  - readiness: `blocked-until-proof`
  - exit: patch validated or no-source-change decision recorded
- `RE-083` `gameflow-runtime-validation-regression`
  - goal: Run build/tests/guards for the selected runtime subcluster and record validation status.
  - scope: `validation and regression evidence`
  - readiness: `blocked-until-proof`
  - exit: validation log published with pass/fail and remaining blockers
- `RE-084` `gameflow-runtime-closure-or-handoff`
  - goal: Close the gameflow runtime subcluster or hand off to the next module-game cluster with a refreshed plan.
  - scope: `closure and reprioritization`
  - readiness: `blocked-until-proof`
  - exit: domain closure, next-subcluster handoff, or terminal blocker recorded

## Readiness decision

- decision: `gameflow-runtime-cluster-scoped-for-proof-chain`
- code change readiness: `blocked`
- next ticket: `RE-078`

Do not patch production source or add/remove proof markers from this story alone.

## Validation

- `python3 -m pytest tests/reverse/test_re077_gameflow_runtime_audit.py -q`
- `python3 -m pytest tests/reverse -q`
- metadata-only guard over generated RE-077 artifacts
