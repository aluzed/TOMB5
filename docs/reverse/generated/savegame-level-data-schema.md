# SaveLevelData source-level stream schema

Status: Generated
Story: `docs/stories/RE-010-savegame-stream-schema.md`

## Purpose

This file captures the ordered `Write(expr, size)` calls from the current `PC_VERSION` branch of `SaveLevelData`.
The PSX branch is still unimplemented, so this is a reconstruction aid, not proof of PSX equivalence.

## Inputs and outputs

- Source: `GAME/SAVEGAME.C`
- CSV: `docs/reverse/generated/savegame-level-data-schema.csv`
- Parsed write sites: `32`

## How to use this schema

- Treat the row order as the first field-order hypothesis for PSX `SaveLevelData`.
- Preserve loop/conditional context; do not expand rows whose counts depend on runtime values.
- Reconstruct `RestoreLevelData` as the inverse `ReadSG` stream only after checking each field against the original control flow.
- Do not use this file to add `(F)`, `(D)`, or `(**)` markers by itself.

## Rows

### 1. `&FmvSceneTriggered`

- source line: `107`
- size expression: `4`
- context: `top-level`

### 2. `&GLOBAL_lastinvitem`

- source line: `108`
- size expression: `4`
- context: `top-level`

### 3. `&word`

- source line: `115`
- size expression: `2`
- context: `top-level`

### 4. `&word`

- source line: `120`
- size expression: `2`
- context: `for(i = 0; i < 10; i++)`

### 5. `&flipeffect`

- source line: `123`
- size expression: `4`
- context: `top-level`

### 6. `&fliptimer`

- source line: `124`
- size expression: `4`
- context: `top-level`

### 7. `&flip_status`

- source line: `125`
- size expression: `4`
- context: `top-level`

### 8. `cd_flags`

- source line: `126`
- size expression: `136`
- context: `top-level`

### 9. `&CurrentAtmosphere`

- source line: `127`
- size expression: `1`
- context: `top-level`

### 10. `&word`

- source line: `144`
- size expression: `2`
- context: `for(i = 0; i < number_rooms; i++) / for (j = 0; j < room[i].num_meshes; j++) / if (room[i].mesh[j].static_number >= 50 && room[i].mesh[j].static_number <= 59) / if (k == 16)`

### 11. `&word`

- source line: `153`
- size expression: `2`
- context: `if (number_rooms > 0)`

### 12. `&CurrentSequence`

- source line: `156`
- size expression: `1`
- context: `top-level`

### 13. `&byte`

- source line: `163`
- size expression: `1`
- context: `top-level`

### 14. `&camera.fixed[i].flags`

- source line: `167`
- size expression: `2`
- context: `for (i = 0; i < number_cameras; i++)`

### 15. `&SpotCam[i].flags`

- source line: `172`
- size expression: `2`
- context: `for(i = 0; i < number_spotcams; i++)`

### 16. `&word`

- source line: `183`
- size expression: `2`
- context: `for(i = 0; i < level_items; i++, item++) / if (item->flags & IFLAG_KILLED)`

### 17. `&packed`

- source line: `234`
- size expression: `2`
- context: `for(i = 0; i < level_items; i++, item++) / else if (item->flags & (IFLAG_ACTIVATION_MASK | IFLAG_INVISIBLE | 0x20) || item->object_number == LARA && FullSave) / if (obj->save_position)`

### 18. `&packed`

- source line: `236`
- size expression: `2`
- context: `for(i = 0; i < level_items; i++, item++) / else if (item->flags & (IFLAG_ACTIVATION_MASK | IFLAG_INVISIBLE | 0x20) || item->object_number == LARA && FullSave) / if (obj->save_position)`

### 19. `&packed`

- source line: `238`
- size expression: `2`
- context: `for(i = 0; i < level_items; i++, item++) / else if (item->flags & (IFLAG_ACTIVATION_MASK | IFLAG_INVISIBLE | 0x20) || item->object_number == LARA && FullSave) / if (obj->save_position)`

### 20. `&item->room_number`

- source line: `240`
- size expression: `1`
- context: `for(i = 0; i < level_items; i++, item++) / else if (item->flags & (IFLAG_ACTIVATION_MASK | IFLAG_INVISIBLE | 0x20) || item->object_number == LARA && FullSave) / if (obj->save_position)`

### 21. `&item->pos.y_rot`

- source line: `242`
- size expression: `2`
- context: `for(i = 0; i < level_items; i++, item++) / else if (item->flags & (IFLAG_ACTIVATION_MASK | IFLAG_INVISIBLE | 0x20) || item->object_number == LARA && FullSave) / if (obj->save_position)`

### 22. `&item->pos.x_rot`

- source line: `245`
- size expression: `2`
- context: `for(i = 0; i < level_items; i++, item++) / else if (item->flags & (IFLAG_ACTIVATION_MASK | IFLAG_INVISIBLE | 0x20) || item->object_number == LARA && FullSave) / if (obj->save_position)`

### 23. `&item->pos.z_rot`

- source line: `247`
- size expression: `2`
- context: `for(i = 0; i < level_items; i++, item++) / else if (item->flags & (IFLAG_ACTIVATION_MASK | IFLAG_INVISIBLE | 0x20) || item->object_number == LARA && FullSave) / if (obj->save_position)`

### 24. `&item->speed`

- source line: `249`
- size expression: `2`
- context: `for(i = 0; i < level_items; i++, item++) / else if (item->flags & (IFLAG_ACTIVATION_MASK | IFLAG_INVISIBLE | 0x20) || item->object_number == LARA && FullSave) / if (obj->save_position)`

### 25. `&item->fallspeed`

- source line: `251`
- size expression: `2`
- context: `for(i = 0; i < level_items; i++, item++) / else if (item->flags & (IFLAG_ACTIVATION_MASK | IFLAG_INVISIBLE | 0x20) || item->object_number == LARA && FullSave) / if (obj->save_position)`

### 26. `&item->current_anim_state`

- source line: `256`
- size expression: `2`
- context: `for(i = 0; i < level_items; i++, item++) / else if (item->flags & (IFLAG_ACTIVATION_MASK | IFLAG_INVISIBLE | 0x20) || item->object_number == LARA && FullSave) / if (obj->save_anim)`

### 27. `&item->goal_anim_state`

- source line: `257`
- size expression: `2`
- context: `for(i = 0; i < level_items; i++, item++) / else if (item->flags & (IFLAG_ACTIVATION_MASK | IFLAG_INVISIBLE | 0x20) || item->object_number == LARA && FullSave) / if (obj->save_anim)`

### 28. `&item->required_anim_state`

- source line: `258`
- size expression: `2`
- context: `for(i = 0; i < level_items; i++, item++) / else if (item->flags & (IFLAG_ACTIVATION_MASK | IFLAG_INVISIBLE | 0x20) || item->object_number == LARA && FullSave) / if (obj->save_anim)`

### 29. `&item->anim_number`

- source line: `262`
- size expression: `2`
- context: `for(i = 0; i < level_items; i++, item++) / else if (item->flags & (IFLAG_ACTIVATION_MASK | IFLAG_INVISIBLE | 0x20) || item->object_number == LARA && FullSave) / if (obj->save_anim) / if (item->object_number == LARA)`

### 30. `&byte`

- source line: `267`
- size expression: `1`
- context: `for(i = 0; i < level_items; i++, item++) / else if (item->flags & (IFLAG_ACTIVATION_MASK | IFLAG_INVISIBLE | 0x20) || item->object_number == LARA && FullSave) / if (obj->save_anim) / else`

### 31. `&item->frame_number`

- source line: `270`
- size expression: `2`
- context: `for(i = 0; i < level_items; i++, item++) / else if (item->flags & (IFLAG_ACTIVATION_MASK | IFLAG_INVISIBLE | 0x20) || item->object_number == LARA && FullSave) / if (obj->save_anim)`

### 32. `&item->hit_points`

- source line: `274`
- size expression: `2`
- context: `for(i = 0; i < level_items; i++, item++) / else if (item->flags & (IFLAG_ACTIVATION_MASK | IFLAG_INVISIBLE | 0x20) || item->object_number == LARA && FullSave)`
