# RestoreLevelData source-level stream schema

Status: Generated
Story: companion to `docs/stories/RE-010-savegame-stream-schema.md` and RE-018/RE-019 restore audits

## Purpose

This file captures the ordered `ReadSG(expr, size)` calls from the current `RestoreLevelData` implementation.
It is a reconstruction aid for PSX save/restore work, not proof of binary or functional equivalence.

## Inputs and outputs

- Source: `GAME/SAVEGAME.C`
- CSV: `docs/reverse/generated/restore-level-data-schema.csv`
- Parsed read sites: `38`

## How to use this schema

- Treat the row order as the current source-side read hypothesis for `RestoreLevelData`.
- Preserve loop/conditional context; do not expand rows whose counts depend on runtime values.
- Compare with `docs/reverse/generated/savegame-level-data-schema.md` only as a source-symmetry check; symmetry is not proof of original PSX equivalence.
- Do not use this file to add `(F)`, `(D)`, or `(**)` markers by itself.

## Rows

### 1. `(char*)&FmvSceneTriggered`

- source line: `114`
- size expression: `4`
- context: `top-level`

### 2. `(char*)&GLOBAL_lastinvitem`

- source line: `115`
- size expression: `4`
- context: `top-level`

### 3. `(char*)&word`

- source line: `117`
- size expression: `2`
- context: `top-level`

### 4. `(char*)&word`

- source line: `125`
- size expression: `2`
- context: `for (i = 0; i < 10; i++)`

### 5. `(char*)&flipeffect`

- source line: `129`
- size expression: `4`
- context: `top-level`

### 6. `(char*)&fliptimer`

- source line: `134`
- size expression: `4`
- context: `top-level`

### 7. `(char*)&flip_status`

- source line: `135`
- size expression: `4`
- context: `top-level`

### 8. `cd_flags`

- source line: `136`
- size expression: `136`
- context: `top-level`

### 9. `(char*)&CurrentAtmosphere`

- source line: `137`
- size expression: `1`
- context: `top-level`

### 10. `(char*)&word`

- source line: `152`
- size expression: `2`
- context: `for (i = 0; i < number_rooms; i++) / for (j = 0; j < room[i].num_meshes; j++) / if (room[i].mesh[j].static_number >= 50 && / if (k == 0)`

### 11. `(char*)&CurrentSequence`

- source line: `165`
- size expression: `1`
- context: `top-level`

### 12. `(char*)&byte`

- source line: `166`
- size expression: `1`
- context: `top-level`

### 13. `(char*)&camera.fixed[i].flags`

- source line: `174`
- size expression: `2`
- context: `for (i = 0; i < number_cameras; i++)`

### 14. `(char*)&SpotCam[i].flags`

- source line: `179`
- size expression: `2`
- context: `for (i = 0; i < number_spotcams; i++)`

### 15. `(char*)&word`

- source line: `192`
- size expression: `2`
- context: `for (i = 0; i < level_items; i++, item++)`

### 16. `(char*)&packed`

- source line: `213`
- size expression: `2`
- context: `for (i = 0; i < level_items; i++, item++) / if (obj->save_position)`

### 17. `(char*)&packed`

- source line: `215`
- size expression: `2`
- context: `for (i = 0; i < level_items; i++, item++) / if (obj->save_position)`

### 18. `(char*)&packed`

- source line: `217`
- size expression: `2`
- context: `for (i = 0; i < level_items; i++, item++) / if (obj->save_position)`

### 19. `(char*)&byte`

- source line: `220`
- size expression: `1`
- context: `for (i = 0; i < level_items; i++, item++) / if (obj->save_position)`

### 20. `(char*)&item->pos.y_rot`

- source line: `222`
- size expression: `2`
- context: `for (i = 0; i < level_items; i++, item++) / if (obj->save_position)`

### 21. `(char*)&item->pos.x_rot`

- source line: `231`
- size expression: `2`
- context: `for (i = 0; i < level_items; i++, item++) / if (obj->save_position) / if (word & 1)`

### 22. `(char*)&item->pos.z_rot`

- source line: `235`
- size expression: `2`
- context: `for (i = 0; i < level_items; i++, item++) / if (obj->save_position) / if (word & 2)`

### 23. `(char*)&item->speed`

- source line: `239`
- size expression: `2`
- context: `for (i = 0; i < level_items; i++, item++) / if (obj->save_position) / if (word & 0x20)`

### 24. `(char*)&item->fallspeed`

- source line: `243`
- size expression: `2`
- context: `for (i = 0; i < level_items; i++, item++) / if (obj->save_position) / if (word & 0x40)`

### 25. `(char*)&item->current_anim_state`

- source line: `249`
- size expression: `2`
- context: `for (i = 0; i < level_items; i++, item++) / if (obj->save_anim)`

### 26. `(char*)&item->goal_anim_state`

- source line: `250`
- size expression: `2`
- context: `for (i = 0; i < level_items; i++, item++) / if (obj->save_anim)`

### 27. `(char*)&item->required_anim_state`

- source line: `251`
- size expression: `2`
- context: `for (i = 0; i < level_items; i++, item++) / if (obj->save_anim)`

### 28. `(char*)&item->anim_number`

- source line: `255`
- size expression: `2`
- context: `for (i = 0; i < level_items; i++, item++) / if (obj->save_anim) / if (item->object_number == LARA)`

### 29. `(char*)&byte`

- source line: `259`
- size expression: `1`
- context: `for (i = 0; i < level_items; i++, item++) / if (obj->save_anim) / else`

### 30. `(char*)&item->frame_number`

- source line: `263`
- size expression: `2`
- context: `for (i = 0; i < level_items; i++, item++) / if (obj->save_anim)`

### 31. `(char*)&item->item_flags[0]`

- source line: `269`
- size expression: `2`
- context: `for (i = 0; i < level_items; i++, item++) / if (PortSave_LevelFormat >= 4)`

### 32. `(char*)&item->item_flags[1]`

- source line: `271`
- size expression: `2`
- context: `for (i = 0; i < level_items; i++, item++) / if (PortSave_LevelFormat >= 4)`

### 33. `(char*)&item->item_flags[2]`

- source line: `273`
- size expression: `2`
- context: `for (i = 0; i < level_items; i++, item++) / if (PortSave_LevelFormat >= 4)`

### 34. `(char*)&item->item_flags[3]`

- source line: `275`
- size expression: `2`
- context: `for (i = 0; i < level_items; i++, item++) / if (PortSave_LevelFormat >= 4)`

### 35. `(char*)&item->timer`

- source line: `277`
- size expression: `2`
- context: `for (i = 0; i < level_items; i++, item++) / if (PortSave_LevelFormat >= 4)`

### 36. `(char*)&item->trigger_flags`

- source line: `279`
- size expression: `2`
- context: `for (i = 0; i < level_items; i++, item++) / if (PortSave_LevelFormat >= 4)`

### 37. `(char*)&item->hit_points`

- source line: `284`
- size expression: `2`
- context: `for (i = 0; i < level_items; i++, item++) / if (word & 0x4000)`

### 38. `(char*)&flags`

- source line: `289`
- size expression: `4`
- context: `for (i = 0; i < level_items; i++, item++) / if (obj->save_flags)`
