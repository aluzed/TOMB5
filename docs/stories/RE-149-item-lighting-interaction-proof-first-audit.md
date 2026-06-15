# RE-149 — Item lighting interaction proof-first audit

Status: Done

## Goal

Open `item-lighting-interaction` after the prior module-game handoff as a metadata-only proof-first audit.

## Progress tracker

- [x] RE-148 object-interaction handoff consumed.
- [x] RE-061 item-lighting-interaction rows selected.
- [x] DoFlameTorch item-lighting pivot selected.
- [x] Readiness and blockers recorded.
- [x] RE-150..RE-156 ticket plan emitted.

## Generated artifacts

- `docs/reverse/generated/re149-item-lighting-interaction-proof-first-audit.csv`
- `docs/reverse/generated/re149-item-lighting-interaction-clusters.csv`
- `docs/reverse/generated/re149-item-lighting-interaction-ticket-plan.csv`
- `docs/reverse/functions/re149-item-lighting-interaction-proof-first-audit.md`

## Readiness decision

- decision: `proof-first-audit-blocked`
- code change readiness: `blocked`
- marker readiness: `blocked`
- next ticket: `RE-150`
- blocker: `Item lighting interaction state contract and symbolic equivalence proof missing`

## Follow-up ticket breakdown

- `RE-150` — `item-lighting-interaction-caller-side-effect-map`: Map item-lighting callers, torch item transitions, dynamic-light triggers, and side-effect surfaces.
- `RE-151` — `item-lighting-interaction-argument-state-taxonomy`: Classify item-lighting argument shapes, Lara torch state, item state, alert-light color fields, and dynamic-light side effects.
- `RE-152` — `item-lighting-interaction-comparison-gate`: Decide if item-lighting-interaction has enough non-raw equivalence proof for any source or marker change.
- `RE-153` — `item-lighting-interaction-reconstruction-plan`: Publish a source reconstruction plan if the proof gate remains blocked.
- `RE-154` — `item-lighting-interaction-source-patch-gate`: Keep source patch denied unless the comparison gate produces a symbolic equivalence proof.
- `RE-155` — `item-lighting-interaction-validation-regression`: Validate generated item-lighting metadata and forbidden-evidence guards.
- `RE-156` — `item-lighting-interaction-closure-or-handoff`: Close item-lighting-interaction or hand off to the next module-game cluster with a refreshed plan.

## Validation

- `python3 -m pytest tests/reverse/test_re149_item_lighting_interaction_audit.py -q`
- `python3 -m pytest tests/reverse -q`
- metadata-only guard over RE-149 artifacts
