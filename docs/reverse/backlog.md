# Backlog priorisée des fonctions reverse TOMB5

Generated: `2026-06-14T20:57:12.672183+00:00`
Source: `docs/reverse/generated/repo-function-map.csv`
CSV détaillé: `docs/reverse/generated/function-priority.csv`
Story: `docs/stories/RE-004-priorisation-fonctions-non-finalisees.md`
Status: Done

## Progress tracker

- [x] Définir une scoring rule reproductible.
- [x] Consommer le mapping Ghidra/repo généré par RE-002.
- [x] Classer les fonctions en lots actionnables.
- [x] Pointer fichier source, ligne et adresse Ghidra quand disponible.
- [x] Mettre en évidence les fonctions `(ND)`.

## Scoring rule

Le score est calculé par `scripts/reverse/function_priority.py`:

```text
score = body_size + callers*120 + callees*35
      + module_weight
      + 500 si mapped / -500 si repo-only
      + 900 si ND
      + 700 si runtime_focus
      + status_weight
```

Pondérations module: `GAME=350`, `SPEC_PSXPC_N=300`, `SPEC_PSX=120`, `SPEC_PSXPC=80`, `SPEC_PC_N=20`.

Pondérations statut: `decompiled=+250`, `named=+150`, `unknown=-200`. Les fonctions déjà final/debug/binary-matched ne restent candidates que si elles portent aussi `(ND)`, pour forcer une vérification de cohérence.

`runtime_focus=yes` si le fichier ou le nom touche notamment `GAMEFLOW`, `SETUP`, `ROOMLOAD`, `LOAD_LEV`, `PSXMAIN`, `PSXINPUT`, `CD`, `SAVEGAME`, `TITLE` ou `TITSEQ`.

Buckets:

- `P0`: fonctions `(ND)` ou fonctions runtime non finalisées déjà mappées.
- `P1`: fonctions non finalisées mappées avec score élevé.
- `P2`: reste du backlog, surtout repo-only/unmapped ou faible impact immédiat.

## Summary

- candidates total: `348` / repo rows `1250`
- mapped candidates: `205`
- ND highlighted: `23`
- P0: `35`; P1: `103`; P2: `210`
- statuses: `debugged` `23`; `decompiled` `324`; `unknown` `1`

## Lot 1 — P0 runtime / ND à clarifier

- `#1` `0x80054f6c` `RestoreLevelData` — `P0` score `6420`
  - source: `GAME/SAVEGAME.C:82`; Ghidra: `0x80054f6c` `FUN_80054f6c`
  - status: `decompiled`; markers: `none`; ND: `no`; runtime: `yes`
  - graph: callers `1`, callees `12`, body_size `4080`
  - why: chemin runtime/chargement/input; adresse Ghidra disponible; 1 caller(s); 12 callee(s); body_size 4080; statut decompiled
  - next: Comparer MIPS/Ghidra avec le chemin runtime documenté, puis tester build si possible.
- `#2` `0x80053f10` `SaveLevelData` — `P0` score `6143`
  - source: `GAME/SAVEGAME.C:100`; Ghidra: `0x80053f10` `FUN_80053f10`
  - status: `decompiled`; markers: `none`; ND: `no`; runtime: `yes`
  - graph: callers `1`, callees `1`, body_size `4188`
  - why: chemin runtime/chargement/input; adresse Ghidra disponible; 1 caller(s); 1 callee(s); body_size 4188; statut decompiled
  - next: Comparer MIPS/Ghidra avec le chemin runtime documenté, puis tester build si possible.
- `#3` `0x8006038c` `S_UpdateInput` — `P0` score `4977`
  - source: `SPEC_PSXPC_N/PSXINPUT.C:91`; Ghidra: `0x8006038c` `FUN_8006038c`
  - status: `decompiled`; markers: `none`; ND: `no`; runtime: `yes`
  - graph: callers `5`, callees `5`, body_size `2452`
  - why: chemin runtime/chargement/input; adresse Ghidra disponible; 5 caller(s); 5 callee(s); body_size 2452; statut decompiled
  - next: Comparer MIPS/Ghidra avec le chemin runtime documenté, puis tester build si possible.
- `#4` `0x8006038c` `S_UpdateInput` — `P0` score `4797`
  - source: `SPEC_PSX/PSXINPUT.C:89`; Ghidra: `0x8006038c` `FUN_8006038c`
  - status: `decompiled`; markers: `none`; ND: `no`; runtime: `yes`
  - graph: callers `5`, callees `5`, body_size `2452`
  - why: chemin runtime/chargement/input; adresse Ghidra disponible; 5 caller(s); 5 callee(s); body_size 2452; statut decompiled
  - next: Comparer MIPS/Ghidra avec le chemin runtime documenté, puis tester build si possible.
- `#5` `0x800105c4` `DoTitle` — `P0` score `4506`
  - source: `GAME/GAMEFLOW.C:931`; Ghidra: `0x800105c4` `FUN_800105c4`
  - status: `debugged`; markers: `D;F;ND`; ND: `yes`; runtime: `yes`
  - graph: callers `0`, callees `24`, body_size `1216`
  - why: marqué ND; chemin runtime/chargement/input; adresse Ghidra disponible; 24 callee(s); body_size 1216
  - next: Vérifier comportement, retirer ND seulement avec preuve/debug documenté.
- `#6` `0x80010064` `main` — `P0` score `3997`
  - source: `SPEC_PSXPC_N/PSXMAIN.C:42`; Ghidra: `0x80010064` `FUN_80010064`
  - status: `debugged`; markers: `D;F;ND`; ND: `yes`; runtime: `yes`
  - graph: callers `0`, callees `31`, body_size `512`
  - why: marqué ND; chemin runtime/chargement/input; adresse Ghidra disponible; 31 callee(s); body_size 512
  - next: Vérifier comportement, retirer ND seulement avec preuve/debug documenté.
- `#7` `0x80010064` `main` — `P0` score `3817`
  - source: `SPEC_PSX/PSXMAIN.C:39`; Ghidra: `0x80010064` `FUN_80010064`
  - status: `debugged`; markers: `D;F;ND`; ND: `yes`; runtime: `yes`
  - graph: callers `0`, callees `31`, body_size `512`
  - why: marqué ND; chemin runtime/chargement/input; adresse Ghidra disponible; 31 callee(s); body_size 512
  - next: Vérifier comportement, retirer ND seulement avec preuve/debug documenté.
- `#8` `0x8005e264` `InitNewCDSystem` — `P0` score `3218`
  - source: `SPEC_PSXPC_N/CD.C:354`; Ghidra: `0x8005e264` `FUN_8005e264`
  - status: `debugged`; markers: `D;F;ND`; ND: `yes`; runtime: `yes`
  - graph: callers `1`, callees `10`, body_size `348`
  - why: marqué ND; chemin runtime/chargement/input; adresse Ghidra disponible; 1 caller(s); 10 callee(s); body_size 348
  - next: Vérifier comportement, retirer ND seulement avec preuve/debug documenté.
- `#9` `0x8005e264` `InitNewCDSystem` — `P0` score `3038`
  - source: `SPEC_PSX/CD.C:346`; Ghidra: `0x8005e264` `FUN_8005e264`
  - status: `debugged`; markers: `D;F;ND`; ND: `yes`; runtime: `yes`
  - graph: callers `1`, callees `10`, body_size `348`
  - why: marqué ND; chemin runtime/chargement/input; adresse Ghidra disponible; 1 caller(s); 10 callee(s); body_size 348
  - next: Vérifier comportement, retirer ND seulement avec preuve/debug documenté.
- `#10` `0x80010264` `QuickControlPhase` — `P0` score `2836`
  - source: `GAME/GAMEFLOW.C:783`; Ghidra: `0x80010264` `FUN_80010264`
  - status: `debugged`; markers: `D;F;ND`; ND: `yes`; runtime: `yes`
  - graph: callers `2`, callees `2`, body_size `76`
  - why: marqué ND; chemin runtime/chargement/input; adresse Ghidra disponible; 2 caller(s); 2 callee(s); body_size 76
  - next: Vérifier comportement, retirer ND seulement avec preuve/debug documenté.

## Lot 2 — P1 grands hubs mappés

- `#36` `0x800937c4` `SoundEffect` — `P1` score `11749`
  - source: `GAME/EFFECTS.C:625`; Ghidra: `0x800937c4` `FUN_800937c4`
  - status: `decompiled`; markers: `none`; ND: `no`; runtime: `no`
  - graph: callers `75`, callees `7`, body_size `1404`
  - why: adresse Ghidra disponible; 75 caller(s); 7 callee(s); body_size 1404; statut decompiled
  - next: Comparer Ghidra/MIPS, valider types/bit-fields, puis décider F ou D.
- `#37` `0x800937c4` `SoundEffect` — `P1` score `11749`
  - source: `GAME/EFFECTS.C:633`; Ghidra: `0x800937c4` `FUN_800937c4`
  - status: `decompiled`; markers: `none`; ND: `no`; runtime: `no`
  - graph: callers `75`, callees `7`, body_size `1404`
  - why: adresse Ghidra disponible; 75 caller(s); 7 callee(s); body_size 1404; statut decompiled
  - next: Comparer Ghidra/MIPS, valider types/bit-fields, puis décider F ou D.
- `#38` `0x800937c4` `SoundEffect` — `P1` score `11749`
  - source: `GAME/EFFECTS.C:891`; Ghidra: `0x800937c4` `FUN_800937c4`
  - status: `decompiled`; markers: `none`; ND: `no`; runtime: `no`
  - graph: callers `75`, callees `7`, body_size `1404`
  - why: adresse Ghidra disponible; 75 caller(s); 7 callee(s); body_size 1404; statut decompiled
  - next: Comparer Ghidra/MIPS, valider types/bit-fields, puis décider F ou D.
- `#39` `0x800383d0` `CalculateSpotCams` — `P1` score `6475`
  - source: `GAME/SPOTCAM.C:429`; Ghidra: `0x800383d0` `FUN_800383d0`
  - status: `decompiled`; markers: `none`; ND: `no`; runtime: `no`
  - graph: callers `1`, callees `13`, body_size `4800`
  - why: adresse Ghidra disponible; 1 caller(s); 13 callee(s); body_size 4800; statut decompiled
  - next: Comparer Ghidra/MIPS, valider types/bit-fields, puis décider F ou D.
- `#40` `0x8007d254` `GetCollisionInfo` — `P1` score `5423`
  - source: `SPEC_PSXPC_N/COLLIDE_S.C:475`; Ghidra: `0x8007d254` `FUN_8007d254`
  - status: `decompiled`; markers: `none`; ND: `no`; runtime: `no`
  - graph: callers `19`, callees `7`, body_size `1848`
  - why: adresse Ghidra disponible; 19 caller(s); 7 callee(s); body_size 1848; statut decompiled
  - next: Comparer Ghidra/MIPS, valider types/bit-fields, puis décider F ou D.
- `#41` `0x80036f3c` `ShatterObject` — `P1` score `4834`
  - source: `GAME/DEBRIS.C:54`; Ghidra: `0x80036f3c` `FUN_80036f3c`
  - status: `decompiled`; markers: `none`; ND: `no`; runtime: `no`
  - graph: callers `7`, callees `6`, body_size `2684`
  - why: adresse Ghidra disponible; 7 caller(s); 6 callee(s); body_size 2684; statut decompiled
  - next: Comparer Ghidra/MIPS, valider types/bit-fields, puis décider F ou D.
- `#42` `0x8003bc04` `S_CallInventory2` — `P1` score `4799`
  - source: `GAME/NEWINV2.C:3153`; Ghidra: `0x8003bc04` `FUN_8003bc04`
  - status: `decompiled`; markers: `none`; ND: `no`; runtime: `no`
  - graph: callers `2`, callees `37`, body_size `2164`
  - why: adresse Ghidra disponible; 2 caller(s); 37 callee(s); body_size 2164; statut decompiled
  - next: Comparer Ghidra/MIPS, valider types/bit-fields, puis décider F ou D.
- `#43` `0x80048de8` `DoProperDetection` — `P1` score `4768`
  - source: `GAME/LARAFIRE.C:99`; Ghidra: `0x80048de8` `FUN_80048de8`
  - status: `decompiled`; markers: `none`; ND: `no`; runtime: `no`
  - graph: callers `2`, callees `4`, body_size `3288`
  - why: adresse Ghidra disponible; 2 caller(s); 4 callee(s); body_size 3288; statut decompiled
  - next: Comparer Ghidra/MIPS, valider types/bit-fields, puis décider F ou D.
- `#44` `0x8003d7a4` `draw_current_object_list` — `P1` score `4516`
  - source: `GAME/NEWINV2.C:1890`; Ghidra: `0x8003d7a4` `FUN_8003d7a4`
  - status: `decompiled`; markers: `none`; ND: `no`; runtime: `no`
  - graph: callers `1`, callees `8`, body_size `3016`
  - why: adresse Ghidra disponible; 1 caller(s); 8 callee(s); body_size 3016; statut decompiled
  - next: Comparer Ghidra/MIPS, valider types/bit-fields, puis décider F ou D.
- `#45` `0x80027fac` `CalculateCamera` — `P1` score `4154`
  - source: `GAME/CAMERA.C:1167`; Ghidra: `0x80027fac` `FUN_80027fac`
  - status: `decompiled`; markers: `none`; ND: `no`; runtime: `no`
  - graph: callers `3`, callees `14`, body_size `2204`
  - why: adresse Ghidra disponible; 3 caller(s); 14 callee(s); body_size 2204; statut decompiled
  - next: Comparer Ghidra/MIPS, valider types/bit-fields, puis décider F ou D.

## Lot 3 — fichiers chauds à traiter par zones

- `SPEC_PSXPC_N/ANIMITEM.C`
  - candidates: `24`; mapped: `2`; ND: `0`; top score: `2967`
- `SPEC_PSXPC_N/MATHS.C`
  - candidates: `19`; mapped: `4`; ND: `0`; top score: `3122`
- `SPEC_PSXPC/MATHS.C`
  - candidates: `18`; mapped: `4`; ND: `0`; top score: `2902`
- `GAME/TRAPS.C`
  - candidates: `15`; mapped: `15`; ND: `0`; top score: `3756`
- `GAME/SWITCH.C`
  - candidates: `15`; mapped: `15`; ND: `0`; top score: `2414`
- `SPEC_PSXPC_N/MISC.C`
  - candidates: `13`; mapped: `9`; ND: `4`; top score: `2052`
- `GAME/SETUP.C`
  - candidates: `12`; mapped: `0`; ND: `0`; top score: `800`
- `GAME/LARAFIRE.C`
  - candidates: `10`; mapped: `7`; ND: `0`; top score: `4768`
- `SPEC_PSXPC/MISC.C`
  - candidates: `9`; mapped: `6`; ND: `0`; top score: `1533`
- `GAME/DOOR.C`
  - candidates: `8`; mapped: `8`; ND: `0`; top score: `2452`
- `GAME/PICKUP.C`
  - candidates: `7`; mapped: `7`; ND: `0`; top score: `3480`
- `SPEC_PSXPC/SFX.C`
  - candidates: `7`; mapped: `4`; ND: `0`; top score: `1399`
- `SPEC_PSXPC/PROFILE.C`
  - candidates: `7`; mapped: `0`; ND: `0`; top score: `-170`
- `GAME/LARA.C`
  - candidates: `6`; mapped: `6`; ND: `0`; top score: `3643`
- `GAME/LARAFLAR.C`
  - candidates: `5`; mapped: `5`; ND: `0`; top score: `2652`

## Lot 4 — P2 / pré-tri mapping

- `#139` `0x8005c0f8` `ControlTwoBlockPlatform` — `P2` score `1798`
  - source: `GAME/TRAPS.C:556`; Ghidra: `0x8005c0f8` `FUN_8005c0f8`
  - status: `decompiled`; markers: `none`; ND: `no`; runtime: `no`
  - graph: callers `0`, callees `6`, body_size `488`
  - why: adresse Ghidra disponible; 6 callee(s); body_size 488; statut decompiled
  - next: Comparer Ghidra/MIPS, valider types/bit-fields, puis décider F ou D.
- `#140` `0x8002dab8` `Load_and_Init_Cutseq` — `P2` score `1784`
  - source: `GAME/DELTAPAK.C:3221`; Ghidra: `0x8002dab8` `FUN_8002dab8`
  - status: `decompiled`; markers: `none`; ND: `no`; runtime: `no`
  - graph: callers `1`, callees `8`, body_size `284`
  - why: adresse Ghidra disponible; 1 caller(s); 8 callee(s); body_size 284; statut decompiled
  - next: Comparer Ghidra/MIPS, valider types/bit-fields, puis décider F ou D.
- `#141` `0x80062dc8` `DisplayFiles` — `P2` score `1779`
  - source: `SPEC_PSX/LOADSAVE.C:44`; Ghidra: `0x80062dc8` `FUN_80062dc8`
  - status: `decompiled`; markers: `none`; ND: `no`; runtime: `no`
  - graph: callers `0`, callees `7`, body_size `664`
  - why: adresse Ghidra disponible; 7 callee(s); body_size 664; statut decompiled
  - next: Comparer Ghidra/MIPS, valider types/bit-fields, puis décider F ou D.
- `#142` `0x80058be0` `CrowDoveSwitchCollision` — `P2` score `1776`
  - source: `GAME/SWITCH.C:127`; Ghidra: `0x80058be0` `FUN_80058be0`
  - status: `decompiled`; markers: `none`; ND: `no`; runtime: `no`
  - graph: callers `0`, callees `4`, body_size `536`
  - why: adresse Ghidra disponible; 4 callee(s); body_size 536; statut decompiled
  - next: Comparer Ghidra/MIPS, valider types/bit-fields, puis décider F ou D.
- `#143` `0x8002bd60` `UnderwaterDoorCollision` — `P2` score `1771`
  - source: `GAME/DOOR.C:112`; Ghidra: `0x8002bd60` `FUN_8002bd60`
  - status: `decompiled`; markers: `none`; ND: `no`; runtime: `no`
  - graph: callers `0`, callees `5`, body_size `496`
  - why: adresse Ghidra disponible; 5 callee(s); body_size 496; statut decompiled
  - next: Comparer Ghidra/MIPS, valider types/bit-fields, puis décider F ou D.
- `#144` `0x80079b30` `mQuickW2VMatrix` — `P2` score `1766`
  - source: `SPEC_PSXPC_N/MATHS.C:15`; Ghidra: `0x80079b30` `FUN_80079b30`
  - status: `decompiled`; markers: `none`; ND: `no`; runtime: `no`
  - graph: callers `4`, callees `0`, body_size `236`
  - why: adresse Ghidra disponible; 4 caller(s); body_size 236; statut decompiled
  - next: Comparer Ghidra/MIPS, valider types/bit-fields, puis décider F ou D.
- `#145` `0x80057138` `PulleyCollision` — `P2` score `1756`
  - source: `GAME/SWITCH.C:328`; Ghidra: `0x80057138` `FUN_80057138`
  - status: `decompiled`; markers: `none`; ND: `no`; runtime: `no`
  - graph: callers `0`, callees `4`, body_size `516`
  - why: adresse Ghidra disponible; 4 callee(s); body_size 516; statut decompiled
  - next: Comparer Ghidra/MIPS, valider types/bit-fields, puis décider F ou D.
- `#146` `0x8005fdd0` `GPU_BeginScene` — `P2` score `1753`
  - source: `SPEC_PSXPC_N/MISC.C:249`; Ghidra: `0x8005fdd0` `FUN_8005fdd0`
  - status: `decompiled`; markers: `none`; ND: `no`; runtime: `no`
  - graph: callers `5`, callees `1`, body_size `68`
  - why: adresse Ghidra disponible; 5 caller(s); 1 callee(s); body_size 68; statut decompiled
  - next: Comparer Ghidra/MIPS, valider types/bit-fields, puis décider F ou D.
- `#147` `0x80063060` `LoadGame` — `P2` score `1750`
  - source: `SPEC_PSXPC_N/LOADSAVE.C:119`; Ghidra: `0x80063060` `FUN_80063060`
  - status: `decompiled`; markers: `none`; ND: `no`; runtime: `no`
  - graph: callers `2`, callees `4`, body_size `320`
  - why: adresse Ghidra disponible; 2 caller(s); 4 callee(s); body_size 320; statut decompiled
  - next: Comparer Ghidra/MIPS, valider types/bit-fields, puis décider F ou D.
- `#148` `0x8008ff20` `GetStringLength` — `P2` score `1742`
  - source: `SPEC_PSXPC_N/TEXT_S.C:401`; Ghidra: `0x8008ff20` `FUN_8008ff20`
  - status: `decompiled`; markers: `none`; ND: `no`; runtime: `no`
  - graph: callers `3`, callees `0`, body_size `332`
  - why: adresse Ghidra disponible; 3 caller(s); body_size 332; statut decompiled
  - next: Comparer Ghidra/MIPS, valider types/bit-fields, puis décider F ou D.

## Workflow recommandé par fonction

1. Ouvrir l'adresse `ghidra_entry` si disponible; sinon vérifier d'abord le commentaire/adresse repo.
2. Comparer la fonction avec `docs/reverse/conventions.md` et `docs/reverse/psx-exe-layout.md`.
3. Vérifier types 32-bit, bit-fields et overlays avant toute modification de marqueur.
4. Compiler ou documenter le blocage runtime/build selon le chemin touché.
5. Ne marquer `(F)`, `(D)` ou `(**)` qu'en suivant la checklist de `docs/reverse/conventions.md`.

## Acceptance criteria

- [x] Une liste priorisée existe avec justification.
- [x] Chaque entrée pointe vers un fichier source repo et une adresse Ghidra quand disponible.
- [x] Les fonctions `(ND)` sont mises en évidence.
- [x] Les lots sont assez petits pour être pris un par un.
