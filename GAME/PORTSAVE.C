#include "PORTSAVE.H"

#include "CAMERA.H"
#include "COLLIDE.H"
#include "CONTROL.H"
#include "GAMEFLOW.H"
#include "LARA.H"
#include "SAVEGAME.H"
#include "TYPES.H"

#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define PORTSAVE_MAGIC "T5P2"
#define PORTSAVE_VERSION 2u

/* Declared in GAME/COLLIDE.H for PC_VERSION only, but implemented by the
 * PSXPC_N backend (SPEC_PSXPC_N/COLLIDE_S.C). */
extern void UpdateLaraRoom(struct ITEM_INFO* item, int height);

#pragma pack(push, 1)
typedef struct PortSaveRecord
{
	char magic[4];
	uint32_t version;
	struct savegame_info save;
	int32_t x;
	int32_t y;
	int32_t z;
	int16_t x_rot;
	int16_t y_rot;
	int16_t z_rot;
	int16_t room;
	int16_t current_anim_state;
	int16_t goal_anim_state;
	int16_t anim_number;
	int16_t frame_number;
	int16_t speed;
	int16_t fallspeed;
	int16_t hit_points;
	uint32_t checksum;
} PortSaveRecord;
#pragma pack(pop)

static int save_requested = 0;
static int load_requested = 0;
static int pending_valid = 0;
static PortSaveRecord pending_record;
static char port_save_path[1024];

const char* PortSave_Path(void)
{
	const char* override_path;
	if (port_save_path[0])
	{
		return port_save_path;
	}

	override_path = getenv("TOMB5_SAVE_PATH");
	if (override_path && override_path[0])
	{
		snprintf(port_save_path, sizeof(port_save_path), "%s", override_path);
	}
	else
	{
		snprintf(port_save_path, sizeof(port_save_path), "%s", PORTSAVE_DEFAULT_FILE);
	}
	return port_save_path;
}

void PortSave_RequestSave(void)
{
	save_requested = 1;
}

void PortSave_RequestLoad(void)
{
	load_requested = 1;
}

int PortSave_TakeSaveRequest(void)
{
	int requested = save_requested;
	save_requested = 0;
	return requested;
}

int PortSave_TakeLoadRequest(void)
{
	int requested = load_requested;
	load_requested = 0;
	return requested;
}

static uint32_t PortSave_Checksum(const unsigned char* data, size_t size)
{
	uint32_t sum = 2166136261u;
	size_t i;
	for (i = 0; i < size; ++i)
	{
		sum ^= data[i];
		sum *= 16777619u;
	}
	return sum;
}

static uint32_t PortSave_RecordChecksum(const PortSaveRecord* record)
{
	const unsigned char* begin = (const unsigned char*)record;
	size_t size = offsetof(PortSaveRecord, checksum);
	return PortSave_Checksum(begin, size);
}

int PortSave_Write(void)
{
	PortSaveRecord record;
	FILE* file;
	size_t written;

	if (lara_item == NULL)
	{
		printf("[SAVE] no Lara item; nothing written\n");
		return 0;
	}

	memset(&record, 0, sizeof(record));
	record.magic[0] = PORTSAVE_MAGIC[0];
	record.magic[1] = PORTSAVE_MAGIC[1];
	record.magic[2] = PORTSAVE_MAGIC[2];
	record.magic[3] = PORTSAVE_MAGIC[3];
	record.version = PORTSAVE_VERSION;

	savegame.Game.Timer = GameTimer;
	savegame.CurrentLevel = gfCurrentLevel;
	/* Refreshes savegame.Lara from the live lara_info (and restores the
	 * pointer fields afterwards). */
	SaveLaraData();
	record.save = savegame;

	record.x = lara_item->pos.x_pos;
	record.y = lara_item->pos.y_pos;
	record.z = lara_item->pos.z_pos;
	record.x_rot = lara_item->pos.x_rot;
	record.y_rot = lara_item->pos.y_rot;
	record.z_rot = lara_item->pos.z_rot;
	record.room = lara_item->room_number;
	record.current_anim_state = lara_item->current_anim_state;
	record.goal_anim_state = lara_item->goal_anim_state;
	record.anim_number = lara_item->anim_number;
	record.frame_number = lara_item->frame_number;
	record.speed = lara_item->speed;
	record.fallspeed = lara_item->fallspeed;
	record.hit_points = lara_item->hit_points;
	record.checksum = PortSave_RecordChecksum(&record);

	file = fopen(PortSave_Path(), "wb");
	if (file == NULL)
	{
		printf("[SAVE] cannot open %s\n", PortSave_Path());
		return 0;
	}

	written = fwrite(&record, sizeof(record), 1, file);
	fclose(file);

	if (written != 1)
	{
		printf("[SAVE] write failed for %s\n", PortSave_Path());
		return 0;
	}

	printf("[SAVE] wrote %s: level %d room %d X %d Y %d Z %d\n",
	       PortSave_Path(), gfCurrentLevel, record.room, record.x, record.y, record.z);
	return 1;
}

int PortSave_Read(void)
{
	PortSaveRecord record;
	FILE* file;
	size_t read;

	file = fopen(PortSave_Path(), "rb");
	if (file == NULL)
	{
		printf("[SAVE] no save file at %s\n", PortSave_Path());
		return 0;
	}

	read = fread(&record, sizeof(record), 1, file);
	fclose(file);

	if (read != 1 || memcmp(record.magic, PORTSAVE_MAGIC, 4) != 0 ||
	    record.version != PORTSAVE_VERSION)
	{
		printf("[SAVE] invalid save header in %s\n", PortSave_Path());
		return 0;
	}

	if (PortSave_RecordChecksum(&record) != record.checksum)
	{
		printf("[SAVE] checksum mismatch in %s\n", PortSave_Path());
		return 0;
	}

	memcpy(&savegame, &record.save, sizeof(savegame));
	pending_record = record;
	pending_valid = 1;

	printf("[SAVE] loaded %s: level %d room %d X %d Y %d Z %d\n",
	       PortSave_Path(), savegame.CurrentLevel, record.room, record.x, record.y, record.z);
	return 1;
}

void PortSave_ApplyPending(void)
{
	PortSaveRecord* record;

	if (!pending_valid || lara_item == NULL)
	{
		return;
	}

	record = &pending_record;
	lara_item->pos.x_pos = record->x;
	lara_item->pos.y_pos = record->y;
	lara_item->pos.z_pos = record->z;
	lara_item->pos.x_rot = record->x_rot;
	lara_item->pos.y_rot = record->y_rot;
	lara_item->pos.z_rot = record->z_rot;
	lara_item->room_number = record->room;
	lara_item->current_anim_state = record->current_anim_state;
	lara_item->goal_anim_state = record->goal_anim_state;
	lara_item->anim_number = record->anim_number;
	lara_item->frame_number = record->frame_number;
	lara_item->speed = record->speed;
	lara_item->fallspeed = record->fallspeed;
	lara_item->hit_points = record->hit_points;

	UpdateLaraRoom(lara_item, 0);
	InitialiseCamera();
	JustLoaded = 1;
	pending_valid = 0;

	printf("[SAVE] applied saved position: room %d X %ld Y %ld Z %ld\n",
	       lara_item->room_number, lara_item->pos.x_pos, lara_item->pos.y_pos,
	       lara_item->pos.z_pos);
}
