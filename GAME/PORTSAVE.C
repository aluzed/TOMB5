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
#define PORTSAVE_VERSION 4u
#define PORTSAVE_V3_VERSION 3u
#define PORTSAVE_LEGACY_VERSION 2u
#define PORTSAVE_LEVEL_DATA_SIZE 8192

/* Declared in GAME/COLLIDE.H for PC_VERSION only, but implemented by the
 * PSXPC_N backend (SPEC_PSXPC_N/COLLIDE_S.C). */
extern void UpdateLaraRoom(struct ITEM_INFO* item, int height);

#pragma pack(push, 1)
/* Version 2 records (466 bytes) are still accepted so existing quick saves
 * remain loadable; they carry no level-state block. */
typedef struct PortSaveRecordV2
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
} PortSaveRecordV2;

/* Version 3 adds a fixed-size level-state block produced by SaveLevelData. */
typedef struct PortSaveRecord
{
	char magic[4];
	uint32_t version;
	struct savegame_info save;
	unsigned char level_data[PORTSAVE_LEVEL_DATA_SIZE];
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
static char port_level_blob[PORTSAVE_LEVEL_DATA_SIZE];
static char port_save_path[1024];
static const char* port_save_message = "";
static int port_save_message_time = 0;

const char* PortSave_Message(void)
{
	return port_save_message;
}

int PortSave_MessageTime(void)
{
	return port_save_message_time;
}

void PortSave_TickMessage(void)
{
	if (port_save_message_time > 0)
	{
		port_save_message_time--;
	}
}

static void PortSave_ShowMessage(const char* message, int frames)
{
	port_save_message = message;
	port_save_message_time = frames;
}

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

static uint32_t PortSave_RecordChecksumV2(const PortSaveRecordV2* record)
{
	const unsigned char* begin = (const unsigned char*)record;
	size_t size = offsetof(PortSaveRecordV2, checksum);
	return PortSave_Checksum(begin, size);
}

int PortSave_Write(void)
{
	PortSaveRecord record;
	FILE* file;
	size_t written;
	int level_bytes;
	char temp_path[1100];

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

	/* Serialise flips, doors, cameras, static meshes and items.  The helper
	 * writes into the level block at sizeof(savegame_info), matching the
	 * layout RestoreLevelData expects. */
	level_bytes = SaveLevelDataToBuffer((char*)record.level_data,
	                                    sizeof(record.level_data));
	if (level_bytes < 0)
	{
		printf("[SAVE] level data does not fit in the save record; nothing written\n");
		PortSave_ShowMessage("Save failed", 90);
		return 0;
	}

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

	if (snprintf(temp_path, sizeof(temp_path), "%s.tmp", PortSave_Path()) >= (int)sizeof(temp_path))
	{
		printf("[SAVE] save path too long for %s\n", PortSave_Path());
		PortSave_ShowMessage("Save failed", 90);
		return 0;
	}

	file = fopen(temp_path, "wb");
	if (file == NULL)
	{
		printf("[SAVE] cannot open %s\n", temp_path);
		PortSave_ShowMessage("Save failed", 90);
		return 0;
	}

	written = fwrite(&record, sizeof(record), 1, file);
	if (fclose(file) != 0 || written != 1)
	{
		printf("[SAVE] write failed for %s\n", temp_path);
		remove(temp_path);
		PortSave_ShowMessage("Save failed", 90);
		return 0;
	}

	/* Keep the previous save intact until the new record is complete. */
	if (rename(temp_path, PortSave_Path()) != 0)
	{
		printf("[SAVE] cannot replace %s\n", PortSave_Path());
		remove(temp_path);
		PortSave_ShowMessage("Save failed", 90);
		return 0;
	}

	PortSave_ShowMessage("Game saved", 90);

	printf("[SAVE] wrote %s: level %d room %d X %d Y %d Z %d, level data %d bytes\n",
	       PortSave_Path(), gfCurrentLevel, record.room, record.x, record.y,
	       record.z, level_bytes);
	return 1;
}

int PortSave_Exists(void)
{
	FILE* file = fopen(PortSave_Path(), "rb");
	if (file == NULL)
	{
		return 0;
	}
	fclose(file);
	return 1;
}

int PortSave_Read(void)
{
	PortSaveRecord record;
	PortSaveRecordV2 legacy;
	FILE* file;
	unsigned char header[8];
	uint32_t version;
	size_t read;
	char* target;

	file = fopen(PortSave_Path(), "rb");
	if (file == NULL)
	{
		printf("[SAVE] no save file at %s\n", PortSave_Path());
		return 0;
	}

	read = fread(header, 1, sizeof(header), file);
	if (read != sizeof(header) || memcmp(header, PORTSAVE_MAGIC, 4) != 0)
	{
		fclose(file);
		printf("[SAVE] invalid save header in %s\n", PortSave_Path());
		return 0;
	}
	memcpy(&version, &header[4], sizeof(version));
	fseek(file, 0, SEEK_SET);

	memset(&record, 0, sizeof(record));
	if (version == PORTSAVE_VERSION || version == PORTSAVE_V3_VERSION)
	{
		read = fread(&record, sizeof(record), 1, file);
		fclose(file);
		if (read != 1 || PortSave_RecordChecksum(&record) != record.checksum)
		{
			printf("[SAVE] checksum mismatch in %s\n", PortSave_Path());
			return 0;
		}
		PortSave_LevelFormat = (version == PORTSAVE_VERSION) ? 4 : 3;
	}
	else if (version == PORTSAVE_LEGACY_VERSION)
	{
		read = fread(&legacy, sizeof(legacy), 1, file);
		fclose(file);
		if (read != 1 || PortSave_RecordChecksumV2(&legacy) != legacy.checksum)
		{
			printf("[SAVE] checksum mismatch in %s\n", PortSave_Path());
			return 0;
		}

		record.version = PORTSAVE_VERSION;
		memcpy(record.magic, legacy.magic, sizeof(record.magic));
		record.save = legacy.save;
		record.x = legacy.x;
		record.y = legacy.y;
		record.z = legacy.z;
		record.x_rot = legacy.x_rot;
		record.y_rot = legacy.y_rot;
		record.z_rot = legacy.z_rot;
		record.room = legacy.room;
		record.current_anim_state = legacy.current_anim_state;
		record.goal_anim_state = legacy.goal_anim_state;
		record.anim_number = legacy.anim_number;
		record.frame_number = legacy.frame_number;
		record.speed = legacy.speed;
		record.fallspeed = legacy.fallspeed;
		record.hit_points = legacy.hit_points;
		PortSave_LevelFormat = 3;
	}
	else
	{
		fclose(file);
		printf("[SAVE] unsupported version %u in %s\n", version, PortSave_Path());
		return 0;
	}

	memcpy(&savegame, &record.save, sizeof(savegame));

	/* sgRestoreGame() reads the level block from MGSaveGamePtr.  The title
	 * path already allocated an 8192-byte buffer; fall back to the local
	 * block if it is not available yet. */
	target = MGSaveGamePtr;
	if (target == NULL)
	{
		target = port_level_blob;
	}
	memcpy(target, record.level_data, sizeof(record.level_data));
	MGSaveGamePtr = target;

	pending_record = record;
	pending_valid = 1;

	PortSave_ShowMessage("Game loaded", 90);
	printf("[SAVE] loaded %s (v%u): level %d room %d X %d Y %d Z %d\n",
	       PortSave_Path(), version, savegame.CurrentLevel, record.room,
	       record.x, record.y, record.z);
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
