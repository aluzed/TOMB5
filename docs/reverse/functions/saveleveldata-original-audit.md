# SaveLevelData original dump audit

Status: Generated
Story: `docs/stories/RE-012-saveleveldata-original-audit.md`

## Progress tracker

- [x] Count original `WriteSG` calls from the ignored original dump CSV.
- [x] Count source-level `Write(...)` sites from `GAME/SAVEGAME.C`.
- [x] Record only versionable metadata, not original instruction rows or bytes.
- [x] State the current marker verdict explicitly.

## Inputs

- Source: `GAME/SAVEGAME.C`
- Original dump CSV: `build/reverse/re007/original/SaveLevelData_80053f10.csv` (ignored; not versioned)
- `WriteSG` final PSX address: `0x80053b04`

## Counts

- original instruction count: `1047`
- original `WriteSG` call count: `81`
- source `Write(...)` site count: `32`
- top-level source write sites: `10`
- loop/conditional-context source write sites: `22`
- status: `needs-control-flow-audit`

## Interpretation

The original PSX function is still represented only by ignored local dump data.
The current source schema has fewer static `Write(...)` sites than the original `WriteSG` call count because source rows include loops and conditionals that must be audited against control flow before any completeness marker is justified.

## Verdict

- `(**)`: no — no rebuilt comparable object/binary comparison was produced.
- `(F)`: no — the source stream is a useful hypothesis, but the original control-flow and per-call field mapping remain unaudited.
- `(D)`: no — no runtime save/restore validation was performed.
- Do not add `(F)`, `(D)`, or `(**)` from this report alone.

## Source schema rows

These are source-level expressions only and are safe to version; they do not include original instructions or bytes.

- `1` line `106`: `&FmvSceneTriggered` size `4` context `top-level`
- `2` line `107`: `&GLOBAL_lastinvitem` size `4` context `top-level`
- `3` line `114`: `&word` size `2` context `top-level`
- `4` line `119`: `&word` size `2` context `for(i = 0; i < 10; i++)`
- `5` line `122`: `&flipeffect` size `4` context `top-level`
- `6` line `123`: `&fliptimer` size `4` context `top-level`
- `7` line `124`: `&flip_status` size `4` context `top-level`
- `8` line `125`: `cd_flags` size `136` context `top-level`
- `9` line `126`: `&CurrentAtmosphere` size `1` context `top-level`
- `10` line `143`: `&word` size `2` context `for(i = 0; i < number_rooms; i++) / for (j = 0; j < room[i].num_meshes; j++) / if (room[i].mesh[j].static_number >= 50 && room[i].mesh[j].static_number <= 59) / if (k == 16)`
- `11` line `152`: `&word` size `2` context `if (number_rooms > 0)`
- `12` line `155`: `&CurrentSequence` size `1` context `top-level`
- `13` line `162`: `&byte` size `1` context `top-level`
- `14` line `166`: `&camera.fixed[i].flags` size `2` context `for (i = 0; i < number_cameras; i++)`
- `15` line `171`: `&SpotCam[i].flags` size `2` context `for(i = 0; i < number_spotcams; i++)`
- `16` line `182`: `&word` size `2` context `for(i = 0; i < level_items; i++, item++) / if (item->flags & IFLAG_KILLED)`
- `17` line `233`: `&packed` size `2` context `for(i = 0; i < level_items; i++, item++) / else if (item->flags & (IFLAG_ACTIVATION_MASK | IFLAG_INVISIBLE | 0x20) || item->object_number == LARA && FullSave) / if (obj->save_position)`
- `18` line `235`: `&packed` size `2` context `for(i = 0; i < level_items; i++, item++) / else if (item->flags & (IFLAG_ACTIVATION_MASK | IFLAG_INVISIBLE | 0x20) || item->object_number == LARA && FullSave) / if (obj->save_position)`
- `19` line `237`: `&packed` size `2` context `for(i = 0; i < level_items; i++, item++) / else if (item->flags & (IFLAG_ACTIVATION_MASK | IFLAG_INVISIBLE | 0x20) || item->object_number == LARA && FullSave) / if (obj->save_position)`
- `20` line `239`: `&item->room_number` size `1` context `for(i = 0; i < level_items; i++, item++) / else if (item->flags & (IFLAG_ACTIVATION_MASK | IFLAG_INVISIBLE | 0x20) || item->object_number == LARA && FullSave) / if (obj->save_position)`
- `21` line `241`: `&item->pos.y_rot` size `2` context `for(i = 0; i < level_items; i++, item++) / else if (item->flags & (IFLAG_ACTIVATION_MASK | IFLAG_INVISIBLE | 0x20) || item->object_number == LARA && FullSave) / if (obj->save_position)`
- `22` line `244`: `&item->pos.x_rot` size `2` context `for(i = 0; i < level_items; i++, item++) / else if (item->flags & (IFLAG_ACTIVATION_MASK | IFLAG_INVISIBLE | 0x20) || item->object_number == LARA && FullSave) / if (obj->save_position)`
- `23` line `246`: `&item->pos.z_rot` size `2` context `for(i = 0; i < level_items; i++, item++) / else if (item->flags & (IFLAG_ACTIVATION_MASK | IFLAG_INVISIBLE | 0x20) || item->object_number == LARA && FullSave) / if (obj->save_position)`
- `24` line `248`: `&item->speed` size `2` context `for(i = 0; i < level_items; i++, item++) / else if (item->flags & (IFLAG_ACTIVATION_MASK | IFLAG_INVISIBLE | 0x20) || item->object_number == LARA && FullSave) / if (obj->save_position)`
- `25` line `250`: `&item->fallspeed` size `2` context `for(i = 0; i < level_items; i++, item++) / else if (item->flags & (IFLAG_ACTIVATION_MASK | IFLAG_INVISIBLE | 0x20) || item->object_number == LARA && FullSave) / if (obj->save_position)`
- `26` line `255`: `&item->current_anim_state` size `2` context `for(i = 0; i < level_items; i++, item++) / else if (item->flags & (IFLAG_ACTIVATION_MASK | IFLAG_INVISIBLE | 0x20) || item->object_number == LARA && FullSave) / if (obj->save_anim)`
- `27` line `256`: `&item->goal_anim_state` size `2` context `for(i = 0; i < level_items; i++, item++) / else if (item->flags & (IFLAG_ACTIVATION_MASK | IFLAG_INVISIBLE | 0x20) || item->object_number == LARA && FullSave) / if (obj->save_anim)`
- `28` line `257`: `&item->required_anim_state` size `2` context `for(i = 0; i < level_items; i++, item++) / else if (item->flags & (IFLAG_ACTIVATION_MASK | IFLAG_INVISIBLE | 0x20) || item->object_number == LARA && FullSave) / if (obj->save_anim)`
- `29` line `261`: `&item->anim_number` size `2` context `for(i = 0; i < level_items; i++, item++) / else if (item->flags & (IFLAG_ACTIVATION_MASK | IFLAG_INVISIBLE | 0x20) || item->object_number == LARA && FullSave) / if (obj->save_anim) / if (item->object_number == LARA)`
- `30` line `266`: `&byte` size `1` context `for(i = 0; i < level_items; i++, item++) / else if (item->flags & (IFLAG_ACTIVATION_MASK | IFLAG_INVISIBLE | 0x20) || item->object_number == LARA && FullSave) / if (obj->save_anim) / else`
- `31` line `269`: `&item->frame_number` size `2` context `for(i = 0; i < level_items; i++, item++) / else if (item->flags & (IFLAG_ACTIVATION_MASK | IFLAG_INVISIBLE | 0x20) || item->object_number == LARA && FullSave) / if (obj->save_anim)`
- `32` line `273`: `&item->hit_points` size `2` context `for(i = 0; i < level_items; i++, item++) / else if (item->flags & (IFLAG_ACTIVATION_MASK | IFLAG_INVISIBLE | 0x20) || item->object_number == LARA && FullSave)`
