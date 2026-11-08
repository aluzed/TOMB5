#include "SAVEGAME.H"

#include "CONTROL.H"
#include "GAMEFLOW.H"
#include "ITEMS.H"
#include "MALLOC.H"

#include "SPECIFIC.H"
#include "SWITCH.H"
#include "TRAPS.H"
#include "TYPES.H"

#ifdef PC_VERSION
#include "GLOBAL.H"
#include "FILE.H"
#include "GAME.H"
#else
#include "SETUP.H"
#include "ROOMLOAD.H"
#endif

#if !SAT_VERSION
#include <stdio.h>
#include <string.h>
#endif
#include "NEWINV2.H"
#include "DRAW.H"
#include "CAMERA.H"
#include "SPOTCAM.H"
#include "LARA.H"

#include <stdlib.h>

/* Declared for PC_VERSION in ITEMS.H, but implemented by the PSXPC_N backend. */
extern void ItemNewRoom(short item_num, short room_number);

#if PSX_VERSION || PSXPC_VERSION || SAT_VERSION
#include "MISC.H"
#endif

static int PortSaveDebugEnabled(void)
{
	static int enabled = -1;
	if (enabled < 0)
	{
		enabled = getenv("TOMB5_SAVE_DEBUG") != NULL;
	}
	return enabled;
}


#if PSXPC_TEST
#include <stdint.h>
#elif PSX_VERSION || SAT_VERSION
typedef unsigned int uintptr_t;
#endif


char FromTitle = 0; // offset 0xA14AC
char JustLoaded = 0; // offset 0xA14AD
int PortSave_LevelFormat = 4;
char* MGSaveGamePtr; // offset 0xA3924
static int SGcount; // offset 0xA391C
static char* SGpoint; // offset 0xA3920
static int SGlimit = 0;
static int SGread_limit = 0;
struct savegame_info savegame;

#define Write(a, b) WriteSG((char*)a, b)

void sgRestoreGame()//55B88, 55FEC (F)
{
	SGcount = 0;
	SGpoint = &MGSaveGamePtr[sizeof(struct savegame_info)];
	GameTimer = savegame.Game.Timer;
	gfCurrentLevel = savegame.CurrentLevel;

	SGread_limit = 8192 - (int)sizeof(struct savegame_info);
	RestoreLevelData(1);
	SGread_limit = 0;
	RestoreLaraData(1);
}

void sgSaveGame()//55AF8(<), 55F5C(<) (F)
{
	SGpoint = &MGSaveGamePtr[sizeof(struct savegame_info)];
	SGcount = 0;

	savegame.Game.Timer = GameTimer;
	savegame.CurrentLevel = gfCurrentLevel;

	SaveLevelData(1);
	SaveLaraData();

	MGSaveGamePtr[7678] = GetRandomControl();
	
	memcpy(&MGSaveGamePtr, &savegame, sizeof(struct savegame_info));
	savegame.Checksum = GameTimer;

	return;
}

void RestoreLevelData(int FullSave)//54B08, 54F6C (F)
{
	int i;
	int j;
	int k;
	int flags;
	short word;
	unsigned char byte;
	short new_room;
	struct ITEM_INFO* item;

	ReadSG((char*)&FmvSceneTriggered, 4);
	ReadSG((char*)&GLOBAL_lastinvitem, 4);

	ReadSG((char*)&word, 2);
	for (i = 0; i < 10; i++)
	{
		flip_stats[i] = (word >> i) & 1;
	}

	for (i = 0; i < 10; i++)
	{
		ReadSG((char*)&word, 2);
		flipmap[i] = word << 8;
	}

	ReadSG((char*)&flipeffect, 4);
	/* flipeffect is a one-shot trigger: restoring it would call the effect
	 * routine with a NULL item on the next frame (observed: flipeffect=0 ->
	 * turn180_effect(NULL) SIGSEGV).  Consume the field but disarm it. */
	flipeffect = -1;
	ReadSG((char*)&fliptimer, 4);
	ReadSG((char*)&flip_status, 4);
	ReadSG(cd_flags, 136);
	ReadSG((char*)&CurrentAtmosphere, 1);

	/* Static-mesh flags are packed with the same bit order as SaveLevelData:
	 * only static numbers 50..59 are serialised, 16 bits per word. */
	word = 0;
	k = 0;
	for (i = 0; i < number_rooms; i++)
	{
		for (j = 0; j < room[i].num_meshes; j++)
		{
			if (room[i].mesh[j].static_number >= 50 &&
			    room[i].mesh[j].static_number <= 59)
			{
				if (k == 0)
				{
					ReadSG((char*)&word, 2);
				}
				room[i].mesh[j].Flags = (room[i].mesh[j].Flags & ~1) |
				                        ((word >> k) & 1);
				k++;
				if (k == 16)
				{
					k = 0;
				}
			}
		}
	}

	ReadSG((char*)&CurrentSequence, 1);
	ReadSG((char*)&byte, 1);
	for (i = 0; i < 6; i++)
	{
		SequenceUsed[i] = (byte >> i) & 1;
	}

	for (i = 0; i < number_cameras; i++)
	{
		ReadSG((char*)&camera.fixed[i].flags, 2);
	}

	for (i = 0; i < number_spotcams; i++)
	{
		ReadSG((char*)&SpotCam[i].flags, 2);
	}

	if (PortSaveDebugEnabled())
	{
		printf("[SAVE] restore camera end at %d bytes\n", SGcount);
	}

	item = &items[0];
	for (i = 0; i < level_items; i++, item++)
	{
		struct object_info* obj;

		ReadSG((char*)&word, 2);

		if (word == 0x2000)
		{
			item->flags |= IFLAG_KILLED | IFLAG_INVISIBLE;
			item->status = ITEM_INVISIBLE;
			continue;
		}

		if (!(word & 0x8000))
		{
			continue;
		}

		obj = &objects[item->object_number];
		new_room = item->room_number;

		if (obj->save_position)
		{
			short packed;

			ReadSG((char*)&packed, 2);
			item->pos.x_pos = (packed << 1) | ((word & 4) ? 1 : 0);
			ReadSG((char*)&packed, 2);
			item->pos.y_pos = (packed << 1) | ((word & 8) ? 1 : 0);
			ReadSG((char*)&packed, 2);
			item->pos.z_pos = (packed << 1) | ((word & 0x10) ? 1 : 0);

			ReadSG((char*)&byte, 1);
			new_room = byte;
			ReadSG((char*)&item->pos.y_rot, 2);

			item->pos.x_rot = 0;
			item->pos.z_rot = 0;
			item->speed = 0;
			item->fallspeed = 0;

			if (word & 1)
			{
				ReadSG((char*)&item->pos.x_rot, 2);
			}
			if (word & 2)
			{
				ReadSG((char*)&item->pos.z_rot, 2);
			}
			if (word & 0x20)
			{
				ReadSG((char*)&item->speed, 2);
			}
			if (word & 0x40)
			{
				ReadSG((char*)&item->fallspeed, 2);
			}
		}

		if (obj->save_anim)
		{
			ReadSG((char*)&item->current_anim_state, 2);
			ReadSG((char*)&item->goal_anim_state, 2);
			ReadSG((char*)&item->required_anim_state, 2);

			if (item->object_number == LARA)
			{
				ReadSG((char*)&item->anim_number, 2);
			}
			else
			{
				ReadSG((char*)&byte, 1);
				item->anim_number = obj->anim_index + byte;
			}

			ReadSG((char*)&item->frame_number, 2);
		}

		if (PortSave_LevelFormat >= 4)
		{
			if (word & 0x80)
				ReadSG((char*)&item->item_flags[0], 2);
			if (word & 0x100)
				ReadSG((char*)&item->item_flags[1], 2);
			if (word & 0x200)
				ReadSG((char*)&item->item_flags[2], 2);
			if (word & 0x400)
				ReadSG((char*)&item->item_flags[3], 2);
			if (word & 0x800)
				ReadSG((char*)&item->timer, 2);
			if (word & 0x1000)
				ReadSG((char*)&item->trigger_flags, 2);
		}

		if (word & 0x4000)
		{
			ReadSG((char*)&item->hit_points, 2);
		}

		if (obj->save_flags)
		{
			ReadSG((char*)&flags, 4);
			item->flags = (short)(flags & 0xFFFF);
			item->active = (flags >> 16) & 1;
			item->status = (flags >> 17) & 3;
			item->gravity_status = (flags >> 19) & 1;
			item->hit_status = (flags >> 20) & 1;
			item->collidable = (flags >> 21) & 1;
			item->looked_at = (flags >> 22) & 1;
			item->dynamic_light = (flags >> 23) & 1;
			item->poisoned = (flags >> 24) & 1;
			item->ai_bits = (flags >> 25) & 0x1F;
			item->really_active = (flags >> 30) & 1;
		}

		if (obj->save_position && new_room >= 0 && new_room < number_rooms &&
		    new_room != item->room_number)
		{
			ItemNewRoom(i, new_room);
		}
	}

	if (PortSaveDebugEnabled())
	{
		printf("[SAVE] restore items end at %d bytes\n", SGcount);
	}
}

void WriteSG(char* pointer, int size)//536A0, 53B04 (F)
{
	if (SGlimit > 0 && SGcount + size > SGlimit)
	{
		/* The destination buffer is full.  Keep counting so the caller can
		 * detect the overflow, but do not write past the buffer. */
		SGcount += size;
		return;
	}

	SGcount += size;

	if (size > 0)
	{
		while (size-- > 0)
		{
			*SGpoint++ = *pointer++;
		}
	}
}

int SaveLevelDataToBuffer(char* buffer, int size)// port helper
{
	char* old = MGSaveGamePtr;
	char* old_point = SGpoint;
	int old_count = SGcount;
	int written;

	if (buffer == NULL || size <= (int)sizeof(struct savegame_info))
	{
		return -1;
	}

	MGSaveGamePtr = buffer;
	SGpoint = &MGSaveGamePtr[sizeof(struct savegame_info)];
	SGcount = 0;
	SGlimit = size - (int)sizeof(struct savegame_info);
	SaveLevelData(1);
	written = SGcount;
	SGlimit = 0;
	SGpoint = old_point;
	SGcount = old_count;
	MGSaveGamePtr = old;

	if (written > size - (int)sizeof(struct savegame_info))
	{
		return -1;
	}
	return written;
}

void SaveLevelData(int FullSave)//53AAC, 53F10 (F)
{
	int i;
	short word = 0;
	unsigned char byte = 0;

	Write(&FmvSceneTriggered, 4);
	Write(&GLOBAL_lastinvitem, 4);

	for(i = 0; i < 10; i++)
	{
		if (flip_stats[i])
			word |= 1 << i;
	}
	Write(&word, 2);

	for(i = 0; i < 10; i++)
	{
		word = flipmap[i] >> 8;
		Write(&word, 2);
	}

	Write(&flipeffect, 4);
	Write(&fliptimer, 4);
	Write(&flip_status, 4);
	Write(cd_flags, 136);
	Write(&CurrentAtmosphere, 1);

	word = 0;
	if (number_rooms > 0)
	{
		int k = 0;
		for(i = 0; i < number_rooms; i++)
		{
			int j;		
			for (j = 0; j < room[i].num_meshes; j++)
			{
				if (room[i].mesh[j].static_number >= 50 && room[i].mesh[j].static_number <= 59)
				{
					word |= (room[i].mesh[j].Flags & 1) << k++;

					if (k == 16)
					{
						Write(&word, 2);
						k = 0;
						word = 0;
					}
				}
			}
		}

		if (k != 0)
			Write(&word, 2);
	}

	Write(&CurrentSequence, 1);

	byte = 0;
	for (i = 0; i < 6; i++)
	{
		byte |= SequenceUsed[i] << i;
	}
	Write(&byte, 1);

	for (i = 0; i < number_cameras; i++)
	{
		Write(&camera.fixed[i].flags, 2);
	}

	for(i = 0; i < number_spotcams; i++)
	{
		Write(&SpotCam[i].flags, 2);
	}
	
	if (PortSaveDebugEnabled())
	{
		printf("[SAVE] save camera end at %d bytes\n", SGcount);
	}

	struct ITEM_INFO* item = &items[0];
	for(i = 0; i < level_items; i++, item++)
	{
		struct object_info* obj = &objects[item->object_number];

		if (item->flags & IFLAG_KILLED)
		{
			word = 0x2000;
			Write(&word, 2);
		}
		else if (item->flags & (IFLAG_ACTIVATION_MASK | IFLAG_INVISIBLE | 0x20) || item->object_number == LARA && FullSave)
		{
			word = 0x8000;

			if (item->pos.x_rot != 0)
				word |= 1;

			if (item->pos.z_rot != 0)
				word |= 2;

			if (item->pos.x_pos & 1)
				word |= 4;

			if (item->pos.y_pos & 1)
				word |= 8;

			if (item->pos.z_pos & 1)
				word |= 0x10;

			if (item->speed != 0)
				word |= 0x20;

			if (item->fallspeed != 0)
				word |= 0x40;

			if (item->item_flags[0])
				word |= 0x80;

			if (item->item_flags[1])
				word |= 0x100;

			if (item->item_flags[2])
				word |= 0x200;

			if (item->item_flags[3])
				word |= 0x400;

			if (item->timer)
				word |= 0x800;

			if (item->trigger_flags)
				word |= 0x1000;

			if (obj->save_hitpoints)
				word |= 0x4000;

			Write(&word, 2);

			if (obj->save_position)
			{
				short packed = item->pos.x_pos >> 1;
				Write(&packed, 2);
				packed = item->pos.y_pos >> 1;
				Write(&packed, 2);
				packed = item->pos.z_pos >> 1;
				Write(&packed, 2);

				Write(&item->room_number, 1);

				Write(&item->pos.y_rot, 2);

				if (word & 1)
					Write(&item->pos.x_rot, 2);
				if (word & 2)
					Write(&item->pos.z_rot, 2);
				if (word & 0x20)
					Write(&item->speed, 2);
				if (word & 0x40)
					Write(&item->fallspeed, 2);
			}

			if (obj->save_anim)
			{
				Write(&item->current_anim_state, 2);
				Write(&item->goal_anim_state, 2);
				Write(&item->required_anim_state, 2);

				if (item->object_number == LARA)
				{
					Write(&item->anim_number, 2);
				}
				else
				{
					byte = item->anim_number - obj->anim_index;
					Write(&byte, 1);
				}

				Write(&item->frame_number, 2);
			}

			if (word & 0x80)
				Write(&item->item_flags[0], 2);
			if (word & 0x100)
				Write(&item->item_flags[1], 2);
			if (word & 0x200)
				Write(&item->item_flags[2], 2);
			if (word & 0x400)
				Write(&item->item_flags[3], 2);
			if (word & 0x800)
				Write(&item->timer, 2);
			if (word & 0x1000)
				Write(&item->trigger_flags, 2);

			if (word & 0x4000)
				Write(&item->hit_points, 2);

			if (obj->save_flags)
			{
				int flags = (unsigned short)item->flags | ((item->active
					| (item->status << 1)
					| (item->gravity_status << 3)
					| (item->hit_status << 4)
					| (item->collidable << 5)
					| (item->looked_at << 6)
					| (item->dynamic_light << 7)
					| (item->poisoned << 8)
					| (item->ai_bits << 9)
					| (item->really_active << 14)) << 16);
				Write(&flags, 4);
			}
		}
		else
		{
			/* Inactive items still occupy one word in the stream so the
			 * reader can walk the item array without a separate count. */
			word = 0;
			Write(&word, 2);
		}

	}

	if (PortSaveDebugEnabled())
	{
		printf("[SAVE] save items end at %d bytes\n", SGcount);
	}

}

void RestoreLaraData(int FullSave)//538D0(<), 53D34(<) (F)
{
	struct ITEM_INFO* item;
	char flag;
	int i;

	if (!FullSave)
	{
		savegame.Lara.item_number = lara.item_number;
		if (savegame.Lara.IsMoving)
		{
			savegame.Lara.IsMoving = 0;
			savegame.Lara.gun_status = LG_NO_ARMS;
		}
	}
	memcpy(&lara, &savegame.Lara, sizeof(struct lara_info));
	lara.target = NULL;
	lara.spaz_effect = NULL;
	lara.right_arm.frame_base = (short*)((char*)lara.right_arm.frame_base + (uintptr_t)objects[PISTOLS_ANIM].frame_base);
	lara.left_arm.frame_base = (short*)((char *)lara.left_arm.frame_base + (uintptr_t)objects[PISTOLS_ANIM].frame_base);
	lara.GeneralPtr = (char *)lara.GeneralPtr + (uintptr_t)malloc_buffer;
	if (lara.burn)
	{
		lara.burn = 0;
		flag = 0;
		if (lara.BurnSmoke)
		{
			lara.BurnSmoke = 0;
			flag = 1;
		}
		LaraBurn();
		if (flag)
		{
			lara.BurnSmoke = 1;
		}
	}
	if (lara.weapon_item != -1)
	{
		lara.weapon_item = CreateItem();
		item = &items[lara.weapon_item];
		item->object_number = savegame.WeaponObject;
		item->anim_number = savegame.WeaponAnim;
		item->frame_number = savegame.WeaponFrame;
		item->current_anim_state = savegame.WeaponCurrent;
		item->goal_anim_state = savegame.WeaponGoal;
		item->status = ITEM_ACTIVE;
		item->room_number = 255;
	}
	
	for (i = 0; i < 15; i++)
	{
		lara.mesh_ptrs[i] = (short*)((char*)mesh_base + (uintptr_t)lara.mesh_ptrs[i]);
	}

	_CutSceneTriggered1 = savegame.CutSceneTriggered1;
	_CutSceneTriggered2 = savegame.CutSceneTriggered2;
}

void SaveLaraData()//53738(<), 53B9C(<) (F)
{
	struct ITEM_INFO* item;
	int i;

	for (i = 0; i < 15; i++)
	{
		lara.mesh_ptrs[i] = (short*)((char*)lara.mesh_ptrs[i] - (uintptr_t)mesh_base);
	}

	lara.left_arm.frame_base = (short*)((char *)lara.left_arm.frame_base - (uintptr_t)objects[PISTOLS_ANIM].frame_base);
	lara.right_arm.frame_base = (short*)((char *)lara.right_arm.frame_base - (uintptr_t)objects[PISTOLS_ANIM].frame_base);
	lara.GeneralPtr = (char *)lara.GeneralPtr - (uintptr_t)malloc_buffer;
	memcpy(&savegame.Lara, &lara, sizeof(savegame.Lara));
	
	for (i = 0; i < 15; i++)
	{
		lara.mesh_ptrs[i] = (short*)((char*)mesh_base + (uintptr_t)lara.mesh_ptrs[i]);
	}

	lara.left_arm.frame_base = (short*)((char *)lara.left_arm.frame_base + (uintptr_t)objects[PISTOLS_ANIM].frame_base);
	lara.right_arm.frame_base = (short*)((char *)lara.right_arm.frame_base + (uintptr_t)objects[PISTOLS_ANIM].frame_base);
	lara.GeneralPtr = (char *)lara.GeneralPtr + (uintptr_t)malloc_buffer;

	if (lara.weapon_item == -1)
	{
		savegame.CutSceneTriggered1 = _CutSceneTriggered1;
		savegame.CutSceneTriggered2 = _CutSceneTriggered2;
	}
	else
	{
		item = &items[lara.weapon_item];
		savegame.WeaponObject = item->object_number;
		savegame.WeaponAnim = item->anim_number;
		savegame.WeaponFrame = item->frame_number;
		savegame.WeaponCurrent = item->current_anim_state;
		savegame.WeaponGoal = item->goal_anim_state;
		savegame.CutSceneTriggered1 = _CutSceneTriggered1;
		savegame.CutSceneTriggered2 = _CutSceneTriggered2;
	}
}

int CheckSumValid(char* buffer)//53720(<), 53B84(<) (F)
{
	return (*(short*)buffer ^ *(short*)(buffer + 0x1DFE)) < 1;
}

void ReadSG(char* pointer, int size)//536E0, 53B44 (F)
{
	if (SGread_limit > 0 && SGcount + size > SGread_limit)
	{
		SGcount += size;
		return;
	}

	SGcount += size;
	
	if (size > 0)
	{
		while (size-- > 0)
		{
			*pointer++ = *SGpoint++;
		}
	}

	return;
}

