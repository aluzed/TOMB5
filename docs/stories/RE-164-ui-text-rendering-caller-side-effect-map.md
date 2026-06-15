# RE-164 — UI text rendering caller and side-effect map

Status: Done

## Goal

Map source-backed callers, text sources, flag families, and visible side-effect surfaces for `PrintString` and `GetStringLength` without authorizing source or marker changes.

## Progress tracker

- [x] RE-163 ticket plan consumed.
- [x] UI text rendering callsites mapped.
- [x] Source-backed rows verified against real source lines.
- [x] Forbidden evidence excluded from generated artifacts.

## Generated artifacts

- `docs/reverse/generated/re164-ui-text-rendering-scope.csv`
- `docs/reverse/generated/re164-ui-text-rendering-callsite-map.csv`
- `docs/reverse/functions/re164-ui-text-rendering-caller-side-effect-map.md`

## Readiness decision

- decision: `caller-side-effect-map-blocked`
- code change readiness: `blocked`
- marker readiness: `blocked`
- next ticket: `RE-165`
- blocker: `missing-ui-text-rendering-state-contract-and-symbolic-equivalence-proof`

## Follow-up breakdown

- `RE-165`: classify PrintString argument and flag taxonomy from this callsite map.
- `RE-166`: document font, draw-buffer, scale, and string-table state contracts.
- `RE-167`: run the non-raw equivalence/readiness gate.

## Validation

- `python3 -m pytest tests/reverse/test_re164_ui_text_rendering_callsite_map.py -q`
- `python3 -m pytest tests/reverse -q`
- metadata-only guard over RE-164 artifacts
