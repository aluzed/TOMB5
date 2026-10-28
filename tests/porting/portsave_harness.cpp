#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include "PORTSAVE.H"
#include "TYPES.H"
#include "STYPES.H"

struct savegame_info savegame;
struct lara_info lara;
char* MGSaveGamePtr;
static char level_blob[8192];
struct ITEM_INFO* lara_item;
unsigned char gfCurrentLevel = 1;
unsigned long GameTimer = 1234;
char JustLoaded = 0;

void SaveLaraData()
{
	/* Keep savegame.Lara zeroed for the harness. */
}

int SaveLevelDataToBuffer(char* buffer, int size)
{
	(void)size;
	/* Exercise the level-data slot without depending on the level loader. */
	if (buffer != NULL && size > (int)sizeof(struct savegame_info))
	{
		buffer[sizeof(struct savegame_info)] = 0x5A;
	}
	return 1;
}

void UpdateLaraRoom(struct ITEM_INFO* item, int height)
{
	(void)height;
	item->room_number = item->room_number;
}

void InitialiseCamera()
{
}

int main(int argc, char** argv)
{
	struct ITEM_INFO item;
	char path[1024];
	FILE* file;
	char garbage[32];

	assert(argc == 2);
	snprintf(path, sizeof(path), "%s", argv[1]);
	setenv("TOMB5_SAVE_PATH", path, 1);
	MGSaveGamePtr = level_blob;
	memset(MGSaveGamePtr, 0, sizeof(level_blob));

	memset(&item, 0, sizeof(item));
	lara_item = &item;
	item.pos.x_pos = 111;
	item.pos.y_pos = 222;
	item.pos.z_pos = 333;
	item.pos.x_rot = 4;
	item.pos.y_rot = 5;
	item.pos.z_rot = 6;
	item.room_number = 7;
	item.current_anim_state = 8;
	item.goal_anim_state = 9;
	item.anim_number = 10;
	item.frame_number = 11;
	item.speed = 12;
	item.fallspeed = 13;
	item.hit_points = 14;

	assert(PortSave_Write() == 1);

	/* A fresh process state must not keep the saved values. */
	memset(&item, 0, sizeof(item));
	lara_item = &item;

	assert(PortSave_Read() == 1);
	PortSave_ApplyPending();
	assert(item.pos.x_pos == 111);
	assert(item.pos.y_pos == 222);
	assert(item.pos.z_pos == 333);
	assert(item.pos.x_rot == 4);
	assert(item.pos.y_rot == 5);
	assert(item.pos.z_rot == 6);
	assert(item.room_number == 7);
	assert(item.current_anim_state == 8);
	assert(item.goal_anim_state == 9);
	assert(item.anim_number == 10);
	assert(item.frame_number == 11);
	assert(item.speed == 12);
	assert(item.fallspeed == 13);
	assert(item.hit_points == 14);

	/* Corruption must fail closed. */
	file = fopen(path, "r+b");
	assert(file != NULL);
	fseek(file, 16, SEEK_SET);
	fread(garbage, 1, sizeof(garbage), file);
	fseek(file, 16, SEEK_SET);
	garbage[0] ^= 0x7F;
	fwrite(garbage, 1, sizeof(garbage), file);
	fclose(file);

	assert(PortSave_Read() == 0);

	/* A bad magic is rejected too. */
	file = fopen(path, "r+b");
	assert(file != NULL);
	fputc('X', file);
	fclose(file);
	assert(PortSave_Read() == 0);

	unlink(path);
	printf("portsave harness OK\n");
	return 0;
}
