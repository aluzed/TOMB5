# RE-154 — Item lighting interaction source patch gate

Status: Done

## Goal

Advance `item-lighting-interaction` using metadata-only evidence for RE-154.

## Progress tracker

- [x] RE-151 taxonomy consumed.
- [x] Item-lighting comparison gate evaluated.
- [x] Patch and marker readiness checked.
- [x] Forbidden evidence excluded from generated artifacts.

## Generated artifacts

- `docs/reverse/generated/re152-re156-item-lighting-interaction-chain.csv`
- `docs/reverse/generated/re152-item-lighting-interaction-comparison-gate.csv`
- `docs/reverse/generated/re153-item-lighting-interaction-reconstruction-plan.csv`
- `docs/reverse/generated/re156-item-lighting-interaction-handoff.csv`
- `docs/reverse/functions/re152-re156-item-lighting-interaction-chain.md`

## Findings

- item-lighting rows remain blocked by missing item lighting state contract and symbolic equivalence proof
- no production source or proof marker patch is admitted by this chain
- continue current item-lighting closure chain

## Follow-up ticket breakdown

- `RE-157` — `ui-text-support` — Open proof-first audit for InitFont and the ui-text-support cluster. Deliverable: `scope CSV, story, and bounded ticket plan`; dependency: `RE-156 handoff`; stop: `audit published or blocker recorded`.
- `RE-158` — `ui-text-support` — Map InitFont callers, marker status, and text/font state surfaces. Deliverable: `source-backed callsite and side-effect map`; dependency: `RE-157 audit`; stop: `metadata-only map published`.
- `RE-159` — `ui-text-support` — Classify InitFont arguments, global text state, and marker proof needs. Deliverable: `argument/state taxonomy`; dependency: `RE-158 callsite map`; stop: `taxonomy published with readiness rows`.
- `RE-160` — `ui-text-support` — Decide whether InitFont has enough non-raw equivalence proof for marker or source changes. Deliverable: `comparison gate`; dependency: `RE-159 taxonomy`; stop: `patch-ready rows or explicit blocker`.
- `RE-161` — `ui-text-support` — Close ui-text-support or hand off to the next module-game backlog domain. Deliverable: `closure or next-domain handoff`; dependency: `RE-160 comparison gate`; stop: `handoff recorded`.

## Readiness decision

- decision: `source-patch-denied`
- code change readiness: `blocked`
- next ticket: `RE-155`

Do not patch production source or add/remove proof markers from this story alone.

## Validation

- `python3 -m pytest tests/reverse/test_re152_re156_item_lighting_chain.py -q`
- `python3 -m pytest tests/reverse -q`
- metadata-only guard over generated RE-152..RE-156 artifacts
