# SaveLevelData source-level stream schema

Status: Generated
Story: `docs/stories/RE-010-savegame-stream-schema.md`; updated by `docs/stories/RE-011-saveleveldata-psx-implementation.md`, `docs/stories/RE-015-saveleveldata-active-item-serialization.md`

## Purpose

This file captures the ordered `Write(expr, size)` calls from the current `SaveLevelData` implementation.
It is a reconstruction aid for PSX save/restore work, not proof of binary or functional equivalence.

## Inputs and outputs

- Source: `GAME/SAVEGAME.C`
- CSV: `docs/reverse/generated/savegame-level-data-schema.csv`
- Parsed write sites: `34`

## How to use this schema

- Treat the row order as the first field-order hypothesis for PSX `SaveLevelData`.
- Preserve loop/conditional context; do not expand rows whose counts depend on runtime values.
- Reconstruct `RestoreLevelData` as the inverse `ReadSG` stream only after checking each field against the original control flow.
- Do not use this file to add `(F)`, `(D)`, or `(**)` markers by itself.

## Rows

### 1. `&FmvSceneTriggered`

- source line: `106`
- size expression: `4`
- context: `top-level`

### 2. `&GLOBAL_lastinvitem`

- source line: `107`
- size expression: `4`
- context: `top-level`

### 3. `&word`

- source line: `114`
- size expression: `2`
- context: `top-level`

### 4. `&word`

- source line: `119`
- size expression: `2`
- context: `for(i = 0; i < 10; i++)`

### 5. `&flipeffect`

- source line: `122`
- size expression: `4`
- context: `top-level`

### 6. `&fliptimer`

- source line: `123`
- size expression: `4`
- context: `top-level`

### 7. `&flip_status`

- source line: `124`
- size expression: `4`
- context: `top-level`

### 8. `cd_flags`

- source line: `125`
- size expression: `136`
- context: `top-level`

### 9. `&CurrentAtmosphere`

- source line: `126`
- size expression: `1`
- context: `top-level`

### 10. `&word`

- source line: `143`
- size expression: `2`
- context: `for(i = 0; i < number_rooms; i++) / for (j = 0; j < room[i].num_meshes; j++) / if (room[i].mesh[j].static_number >= 50 && room[i].mesh[j].static_number <= 59) / if (k == 16)`

### 11. `&word`

- source line: `152`
- size expression: `2`
- context: `if (number_rooms > 0)`

### 12. `&CurrentSequence`

- source line: `155`
- size expression: `1`
- context: `top-level`

### 13. `&byte`

- source line: `162`
- size expression: `1`
- context: `top-level`

### 14. `&camera.fixed[i].flags`

- source line: `166`
- size expression: `2`
- context: `for (i = 0; i < number_cameras; i++)`

### 15. `&SpotCam[i].flags`

- source line: `171`
- size expression: `2`
- context: `for(i = 0; i < number_spotcams; i++)`

### 16. `&word`

- source line: `182`
- size expression: `2`
- context: `for(i = 0; i < level_items; i++, item++) / if (item->flags & IFLAG_KILLED)`

### 17. `&word`

- source line: `230`
- size expression: `2`
- context: `for(i = 0; i < level_items; i++, item++) / else if (item->flags & (IFLAG_ACTIVATION_MASK | IFLAG_INVISIBLE | 0x20) || item->object_number == LARA && FullSave)`

### 18. `&packed`

- source line: `235`
- size expression: `2`
- context: `for(i = 0; i < level_items; i++, item++) / else if (item->flags & (IFLAG_ACTIVATION_MASK | IFLAG_INVISIBLE | 0x20) || item->object_number == LARA && FullSave) / if (obj->save_position)`

### 19. `&packed`

- source line: `237`
- size expression: `2`
- context: `for(i = 0; i < level_items; i++, item++) / else if (item->flags & (IFLAG_ACTIVATION_MASK | IFLAG_INVISIBLE | 0x20) || item->object_number == LARA && FullSave) / if (obj->save_position)`

### 20. `&packed`

- source line: `239`
- size expression: `2`
- context: `for(i = 0; i < level_items; i++, item++) / else if (item->flags & (IFLAG_ACTIVATION_MASK | IFLAG_INVISIBLE | 0x20) || item->object_number == LARA && FullSave) / if (obj->save_position)`

### 21. `&item->room_number`

- source line: `241`
- size expression: `1`
- context: `for(i = 0; i < level_items; i++, item++) / else if (item->flags & (IFLAG_ACTIVATION_MASK | IFLAG_INVISIBLE | 0x20) || item->object_number == LARA && FullSave) / if (obj->save_position)`

### 22. `&item->pos.y_rot`

- source line: `243`
- size expression: `2`
- context: `for(i = 0; i < level_items; i++, item++) / else if (item->flags & (IFLAG_ACTIVATION_MASK | IFLAG_INVISIBLE | 0x20) || item->object_number == LARA && FullSave) / if (obj->save_position)`

### 23. `&item->pos.x_rot`

- source line: `246`
- size expression: `2`
- context: `for(i = 0; i < level_items; i++, item++) / else if (item->flags & (IFLAG_ACTIVATION_MASK | IFLAG_INVISIBLE | 0x20) || item->object_number == LARA && FullSave) / if (obj->save_position)`

### 24. `&item->pos.z_rot`

- source line: `248`
- size expression: `2`
- context: `for(i = 0; i < level_items; i++, item++) / else if (item->flags & (IFLAG_ACTIVATION_MASK | IFLAG_INVISIBLE | 0x20) || item->object_number == LARA && FullSave) / if (obj->save_position)`

### 25. `&item->speed`

- source line: `250`
- size expression: `2`
- context: `for(i = 0; i < level_items; i++, item++) / else if (item->flags & (IFLAG_ACTIVATION_MASK | IFLAG_INVISIBLE | 0x20) || item->object_number == LARA && FullSave) / if (obj->save_position)`

### 26. `&item->fallspeed`

- source line: `252`
- size expression: `2`
- context: `for(i = 0; i < level_items; i++, item++) / else if (item->flags & (IFLAG_ACTIVATION_MASK | IFLAG_INVISIBLE | 0x20) || item->object_number == LARA && FullSave) / if (obj->save_position)`

### 27. `&item->current_anim_state`

- source line: `257`
- size expression: `2`
- context: `for(i = 0; i < level_items; i++, item++) / else if (item->flags & (IFLAG_ACTIVATION_MASK | IFLAG_INVISIBLE | 0x20) || item->object_number == LARA && FullSave) / if (obj->save_anim)`

### 28. `&item->goal_anim_state`

- source line: `258`
- size expression: `2`
- context: `for(i = 0; i < level_items; i++, item++) / else if (item->flags & (IFLAG_ACTIVATION_MASK | IFLAG_INVISIBLE | 0x20) || item->object_number == LARA && FullSave) / if (obj->save_anim)`

### 29. `&item->required_anim_state`

- source line: `259`
- size expression: `2`
- context: `for(i = 0; i < level_items; i++, item++) / else if (item->flags & (IFLAG_ACTIVATION_MASK | IFLAG_INVISIBLE | 0x20) || item->object_number == LARA && FullSave) / if (obj->save_anim)`

### 30. `&item->anim_number`

- source line: `263`
- size expression: `2`
- context: `for(i = 0; i < level_items; i++, item++) / else if (item->flags & (IFLAG_ACTIVATION_MASK | IFLAG_INVISIBLE | 0x20) || item->object_number == LARA && FullSave) / if (obj->save_anim) / if (item->object_number == LARA)`

### 31. `&byte`

- source line: `268`
- size expression: `1`
- context: `for(i = 0; i < level_items; i++, item++) / else if (item->flags & (IFLAG_ACTIVATION_MASK | IFLAG_INVISIBLE | 0x20) || item->object_number == LARA && FullSave) / if (obj->save_anim) / else`

### 32. `&item->frame_number`

- source line: `271`
- size expression: `2`
- context: `for(i = 0; i < level_items; i++, item++) / else if (item->flags & (IFLAG_ACTIVATION_MASK | IFLAG_INVISIBLE | 0x20) || item->object_number == LARA && FullSave) / if (obj->save_anim)`

### 33. `&item->hit_points`

- source line: `275`
- size expression: `2`
- context: `for(i = 0; i < level_items; i++, item++) / else if (item->flags & (IFLAG_ACTIVATION_MASK | IFLAG_INVISIBLE | 0x20) || item->object_number == LARA && FullSave)`

### 34. `&flags`

- source line: `289`
- size expression: `4`
- context: `for(i = 0; i < level_items; i++, item++) / else if (item->flags & (IFLAG_ACTIVATION_MASK | IFLAG_INVISIBLE | 0x20) || item->object_number == LARA && FullSave) / if (obj->save_flags)`
