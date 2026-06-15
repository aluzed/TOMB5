# RE-044 — Post-RestoreLevelData domain reprioritization

Source: `docs/reverse/generated/function-priority.csv`
RestoreLevelData chain: `closed-by-RE-043`
Excluded closed-chain candidates: `3`
Code-change readiness: `documentation-only-selection-gate`
Recommended next ticket: `RE-045`

## Progress tracker

- [x] Closed RestoreLevelData chain excluded.
- [x] Existing priority CSV consumed without raw evidence expansion.
- [x] Domain-level shortlist generated.
- [x] Next ticket selected as a proof-first audit gate.

## Domain shortlist

- `#1` `audio-effects` — Audio/effects hubs
  - status: `candidate`; score: `49533`; candidates: `19`; ND: `1`; runtime: `0`
  - top: `SoundEffect` in `GAME/EFFECTS.C`
  - rationale: high fan-in effects/audio hub; good impact and separated from closed savegame work
  - next action: `create RE-045 for audio-effects proof-first audit`
  - representative functions:
    - `SoundEffect` — `GAME/EFFECTS.C:625`; bucket `P1`; status `decompiled`; score `11749`
    - `SoundEffect` — `GAME/EFFECTS.C:633`; bucket `P1`; status `decompiled`; score `11749`
    - `SoundEffect` — `GAME/EFFECTS.C:891`; bucket `P1`; status `decompiled`; score `11749`
- `#2` `module-game` — Module GAME follow-up
  - status: `candidate`; score: `29309`; candidates: `54`; ND: `3`; runtime: `14`
  - top: `ShatterObject` in `GAME/DEBRIS.C`
  - rationale: remaining mapped non-final domain after savegame closure
  - next action: `defer until higher-ranked domain is selected`
  - representative functions:
    - `ShatterObject` — `GAME/DEBRIS.C:54`; bucket `P1`; status `decompiled`; score `4834`
    - `DoTitle` — `GAME/GAMEFLOW.C:931`; bucket `P0`; status `debugged`; score `4506`
    - `LaraControl` — `GAME/LARAMISC.C:163`; bucket `P1`; status `decompiled`; score `3895`
- `#3` `collision` — Collision and spatial queries
  - status: `candidate`; score: `26055`; candidates: `32`; ND: `0`; runtime: `0`
  - top: `GetCollisionInfo` in `SPEC_PSXPC_N/COLLIDE_S.C`
  - rationale: gameplay collision queries have many callers and clear validation boundaries
  - next action: `defer until higher-ranked domain is selected`
  - representative functions:
    - `GetCollisionInfo` — `SPEC_PSXPC_N/COLLIDE_S.C:475`; bucket `P1`; status `decompiled`; score `5423`
    - `PickUpCollision` — `GAME/PICKUP.C:235`; bucket `P1`; status `decompiled`; score `3480`
    - `PuzzleHoleCollision` — `GAME/PICKUP.C:217`; bucket `P1`; status `decompiled`; score `3335`
- `#4` `module-spec_psxpc_n` — Module SPEC_PSXPC_N follow-up
  - status: `candidate`; score: `25956`; candidates: `27`; ND: `7`; runtime: `5`
  - top: `PrintString` in `SPEC_PSXPC_N/TEXT_S.C`
  - rationale: remaining mapped non-final domain after savegame closure
  - next action: `defer until higher-ranked domain is selected`
  - representative functions:
    - `PrintString` — `SPEC_PSXPC_N/TEXT_S.C:196`; bucket `P1`; status `decompiled`; score `4015`
    - `main` — `SPEC_PSXPC_N/PSXMAIN.C:42`; bucket `P0`; status `debugged`; score `3997`
    - `GetBoundsAccurate` — `SPEC_PSXPC_N/CALCLARA.C:1909`; bucket `P1`; status `decompiled`; score `3481`
- `#5` `maths-render-support` — Maths/render support
  - status: `candidate`; score: `22930`; candidates: `92`; ND: `4`; runtime: `0`
  - top: `mTranslateXYZ` in `SPEC_PSXPC_N/MATHS.C`
  - rationale: remaining mapped non-final domain after savegame closure
  - next action: `defer until higher-ranked domain is selected`
  - representative functions:
    - `mTranslateXYZ` — `SPEC_PSXPC_N/MATHS.C:305`; bucket `P1`; status `decompiled`; score `3122`
    - `DrawPhaseGame` — `SPEC_PSXPC/DRAWPHAS.C:49`; bucket `P1`; status `decompiled`; score `3075`
    - `mTranslateXYZ` — `SPEC_PSXPC/MATHS.C:194`; bucket `P1`; status `decompiled`; score `2902`
- `#6` `traps-switches-doors` — Traps, switches, and doors
  - status: `candidate`; score: `22786`; candidates: `20`; ND: `0`; runtime: `0`
  - top: `ControlRollingBall` in `GAME/TRAPS.C`
  - rationale: remaining mapped non-final domain after savegame closure
  - next action: `defer until higher-ranked domain is selected`
  - representative functions:
    - `ControlRollingBall` — `GAME/TRAPS.C:476`; bucket `P1`; status `decompiled`; score `3756`
    - `ControlExplosion` — `GAME/TRAPS.C:654`; bucket `P1`; status `decompiled`; score `3579`
    - `FlameEmitter3Control` — `GAME/TRAPS.C:377`; bucket `P1`; status `decompiled`; score `3175`
- `#7` `module-spec_psxpc` — Module SPEC_PSXPC follow-up
  - status: `candidate`; score: `22609`; candidates: `28`; ND: `0`; runtime: `4`
  - top: `PrintString` in `SPEC_PSXPC/FXTRIG.C`
  - rationale: remaining mapped non-final domain after savegame closure
  - next action: `defer until higher-ranked domain is selected`
  - representative functions:
    - `PrintString` — `SPEC_PSXPC/FXTRIG.C:7`; bucket `P1`; status `decompiled`; score `3795`
    - `GetBoundsAccurate` — `SPEC_PSXPC/CALCLARA.C:20`; bucket `P1`; status `decompiled`; score `3261`
    - `S_PlayFMV` — `SPEC_PSXPC/MOVIE.C:5`; bucket `P1`; status `decompiled`; score `3118`
- `#8` `module-spec_psx` — Module SPEC_PSX follow-up
  - status: `candidate`; score: `20480`; candidates: `12`; ND: `7`; runtime: `4`
  - top: `main` in `SPEC_PSX/PSXMAIN.C`
  - rationale: contains ND markers that can be audited without source reconstruction
  - next action: `defer until higher-ranked domain is selected`
  - representative functions:
    - `main` — `SPEC_PSX/PSXMAIN.C:39`; bucket `P0`; status `debugged`; score `3817`
    - `S_PlayFMV` — `SPEC_PSX/MOVIE.C:6`; bucket `P1`; status `decompiled`; score `3158`
    - `InitNewCDSystem` — `SPEC_PSX/CD.C:346`; bucket `P0`; status `debugged`; score `3038`
- `#9` `lara-combat` — Lara combat and weapon detection
  - status: `candidate`; score: `19048`; candidates: `10`; ND: `0`; runtime: `0`
  - top: `DoProperDetection` in `GAME/LARAFIRE.C`
  - rationale: remaining mapped non-final domain after savegame closure
  - next action: `defer until higher-ranked domain is selected`
  - representative functions:
    - `DoProperDetection` — `GAME/LARAFIRE.C:99`; bucket `P1`; status `decompiled`; score `4768`
    - `LaraGetNewTarget` — `GAME/LARAFIRE.C:201`; bucket `P1`; status `decompiled`; score `3056`
    - `FireWeapon` — `GAME/LARAFIRE.C:185`; bucket `P1`; status `decompiled`; score `2727`
- `#10` `inventory` — Inventory/frontend item UI
  - status: `candidate`; score: `18517`; candidates: `11`; ND: `0`; runtime: `0`
  - top: `S_CallInventory2` in `GAME/NEWINV2.C`
  - rationale: inventory/frontend routines form an isolatable UI-domain proof chain
  - next action: `defer until higher-ranked domain is selected`
  - representative functions:
    - `S_CallInventory2` — `GAME/NEWINV2.C:3153`; bucket `P1`; status `decompiled`; score `4799`
    - `draw_current_object_list` — `GAME/NEWINV2.C:1890`; bucket `P1`; status `decompiled`; score `4516`
    - `Requester` — `SPEC_PSXPC/REQUEST.C:12`; bucket `P1`; status `decompiled`; score `3328`
- `#11` `input` — Runtime input handling
  - status: `candidate`; score: `13906`; candidates: `3`; ND: `0`; runtime: `2`
  - top: `S_UpdateInput` in `SPEC_PSXPC_N/PSXINPUT.C`
  - rationale: runtime input is high-priority but cross-platform, so scope must be narrow
  - next action: `defer until higher-ranked domain is selected`
  - representative functions:
    - `S_UpdateInput` — `SPEC_PSXPC_N/PSXINPUT.C:91`; bucket `P0`; status `decompiled`; score `4977`
    - `S_UpdateInput` — `SPEC_PSX/PSXINPUT.C:89`; bucket `P0`; status `decompiled`; score `4797`
    - `S_UpdateInput` — `SPEC_PSXPC/PSXPCINPUT.C:60`; bucket `P1`; status `decompiled`; score `4057`
- `#12` `camera` — Camera and spotcam control
  - status: `candidate`; score: `13674`; candidates: `4`; ND: `0`; runtime: `0`
  - top: `CalculateSpotCams` in `GAME/SPOTCAM.C`
  - rationale: camera/spotcam routines are large but domain-local enough for a focused audit
  - next action: `defer until higher-ranked domain is selected`
  - representative functions:
    - `CalculateSpotCams` — `GAME/SPOTCAM.C:429`; bucket `P1`; status `decompiled`; score `6475`
    - `CalculateCamera` — `GAME/CAMERA.C:1167`; bucket `P1`; status `decompiled`; score `4154`
    - `CombatCamera` — `GAME/CAMERA.C:1601`; bucket `P1`; status `decompiled`; score `2845`

## Selection rule

Domains are ranked from existing metadata-only priority rows after excluding the closed savegame chain. Scores aggregate top candidate weights plus small breadth bonuses; the result is a selection gate, not a source-patch authorization.

## Safety decision

No production source patch is implied by RE-044. The selected RE-045 domain must start with metadata-only proof artifacts and its own readiness tracker.
