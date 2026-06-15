# RE-165 — UI text rendering argument taxonomy

Status: Done

## Goal

Classify the `PrintString` and `GetStringLength` callsite families from RE-164 into stable metadata categories without authorizing source or marker changes.

## Progress tracker

- [x] RE-164 callsite map consumed.
- [x] UI text argument taxonomy emitted.
- [x] Source-backed callsite-only proof propagated.
- [x] Forbidden evidence excluded from generated artifacts.

## Generated artifacts

- `docs/reverse/generated/re165-ui-text-rendering-argument-taxonomy.csv`
- `docs/reverse/functions/re165-ui-text-rendering-argument-taxonomy.md`

## Readiness decision

- decision: `argument-taxonomy-blocked`
- code change readiness: `blocked`
- marker readiness: `blocked`
- next ticket: `RE-166`
- blocker: `missing-ui-text-rendering-state-contract-and-symbolic-equivalence-proof`

## Follow-up breakdown

- `RE-166`: document font buffers, string tables, scale state, draw queues, and bounds-output contracts.
- `RE-167`: use the state contract to run the non-raw equivalence/readiness gate.
- `RE-168`: only consider source or marker changes if RE-167 marks rows ready.

## Validation

- `python3 -m pytest tests/reverse/test_re165_ui_text_rendering_argument_taxonomy.py -q`
- `python3 -m pytest tests/reverse -q`
- metadata-only guard over RE-165 artifacts
