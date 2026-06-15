# RE-166 — UI text rendering state contract

Status: Done

## Goal

Document source-backed state contracts for `PrintString`, `GetStringLength`, and `DrawChar` before the non-raw equivalence gate.

## Progress tracker

- [x] RE-165 taxonomy consumed.
- [x] UI text state contract emitted.
- [x] Draw-buffer, font, string, flag, bounds, and scale surfaces classified.
- [x] Forbidden evidence excluded from generated artifacts.

## Generated artifacts

- `docs/reverse/generated/re166-ui-text-rendering-state-contract.csv`
- `docs/reverse/functions/re166-ui-text-rendering-state-contract.md`

## Readiness decision

- decision: `state-contract-documented-equivalence-blocked`
- code change readiness: `blocked`
- marker readiness: `blocked`
- next ticket: `RE-167`
- blocker: `missing-ui-text-rendering-non-raw-symbolic-equivalence-proof`

## Follow-up breakdown

- `RE-167`: compare these source-backed contracts against non-raw symbolic evidence and emit readiness rows.
- `RE-168`: only consider source or marker changes if RE-167 marks rows ready.
- `RE-169`: select the next SPEC_PSXPC_N cluster after this UI text rendering chain closes or blocks.

## Validation

- `python3 -m pytest tests/reverse/test_re166_ui_text_rendering_state_contract.py -q`
- `python3 -m pytest tests/reverse -q`
- metadata-only guard over RE-166 artifacts

No production source or marker change is authorized by this state contract.
