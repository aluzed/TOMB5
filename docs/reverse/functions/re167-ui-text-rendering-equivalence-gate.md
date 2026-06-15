# RE-167 — UI text rendering equivalence gate

Cluster: `ui-text-rendering`
Decision: `equivalence-gate-blocked-no-ready-rows`
Next: `RE-168`

## Progress tracker

- [x] RE-166 state contract consumed.
- [x] Equivalence readiness matrix emitted.
- [x] Source and marker readiness kept blocked.
- [x] Forbidden evidence excluded from generated artifacts.

## Summary

- contract rows consumed: `9`
- code-change-ready rows: `0`
- marker-ready rows: `0`
- source patch authorized: `no`

## Readiness rows

- `ui-text-printstring-scale-flag-lifecycle`: `PrintString` / `scale-flag-state` / `blocked-missing-ui-text-rendering-non-raw-symbolic-equivalence-proof`
- `ui-text-printstring-blink-frame-gate`: `PrintString` / `blink-frame-counter` / `blocked-missing-ui-text-rendering-non-raw-symbolic-equivalence-proof`
- `ui-text-printstring-alignment-bounds-contract`: `PrintString` / `text-positioning-state` / `blocked-missing-ui-text-rendering-non-raw-symbolic-equivalence-proof`
- `ui-text-printstring-glyph-table-contract`: `PrintString` / `font-glyph-table-state` / `blocked-missing-ui-text-rendering-non-raw-symbolic-equivalence-proof`
- `ui-text-getstringlength-scale-read-contract`: `GetStringLength` / `scale-flag-state` / `blocked-missing-ui-text-rendering-non-raw-symbolic-equivalence-proof`
- `ui-text-getstringlength-font-metric-contract`: `GetStringLength` / `font-metric-state` / `blocked-missing-ui-text-rendering-non-raw-symbolic-equivalence-proof`
- `ui-text-getstringlength-bounds-output-contract`: `GetStringLength` / `optional-bounds-output` / `blocked-missing-ui-text-rendering-non-raw-symbolic-equivalence-proof`
- `ui-text-getstringlength-control-character-contract`: `GetStringLength` / `control-character-state` / `blocked-missing-ui-text-rendering-non-raw-symbolic-equivalence-proof`
- `ui-text-drawchar-draw-buffer-contract`: `DrawChar` / `draw-buffer-state` / `blocked-missing-ui-text-rendering-non-raw-symbolic-equivalence-proof`

No production source or marker change is authorized by this equivalence gate.
