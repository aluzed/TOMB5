# RE-164 — UI text rendering caller and side-effect map

Cluster: `ui-text-rendering`
Decision: `caller-side-effect-map-blocked`
Next: `RE-165`

## Progress tracker

- [x] RE-163 ticket plan consumed.
- [x] UI text rendering callsites mapped.
- [x] Text-source, flag-source, and visible side-effect categories classified.
- [x] Patch and marker readiness kept blocked.

## Summary

- scoped functions: `PrintString, GetStringLength`
- source-backed callsite rows: `88`
- source patch authorized: `no`

## Findings

- `do_gfx_debug_mode` -> `PrintString` in `SPEC_PSXPC_N/GPU.C`; shape `shape-ui-text-printstring-five-arg`; text `formatted-buffer`; flag `no-alignment-flags`; patch `no`
- `do_gfx_debug_mode` -> `PrintString` in `SPEC_PSXPC_N/GPU.C`; shape `shape-ui-text-printstring-five-arg`; text `formatted-buffer`; flag `no-alignment-flags`; patch `no`
- `DisplayFiles` -> `PrintString` in `SPEC_PSXPC_N/LOADSAVE.C`; shape `shape-ui-text-printstring-five-arg`; text `formatted-buffer`; flag `caller-provided-flags`; patch `no`
- `DisplayFiles` -> `PrintString` in `SPEC_PSXPC_N/LOADSAVE.C`; shape `shape-ui-text-printstring-five-arg`; text `formatted-buffer`; flag `caller-provided-flags`; patch `no`
- `LoadGame` -> `PrintString` in `SPEC_PSXPC_N/LOADSAVE.C`; shape `shape-ui-text-printstring-five-arg`; text `string-wad-offset`; flag `center-alignment-flags`; patch `no`
- `LoadGame` -> `PrintString` in `SPEC_PSXPC_N/LOADSAVE.C`; shape `shape-ui-text-printstring-five-arg`; text `string-wad-offset`; flag `center-alignment-flags`; patch `no`
- `SaveGame` -> `PrintString` in `SPEC_PSXPC_N/LOADSAVE.C`; shape `shape-ui-text-printstring-five-arg`; text `string-wad-offset`; flag `center-alignment-flags`; patch `no`
- `SaveGame` -> `PrintString` in `SPEC_PSXPC_N/LOADSAVE.C`; shape `shape-ui-text-printstring-five-arg`; text `string-wad-offset`; flag `center-alignment-flags`; patch `no`
- `Requester` -> `PrintString` in `SPEC_PSXPC_N/REQUEST.C`; shape `shape-ui-text-printstring-five-arg`; text `string-wad-offset`; flag `center-alignment-flags`; patch `no`
- `Requester` -> `PrintString` in `SPEC_PSXPC_N/REQUEST.C`; shape `shape-ui-text-printstring-five-arg`; text `string-wad-offset`; flag `no-alignment-flags`; patch `no`
- `Requester` -> `PrintString` in `SPEC_PSXPC_N/REQUEST.C`; shape `shape-ui-text-printstring-five-arg`; text `string-wad-offset`; flag `no-alignment-flags`; patch `no`
- `Requester` -> `PrintString` in `SPEC_PSXPC_N/REQUEST.C`; shape `shape-ui-text-printstring-five-arg`; text `string-wad-offset`; flag `right-alignment-flags`; patch `no`
- `Requester` -> `PrintString` in `SPEC_PSXPC_N/REQUEST.C`; shape `shape-ui-text-printstring-five-arg`; text `string-wad-offset`; flag `right-alignment-flags`; patch `no`
- `Requester` -> `PrintString` in `SPEC_PSXPC_N/REQUEST.C`; shape `shape-ui-text-printstring-five-arg`; text `string-wad-offset`; flag `center-alignment-flags`; patch `no`
- `Requester` -> `PrintString` in `SPEC_PSXPC_N/REQUEST.C`; shape `shape-ui-text-printstring-five-arg`; text `string-wad-offset`; flag `center-alignment-flags`; patch `no`
- `Requester` -> `PrintString` in `SPEC_PSXPC_N/REQUEST.C`; shape `shape-ui-text-printstring-five-arg`; text `inline-control-string`; flag `no-alignment-flags`; patch `no`
- `Requester` -> `PrintString` in `SPEC_PSXPC_N/REQUEST.C`; shape `shape-ui-text-printstring-five-arg`; text `inline-control-string`; flag `no-alignment-flags`; patch `no`
- `DisplayConfig` -> `PrintString` in `SPEC_PSXPC_N/SPECIFIC.C`; shape `shape-ui-text-printstring-five-arg`; text `inline-control-string`; flag `center-alignment-flags`; patch `no`
- `DisplayConfig` -> `PrintString` in `SPEC_PSXPC_N/SPECIFIC.C`; shape `shape-ui-text-printstring-five-arg`; text `inline-control-string`; flag `center-alignment-flags`; patch `no`
- `DisplayConfig` -> `PrintString` in `SPEC_PSXPC_N/SPECIFIC.C`; shape `shape-ui-text-printstring-five-arg`; text `inline-control-string`; flag `center-alignment-flags`; patch `no`
- `DisplayConfig` -> `PrintString` in `SPEC_PSXPC_N/SPECIFIC.C`; shape `shape-ui-text-printstring-five-arg`; text `inline-control-string`; flag `center-alignment-flags`; patch `no`
- `DisplayConfig` -> `PrintString` in `SPEC_PSXPC_N/SPECIFIC.C`; shape `shape-ui-text-printstring-five-arg`; text `inline-control-string`; flag `center-alignment-flags`; patch `no`
- `DisplayConfig` -> `PrintString` in `SPEC_PSXPC_N/SPECIFIC.C`; shape `shape-ui-text-printstring-five-arg`; text `inline-control-string`; flag `center-alignment-flags`; patch `no`
- `DisplayConfig` -> `PrintString` in `SPEC_PSXPC_N/SPECIFIC.C`; shape `shape-ui-text-printstring-five-arg`; text `inline-control-string`; flag `center-alignment-flags`; patch `no`
- `DisplayConfig` -> `PrintString` in `SPEC_PSXPC_N/SPECIFIC.C`; shape `shape-ui-text-printstring-five-arg`; text `inline-control-string`; flag `center-alignment-flags`; patch `no`
- `DisplayConfig` -> `PrintString` in `SPEC_PSXPC_N/SPECIFIC.C`; shape `shape-ui-text-printstring-five-arg`; text `string-wad-offset`; flag `no-alignment-flags`; patch `no`
- `DisplayConfig` -> `PrintString` in `SPEC_PSXPC_N/SPECIFIC.C`; shape `shape-ui-text-printstring-five-arg`; text `string-wad-offset`; flag `no-alignment-flags`; patch `no`
- `DisplayConfig` -> `PrintString` in `SPEC_PSXPC_N/SPECIFIC.C`; shape `shape-ui-text-printstring-five-arg`; text `string-wad-offset`; flag `right-alignment-flags`; patch `no`
- `DisplayConfig` -> `PrintString` in `SPEC_PSXPC_N/SPECIFIC.C`; shape `shape-ui-text-printstring-five-arg`; text `string-wad-offset`; flag `right-alignment-flags`; patch `no`
- `DisplayConfig` -> `PrintString` in `SPEC_PSXPC_N/SPECIFIC.C`; shape `shape-ui-text-printstring-five-arg`; text `string-wad-offset`; flag `no-alignment-flags`; patch `no`
- `DisplayConfig` -> `PrintString` in `SPEC_PSXPC_N/SPECIFIC.C`; shape `shape-ui-text-printstring-five-arg`; text `string-wad-offset`; flag `no-alignment-flags`; patch `no`
- `DisplayConfig` -> `PrintString` in `SPEC_PSXPC_N/SPECIFIC.C`; shape `shape-ui-text-printstring-five-arg`; text `string-wad-offset`; flag `right-alignment-flags`; patch `no`
- `DisplayConfig` -> `PrintString` in `SPEC_PSXPC_N/SPECIFIC.C`; shape `shape-ui-text-printstring-five-arg`; text `string-wad-offset`; flag `right-alignment-flags`; patch `no`
- `DisplayConfig` -> `PrintString` in `SPEC_PSXPC_N/SPECIFIC.C`; shape `shape-ui-text-printstring-five-arg`; text `string-wad-offset`; flag `no-alignment-flags`; patch `no`
- `DisplayConfig` -> `PrintString` in `SPEC_PSXPC_N/SPECIFIC.C`; shape `shape-ui-text-printstring-five-arg`; text `string-wad-offset`; flag `no-alignment-flags`; patch `no`
- `DisplayConfig` -> `PrintString` in `SPEC_PSXPC_N/SPECIFIC.C`; shape `shape-ui-text-printstring-five-arg`; text `string-wad-offset`; flag `no-alignment-flags`; patch `no`
- `DisplayConfig` -> `PrintString` in `SPEC_PSXPC_N/SPECIFIC.C`; shape `shape-ui-text-printstring-five-arg`; text `string-wad-offset`; flag `no-alignment-flags`; patch `no`
- `DisplayConfig` -> `PrintString` in `SPEC_PSXPC_N/SPECIFIC.C`; shape `shape-ui-text-printstring-five-arg`; text `string-wad-offset`; flag `no-alignment-flags`; patch `no`
- `DisplayConfig` -> `PrintString` in `SPEC_PSXPC_N/SPECIFIC.C`; shape `shape-ui-text-printstring-five-arg`; text `formatted-buffer`; flag `right-alignment-flags`; patch `no`
- `DisplayConfig` -> `PrintString` in `SPEC_PSXPC_N/SPECIFIC.C`; shape `shape-ui-text-printstring-five-arg`; text `formatted-buffer`; flag `right-alignment-flags`; patch `no`
- `DisplayConfig` -> `PrintString` in `SPEC_PSXPC_N/SPECIFIC.C`; shape `shape-ui-text-printstring-five-arg`; text `formatted-buffer`; flag `right-alignment-flags`; patch `no`
- `DisplayConfig` -> `PrintString` in `SPEC_PSXPC_N/SPECIFIC.C`; shape `shape-ui-text-printstring-five-arg`; text `formatted-buffer`; flag `right-alignment-flags`; patch `no`
- `DisplayConfig` -> `PrintString` in `SPEC_PSXPC_N/SPECIFIC.C`; shape `shape-ui-text-printstring-five-arg`; text `formatted-buffer`; flag `right-alignment-flags`; patch `no`
- `DisplayConfig` -> `PrintString` in `SPEC_PSXPC_N/SPECIFIC.C`; shape `shape-ui-text-printstring-five-arg`; text `string-wad-offset`; flag `center-alignment-flags`; patch `no`
- `DisplayConfig` -> `PrintString` in `SPEC_PSXPC_N/SPECIFIC.C`; shape `shape-ui-text-printstring-five-arg`; text `string-wad-offset`; flag `center-alignment-flags`; patch `no`
- `sub_62190` -> `PrintString` in `SPEC_PSXPC_N/SPECIFIC.C`; shape `shape-ui-text-printstring-five-arg`; text `string-wad-offset`; flag `blink-or-composite-flags`; patch `no`
- `DoPauseMenu` -> `PrintString` in `SPEC_PSXPC_N/SPECIFIC.C`; shape `shape-ui-text-printstring-five-arg`; text `string-wad-offset`; flag `center-alignment-flags`; patch `no`
- `DoPauseMenu` -> `PrintString` in `SPEC_PSXPC_N/SPECIFIC.C`; shape `shape-ui-text-printstring-five-arg`; text `string-wad-offset`; flag `center-alignment-flags`; patch `no`
- `DoPauseMenu` -> `PrintString` in `SPEC_PSXPC_N/SPECIFIC.C`; shape `shape-ui-text-printstring-five-arg`; text `string-wad-offset`; flag `right-alignment-flags`; patch `no`
- `DoPauseMenu` -> `PrintString` in `SPEC_PSXPC_N/SPECIFIC.C`; shape `shape-ui-text-printstring-five-arg`; text `string-wad-offset`; flag `center-alignment-flags`; patch `no`
- `DoPauseMenu` -> `PrintString` in `SPEC_PSXPC_N/SPECIFIC.C`; shape `shape-ui-text-printstring-five-arg`; text `string-wad-offset`; flag `center-alignment-flags`; patch `no`
- `DoPauseMenu` -> `PrintString` in `SPEC_PSXPC_N/SPECIFIC.C`; shape `shape-ui-text-printstring-five-arg`; text `string-wad-offset`; flag `center-alignment-flags`; patch `no`
- `DoPauseMenu` -> `PrintString` in `SPEC_PSXPC_N/SPECIFIC.C`; shape `shape-ui-text-printstring-five-arg`; text `string-wad-offset`; flag `center-alignment-flags`; patch `no`
- `DoPauseMenu` -> `PrintString` in `SPEC_PSXPC_N/SPECIFIC.C`; shape `shape-ui-text-printstring-five-arg`; text `string-wad-offset`; flag `right-alignment-flags`; patch `no`
- `DoPauseMenu` -> `PrintString` in `SPEC_PSXPC_N/SPECIFIC.C`; shape `shape-ui-text-printstring-five-arg`; text `string-wad-offset`; flag `center-alignment-flags`; patch `no`
- `DoPauseMenu` -> `PrintString` in `SPEC_PSXPC_N/SPECIFIC.C`; shape `shape-ui-text-printstring-five-arg`; text `string-wad-offset`; flag `center-alignment-flags`; patch `no`
- `DoPauseMenu` -> `PrintString` in `SPEC_PSXPC_N/SPECIFIC.C`; shape `shape-ui-text-printstring-five-arg`; text `string-wad-offset`; flag `center-alignment-flags`; patch `no`
- `S_Death` -> `PrintString` in `SPEC_PSXPC_N/SPECIFIC.C`; shape `shape-ui-text-printstring-five-arg`; text `string-wad-offset`; flag `blink-or-composite-flags`; patch `no`
- `S_Death` -> `PrintString` in `SPEC_PSXPC_N/SPECIFIC.C`; shape `shape-ui-text-printstring-five-arg`; text `string-wad-offset`; flag `center-alignment-flags`; patch `no`
- `S_Death` -> `PrintString` in `SPEC_PSXPC_N/SPECIFIC.C`; shape `shape-ui-text-printstring-five-arg`; text `string-wad-offset`; flag `center-alignment-flags`; patch `no`
- `S_Death` -> `PrintString` in `SPEC_PSXPC_N/SPECIFIC.C`; shape `shape-ui-text-printstring-five-arg`; text `string-wad-offset`; flag `center-alignment-flags`; patch `no`
- `S_Death` -> `PrintString` in `SPEC_PSXPC_N/SPECIFIC.C`; shape `shape-ui-text-printstring-five-arg`; text `string-wad-offset`; flag `center-alignment-flags`; patch `no`
- `S_Death` -> `PrintString` in `SPEC_PSXPC_N/SPECIFIC.C`; shape `shape-ui-text-printstring-five-arg`; text `string-wad-offset`; flag `center-alignment-flags`; patch `no`
- `TitleOptions` -> `PrintString` in `SPEC_PSXPC_N/TITSEQ.C`; shape `shape-ui-text-printstring-five-arg`; text `formatted-buffer`; flag `blink-or-composite-flags`; patch `no`
- `TitleOptions` -> `PrintString` in `SPEC_PSXPC_N/TITSEQ.C`; shape `shape-ui-text-printstring-five-arg`; text `string-wad-offset`; flag `center-alignment-flags`; patch `no`
- `TitleOptions` -> `PrintString` in `SPEC_PSXPC_N/TITSEQ.C`; shape `shape-ui-text-printstring-five-arg`; text `string-wad-offset`; flag `center-alignment-flags`; patch `no`
- `TitleOptions` -> `PrintString` in `SPEC_PSXPC_N/TITSEQ.C`; shape `shape-ui-text-printstring-five-arg`; text `string-wad-offset`; flag `center-alignment-flags`; patch `no`
- `TitleOptions` -> `PrintString` in `SPEC_PSXPC_N/TITSEQ.C`; shape `shape-ui-text-printstring-five-arg`; text `string-wad-offset`; flag `center-alignment-flags`; patch `no`
- `TitleOptions` -> `PrintString` in `SPEC_PSXPC_N/TITSEQ.C`; shape `shape-ui-text-printstring-five-arg`; text `string-wad-offset`; flag `center-alignment-flags`; patch `no`
- `TitleOptions` -> `PrintString` in `SPEC_PSXPC_N/TITSEQ.C`; shape `shape-ui-text-printstring-five-arg`; text `string-wad-offset`; flag `center-alignment-flags`; patch `no`
- `TitleOptions` -> `PrintString` in `SPEC_PSXPC_N/TITSEQ.C`; shape `shape-ui-text-printstring-five-arg`; text `string-wad-offset`; flag `center-alignment-flags`; patch `no`
- `TitleOptions` -> `PrintString` in `SPEC_PSXPC_N/TITSEQ.C`; shape `shape-ui-text-printstring-five-arg`; text `string-wad-offset`; flag `center-alignment-flags`; patch `no`
- `TitleOptions` -> `PrintString` in `SPEC_PSXPC_N/TITSEQ.C`; shape `shape-ui-text-printstring-five-arg`; text `string-wad-offset`; flag `center-alignment-flags`; patch `no`
- `TitleOptions` -> `PrintString` in `SPEC_PSXPC_N/TITSEQ.C`; shape `shape-ui-text-printstring-five-arg`; text `string-wad-offset`; flag `center-alignment-flags`; patch `no`
- `TitleOptions` -> `PrintString` in `SPEC_PSXPC_N/TITSEQ.C`; shape `shape-ui-text-printstring-five-arg`; text `string-wad-offset`; flag `center-alignment-flags`; patch `no`
- `TitleOptions` -> `PrintString` in `SPEC_PSXPC_N/TITSEQ.C`; shape `shape-ui-text-printstring-five-arg`; text `string-wad-offset`; flag `center-alignment-flags`; patch `no`
- `TitleOptions` -> `PrintString` in `SPEC_PSXPC_N/TITSEQ.C`; shape `shape-ui-text-printstring-five-arg`; text `string-wad-offset`; flag `center-alignment-flags`; patch `no`
- `TitleOptions` -> `PrintString` in `SPEC_PSXPC_N/TITSEQ.C`; shape `shape-ui-text-printstring-five-arg`; text `string-wad-offset`; flag `center-alignment-flags`; patch `no`
- `sub_1054` -> `PrintString` in `SPEC_PSXPC_N/TITSEQ.C`; shape `shape-ui-text-printstring-five-arg`; text `string-wad-offset`; flag `center-alignment-flags`; patch `no`
- `sub_1054` -> `PrintString` in `SPEC_PSXPC_N/TITSEQ.C`; shape `shape-ui-text-printstring-five-arg`; text `string-wad-offset`; flag `center-alignment-flags`; patch `no`
- `sub_1054` -> `PrintString` in `SPEC_PSXPC_N/TITSEQ.C`; shape `shape-ui-text-printstring-five-arg`; text `string-wad-offset`; flag `center-alignment-flags`; patch `no`
- `TITSEQ_StoryBoardMenuControl` -> `PrintString` in `SPEC_PSXPC_N/TITSEQ.C`; shape `shape-ui-text-printstring-five-arg`; text `string-wad-offset`; flag `center-alignment-flags`; patch `no`
- `Requester` -> `GetStringLength` in `SPEC_PSXPC_N/REQUEST.C`; shape `shape-ui-text-length-with-bounds`; text `string-wad-offset`; flag `not-applicable`; patch `no`
- `Requester` -> `GetStringLength` in `SPEC_PSXPC_N/REQUEST.C`; shape `shape-ui-text-length-with-optional-bound`; text `string-wad-offset`; flag `not-applicable`; patch `no`
- `PrintString` -> `GetStringLength` in `SPEC_PSXPC_N/TEXT_S.C`; shape `shape-ui-text-length-with-optional-bound`; text `caller-string-pointer`; flag `not-applicable`; patch `no`
- `PrintString` -> `GetStringLength` in `SPEC_PSXPC_N/TEXT_S.C`; shape `shape-ui-text-length-with-bounds`; text `caller-string-pointer`; flag `not-applicable`; patch `no`
- `GetStringDimensions` -> `GetStringLength` in `SPEC_PSXPC_N/TEXT_S.C`; shape `shape-ui-text-length-with-bounds`; text `caller-string-pointer`; flag `not-applicable`; patch `no`
- `GetStringDimensions` -> `GetStringLength` in `SPEC_PSXPC_N/TEXT_S.C`; shape `shape-ui-text-length-with-bounds`; text `caller-string-pointer`; flag `not-applicable`; patch `no`

No production source or marker change is authorized by this map.
