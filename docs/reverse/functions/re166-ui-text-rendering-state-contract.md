# RE-166 — UI text rendering state contract

Cluster: `ui-text-rendering`
Decision: `state-contract-documented-equivalence-blocked`
Next: `RE-167`

## Progress tracker

- [x] RE-165 taxonomy consumed.
- [x] UI text state contract emitted.
- [x] Source-backed contract surfaces recorded.
- [x] Patch and marker readiness kept blocked.

## Summary

- taxonomy families consumed: `20`
- state contract rows: `9`
- source patch authorized: `no`

## Contract rows

- `ui-text-printstring-scale-flag-lifecycle`: `PrintString` surface `scale-flag-state` status `contract-documented-equivalence-blocked` readiness `no`
- `ui-text-printstring-blink-frame-gate`: `PrintString` surface `blink-frame-counter` status `contract-documented-equivalence-blocked` readiness `no`
- `ui-text-printstring-alignment-bounds-contract`: `PrintString` surface `text-positioning-state` status `contract-documented-equivalence-blocked` readiness `no`
- `ui-text-printstring-glyph-table-contract`: `PrintString` surface `font-glyph-table-state` status `contract-documented-equivalence-blocked` readiness `no`
- `ui-text-getstringlength-scale-read-contract`: `GetStringLength` surface `scale-flag-state` status `contract-documented-equivalence-blocked` readiness `no`
- `ui-text-getstringlength-font-metric-contract`: `GetStringLength` surface `font-metric-state` status `contract-documented-equivalence-blocked` readiness `no`
- `ui-text-getstringlength-bounds-output-contract`: `GetStringLength` surface `optional-bounds-output` status `contract-documented-equivalence-blocked` readiness `no`
- `ui-text-getstringlength-control-character-contract`: `GetStringLength` surface `control-character-state` status `contract-documented-equivalence-blocked` readiness `no`
- `ui-text-drawchar-draw-buffer-contract`: `DrawChar` surface `draw-buffer-state` status `contract-documented-equivalence-blocked` readiness `no`

No production source or marker change is authorized by this state contract.
