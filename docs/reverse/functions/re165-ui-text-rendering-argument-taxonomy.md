# RE-165 — UI text rendering argument taxonomy

Cluster: `ui-text-rendering`
Decision: `argument-taxonomy-blocked`
Next: `RE-166`

## Progress tracker

- [x] RE-164 callsite map consumed.
- [x] UI text argument taxonomy emitted.
- [x] Upstream source-backed readiness propagated fail-closed.
- [x] Patch and marker readiness kept blocked.

## Summary

- source-backed callsites consumed: `88`
- taxonomy families: `20`
- source patch authorized: `no`

## Families

- `ui-text-printstring-caller-layout-literal-colour-inline-control-string-center`: `PrintString` count `8` text `inline-control-string` flag `center-alignment-flags` patch `no`
- `ui-text-printstring-caller-layout-literal-colour-inline-control-string-none`: `PrintString` count `2` text `inline-control-string` flag `no-alignment-flags` patch `no`
- `ui-text-printstring-caller-layout-literal-colour-string-wad-center`: `PrintString` count `1` text `string-wad-offset` flag `center-alignment-flags` patch `no`
- `ui-text-printstring-caller-layout-literal-colour-string-wad-none`: `PrintString` count `10` text `string-wad-offset` flag `no-alignment-flags` patch `no`
- `ui-text-printstring-caller-layout-literal-colour-string-wad-right`: `PrintString` count `5` text `string-wad-offset` flag `right-alignment-flags` patch `no`
- `ui-text-printstring-caller-layout-request-colour-string-wad-center`: `PrintString` count `1` text `string-wad-offset` flag `center-alignment-flags` patch `no`
- `ui-text-printstring-caller-layout-request-colour-string-wad-none`: `PrintString` count `1` text `string-wad-offset` flag `no-alignment-flags` patch `no`
- `ui-text-printstring-caller-layout-request-colour-string-wad-right`: `PrintString` count `1` text `string-wad-offset` flag `right-alignment-flags` patch `no`
- `ui-text-printstring-literal-coordinate-literal-colour-formatted-buffer-none`: `PrintString` count `2` text `formatted-buffer` flag `no-alignment-flags` patch `no`
- `ui-text-printstring-literal-coordinate-literal-colour-string-wad-center`: `PrintString` count `2` text `string-wad-offset` flag `center-alignment-flags` patch `no`
- `ui-text-printstring-literal-coordinate-literal-colour-string-wad-right`: `PrintString` count `2` text `string-wad-offset` flag `right-alignment-flags` patch `no`
- `ui-text-printstring-screen-centered-literal-colour-formatted-buffer-blink-composite`: `PrintString` count `1` text `formatted-buffer` flag `blink-or-composite-flags` patch `no`
- `ui-text-printstring-screen-centered-literal-colour-formatted-buffer-caller-provided`: `PrintString` count `2` text `formatted-buffer` flag `caller-provided-flags` patch `no`
- `ui-text-printstring-screen-centered-literal-colour-formatted-buffer-right`: `PrintString` count `5` text `formatted-buffer` flag `right-alignment-flags` patch `no`
- `ui-text-printstring-screen-centered-literal-colour-string-wad-blink-composite`: `PrintString` count `2` text `string-wad-offset` flag `blink-or-composite-flags` patch `no`
- `ui-text-printstring-screen-centered-literal-colour-string-wad-center`: `PrintString` count `36` text `string-wad-offset` flag `center-alignment-flags` patch `no`
- `ui-text-printstring-screen-centered-request-colour-string-wad-center`: `PrintString` count `1` text `string-wad-offset` flag `center-alignment-flags` patch `no`
- `ui-text-getstringlength-caller-string-optional-bound`: `GetStringLength` count `1` text `caller-string-pointer` flag `not-applicable` patch `no`
- `ui-text-getstringlength-caller-string-with-bounds`: `GetStringLength` count `4` text `caller-string-or-string-wad` flag `not-applicable` patch `no`
- `ui-text-getstringlength-string-wad-optional-bound`: `GetStringLength` count `1` text `string-wad-offset` flag `not-applicable` patch `no`

No production source or marker change is authorized by this taxonomy.
