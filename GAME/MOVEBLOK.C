#include "MOVEBLOK.H"

#include "BOX.H"
#include "CAMERA.H"
#include "COLLIDE.H"
#include "CONTROL.H"
#include "DRAW.H"
#include "EFFECTS.H"
#include "ITEMS.H"
#include "LARA.H"
#include "OBJECTS.H"
#include "SETUP.H"
#include "SOUND.H"
#include "SPECIFIC.H"

#if PSX_VERSION || PSXPC_VERSION || SAT_VERSION
#include "GETSTUFF.H"
#include "CALCLARA.H"
#include "COLLIDE_S.H"
#include "MATHS.H"
#include "GTEREG.H"
#include "PSXINPUT.H"
#endif

#include <stdlib.h>

/* Portage PSXPC_N de game/moveblok.cpp (source PC TR5).
 * Le bloc poussable n'avait aucun handler dans le port : le premier
 * secret de The Colosseum etait donc inaccessible. */

static short MovingBlockBounds[12] = { 0, 0, -256, 0, 0, 0, -1820, 1820, -5460, 5460, -1820, 1820 };
static struct PHD_VECTOR MovingBlockPos = { 0, 0, 0 };

static void ClearMovableBlockSplitters(long x, long y, long z, short room_number)
{
	struct FLOOR_INFO* floor;
	short room_num, height;

	floor = GetFloor(x, y, z, &room_number);
	boxes[floor->box].overlap_index = ~0x4000;
	height = boxes[floor->box].height;
	room_num = room_number;
	floor = GetFloor(x + 1024, y, z, &room_number);

	if (floor->box != 0x7FF)
	{
		if (boxes[floor->box].height == height && boxes[floor->box].overlap_index & 0x8000 && boxes[floor->box].overlap_index & 0x4000)
			ClearMovableBlockSplitters(x + 1024, y, z, room_number);
	}

	room_number = room_num;
	floor = GetFloor(x - 1024, y, z, &room_number);

	if (floor->box != 0x7FF)
	{
		if (boxes[floor->box].height == height && boxes[floor->box].overlap_index & 0x8000 && boxes[floor->box].overlap_index & 0x4000)
			ClearMovableBlockSplitters(x - 1024, y, z, room_number);
	}

	room_number = room_num;
	floor = GetFloor(x, y, z + 1024, &room_number);

	if (floor->box != 0x7FF)
	{
		if (boxes[floor->box].height == height && boxes[floor->box].overlap_index & 0x8000 && boxes[floor->box].overlap_index & 0x4000)
			ClearMovableBlockSplitters(x, y, z + 1024, room_number);
	}

	room_number = room_num;
	floor = GetFloor(x, y, z - 1024, &room_number);

	if (floor->box != 0x7FF)
	{
		if (boxes[floor->box].height == height && boxes[floor->box].overlap_index & 0x8000 && boxes[floor->box].overlap_index & 0x4000)
			ClearMovableBlockSplitters(x, y, z - 1024, room_number);
	}
}

/* Initialiseur des sols/blocs qui s'effondrent (CRUMBLING_FLOOR,
 * FALLING_BLOCK). TRAPS.C ne peut pas encore etre recompile (COLLIDE.C
 * depend d'un MoveLaraPositionToItem absent des objets de build57), donc
 * ce petit helper vit ici en attendant un build propre. */
/* Meme raison : SetLaraPosition/InterpolateLaraAngle manquent dans le
 * COLLIDE.C.o de build57. Definitions faibles, remplacees par celles de
 * COLLIDE.C lors d'une compilation propre. */
static short PortInterpolateLaraAngle(short current, short target, short step)
{
	short diff = (short)(target - current);

	if (step < diff)
		return (short)(current + step);

	if (diff < -step)
		return (short)(current - step);

	return target;
}

__attribute__((weak)) int SetLaraPosition(struct PHD_3DPOS* dst, struct PHD_3DPOS* target, int distance, short step)
{
	long dx = target->x_pos - dst->x_pos;
	long dy = target->y_pos - dst->y_pos;
	long dz = target->z_pos - dst->z_pos;
	long dist = phd_sqrt_asm(dx * dx + dy * dy + dz * dz);

	if (dist <= distance)
	{
		dst->x_pos = target->x_pos;
		dst->y_pos = target->y_pos;
		dst->z_pos = target->z_pos;
	}
	else
	{
		long ratio = ((long)distance << 16) / dist;

		dst->x_pos += (dx * ratio) >> 16;
		dst->y_pos += (dy * ratio) >> 16;
		dst->z_pos += (dz * ratio) >> 16;
	}

	if (!lara.IsMoving)
	{
		if (lara.water_status == LW_UNDERWATER)
		{
			lara.MoveCount = 0;
			lara.IsMoving = 1;
		}
		else
		{
			long angle = phd_atan_asm(dst->x_pos - target->x_pos, dst->z_pos - target->z_pos) + 8192;
			int quadrant = (int)(((angle >> 14) - ((target->y_rot + 8192) >> 14)) & 3);
			int anim;
			short state;

			switch (quadrant)
			{
			case 0:
				anim = 65;
				state = 22;
				break;
			case 1:
				anim = 1;
				state = 0;
				break;
			case 2:
				anim = 67;
				state = 21;
				break;
			default:
				anim = 40;
				state = 16;
				break;
			}

			lara_item->anim_number = (short)anim;
			lara_item->current_anim_state = state;
			lara_item->goal_anim_state = state;
			lara_item->frame_number = anims[anim].frame_base;
			lara.gun_status = LG_HANDS_BUSY;
			lara.MoveCount = 0;
			lara.IsMoving = 1;
		}
	}

	dst->x_rot = PortInterpolateLaraAngle(dst->x_rot, target->x_rot, step);
	dst->y_rot = PortInterpolateLaraAngle(dst->y_rot, target->y_rot, step);
	dst->z_rot = PortInterpolateLaraAngle(dst->z_rot, target->z_rot, step);

	return dst->x_pos == target->x_pos && dst->y_pos == target->y_pos && dst->z_pos == target->z_pos &&
		dst->x_rot == target->x_rot && dst->y_rot == target->y_rot && dst->z_rot == target->z_rot;
}

/* Le COLLIDE.C.o de build57 ne contient pas MoveLaraPositionToItem, alors
 * que TRAPS.C (FloorTrapDoorCollision) le reference. Definition faible :
 * elle satisfait l'edition de liens actuelle et une future compilation de
 * COLLIDE.C (definition forte) la remplacera sans conflit. */
__attribute__((weak)) int MoveLaraPositionToItem(struct PHD_VECTOR* vector, struct ITEM_INFO* item, struct ITEM_INFO* l)
{
	struct PHD_3DPOS target;
	struct FLOOR_INFO* floor;
	short room, height;
	long dx, dy, dz;

#if PSX_VERSION || PSXPC_VERSION || PSXPC_TEST || SAT_VERSION
	mPushUnitMatrix();
	mRotYXZ(item->pos.y_rot, item->pos.x_rot, item->pos.z_rot);

	IR1 = vector->x;
	IR2 = vector->y;
	IR3 = vector->z;
	TRX = item->pos.x_pos;
	TRY = item->pos.y_pos;
	TRZ = item->pos.z_pos;

	docop2(0x498012);

	target.x_pos = MAC1;
	target.y_pos = MAC2;
	target.z_pos = MAC3;

	mPopMatrix();
#else
	target.x_pos = item->pos.x_pos + ((vector->x * COS(item->pos.y_rot) - vector->z * SIN(item->pos.y_rot)) >> W2V_SHIFT);
	target.y_pos = item->pos.y_pos + vector->y;
	target.z_pos = item->pos.z_pos + ((vector->x * SIN(item->pos.y_rot) + vector->z * COS(item->pos.y_rot)) >> W2V_SHIFT);
#endif

	target.x_rot = item->pos.x_rot;
	target.y_rot = item->pos.y_rot;
	target.z_rot = item->pos.z_rot;

	if (item->object_number == 354 || item->object_number == 241)
	{
		room = l->room_number;
		floor = GetFloor(target.x_pos, target.y_pos, target.z_pos, &room);
		height = GetHeight(floor, target.x_pos, target.y_pos, target.z_pos);

		if (ABS(height - l->pos.y_pos) >= 513)
		{
			if (lara.IsMoving)
			{
				lara.IsMoving = 0;
				lara.gun_status = LG_NO_ARMS;
			}

			return 0;
		}

		dx = target.x_pos - l->pos.x_pos;
		dy = target.y_pos - l->pos.y_pos;
		dz = target.z_pos - l->pos.z_pos;

		if (phd_sqrt_asm(dx * dx + dy * dy + dz * dz) < 128)
			return 1;
	}

	return SetLaraPosition(&l->pos, &target, 12, 364);
}

void PortInitialiseFallingBlock2(short item_number)
{
	items[item_number].mesh_bits = 1;
}

void InitialiseMovingBlock(short item_number)
{
	struct ITEM_INFO* item = &items[item_number];

	ClearMovableBlockSplitters(item->pos.x_pos, item->pos.y_pos, item->pos.z_pos, item->room_number);
}

/* Sous-ensemble de GetCollidedObjects (game/collide.cpp) : la version
 * globale du port est un stub, et les blocs poussables ne consultent que
 * la liste d'items (statiques = NULL). */
static short PortCollidedObjects(struct ITEM_INFO* item, long rad, int noInvisible, struct ITEM_INFO** StoredItems)
{
	struct ITEM_INFO* item2;
	struct room_info* r;
	short* doors;
	short* bounds;
	long j, sy, cy, dx, dy, dz, num;
	short rooms[22];
	short switch_bounds[6];
	short room_count, items_count, item_number, next_item;

	rooms[0] = camera.pos.room_number;
	r = &room[rooms[0]];
	doors = r->door;
	room_count = 1;
	items_count = 0;

	if (doors)
	{
		for (int i = *doors++; i > 0; i--, doors += 16)
		{
			for (j = 0; j < room_count; j++)
				if (rooms[j] == *doors)
					break;

			if (j == room_count)
			{
				rooms[room_count] = *doors;
				room_count++;
			}
		}
	}

	for (int i = 0; i < room_count; i++)
	{
		item_number = room[rooms[i]].item_number;

		while (item_number != -1)
		{
			item2 = &items[item_number];
			next_item = item2->next_item;

			if (item2 == item)
			{
				item_number = next_item;
				continue;
			}

			if (item2 == lara_item)
			{
				item_number = next_item;
				continue;
			}

			if (item2->flags & IFLAG_CLEAR_BODY)
			{
				item_number = next_item;
				continue;
			}

			if (!objects[item2->object_number].collision && item2->object_number != LARA)
			{
				item_number = next_item;
				continue;
			}

			if (!objects[item2->object_number].draw_routine || !item2->mesh_bits)
			{
				item_number = next_item;
				continue;
			}

			if (noInvisible && item2->status == ITEM_INVISIBLE)
			{
				item_number = next_item;
				continue;
			}

			dx = item->pos.x_pos - item2->pos.x_pos;
			dy = item->pos.y_pos - item2->pos.y_pos;
			dz = item->pos.z_pos - item2->pos.z_pos;

			if (dx < -2048 || dx > 2048 || dy < -2048 || dy > 2048 || dz < -2048 || dz > 2048)
			{
				item_number = next_item;
				continue;
			}

			bounds = GetBestFrame(item2);

			if (item->pos.y_pos + rad + 128 < item2->pos.y_pos + bounds[2] || item->pos.y_pos - rad - 128 > item2->pos.y_pos + bounds[3])
			{
				item_number = next_item;
				continue;
			}

			sy = SIN(item2->pos.y_rot);
			cy = COS(item2->pos.y_rot);
			dx = item->pos.x_pos - item2->pos.x_pos;
			dz = item->pos.z_pos - item2->pos.z_pos;
			num = (dx * cy - sy * dz) >> W2V_SHIFT;

			if (item2->object_number == TURN_SWITCH)
			{
				switch_bounds[0] = -256;
				switch_bounds[1] = 256;
				switch_bounds[4] = -256;
				switch_bounds[5] = 256;
				bounds = switch_bounds;
			}

			if (rad + num + 128 >= bounds[0] && num - rad - 128 <= bounds[1])
			{
				num = (dx * sy + cy * dz) >> W2V_SHIFT;

				if (rad + num + 128 >= bounds[4] && num - rad - 128 <= bounds[5])
				{
					StoredItems[items_count] = item2;
					items_count++;

					if (!rad)
						return 1;
				}
			}

			item_number = next_item;
		}
	}

	StoredItems[items_count] = 0;
	return items_count;
}

static int PushPullQuadrant(void)
{
	return (unsigned short)(lara_item->pos.y_rot + 0x2000) / 0x4000;
}

void MovableBlock(short item_number)
{
	struct ITEM_INFO* item = &items[item_number];
	struct FLOOR_INFO* floor;
	struct PHD_VECTOR pos;
	long offset;
	short frame, base, room_number;
	static char sfx = 0;
	int quadrant = PushPullQuadrant();

	pos.x = 0;
	pos.y = 0;
	pos.z = 0;

	switch (lara_item->anim_number)
	{
	case ANIMATION_LARA_OBJECT_PUSH:
		frame = lara_item->frame_number;
		base = anims[ANIMATION_LARA_OBJECT_PUSH].frame_base;

		if ((frame >= base + 30 && frame <= base + 67) || (frame >= base + 78 && frame <= base + 125) || (frame >= base + 140 && frame <= base + 160))
		{
			SoundEffect(SFX_PUSHABLE_SOUND, &item->pos, SFX_ALWAYS);
			sfx = 1;
		}
		else if (sfx)
		{
			SoundEffect(SFX_PUSH_BLOCK_END, &item->pos, SFX_ALWAYS);
			sfx = 0;
		}

		GetLaraJointPos(&pos, LJ_LHAND);

		switch (quadrant)
		{
		case NORTH:
			offset = pos.z + *(long*)&item->item_flags[2] - *(long*)&lara_item->item_flags[2];

			if (abs(item->pos.z_pos - offset) < 512 && item->pos.z_pos < offset)
				item->pos.z_pos = offset;

			break;

		case EAST:
			offset = pos.x + *(long*)&item->item_flags[0] - *(long*)&lara_item->item_flags[0];

			if (abs(item->pos.x_pos - offset) < 512 && item->pos.x_pos < offset)
				item->pos.x_pos = offset;

			break;

		case SOUTH:
			offset = pos.z + *(long*)&item->item_flags[2] - *(long*)&lara_item->item_flags[2];

			if (abs(item->pos.z_pos - offset) < 512 && item->pos.z_pos > offset)
				item->pos.z_pos = offset;

			break;

		case WEST:
			offset = pos.x + *(long*)&item->item_flags[0] - *(long*)&lara_item->item_flags[0];

			if (abs(item->pos.x_pos - offset) < 512 && item->pos.x_pos > offset)
				item->pos.x_pos = offset;

			break;
		}

		if (lara_item->frame_number == anims[lara_item->anim_number].frame_end - 1)
		{
			if (!(input & IN_ACTION))
				lara_item->goal_anim_state = STATE_LARA_STOP;
			else if (!TestBlockPush(item, 1024, quadrant))
				lara_item->goal_anim_state = STATE_LARA_STOP;
		}

		break;

	case ANIMATION_LARA_OBJECT_PULL:
		frame = lara_item->frame_number;
		base = anims[ANIMATION_LARA_OBJECT_PULL].frame_base;

		if ((frame >= base + 40 && frame <= base + 122) || (frame >= base + 130 && frame <= base + 170))
		{
			SoundEffect(SFX_PUSHABLE_SOUND, &item->pos, SFX_ALWAYS);
			sfx = 1;
		}
		else if (sfx)
		{
			SoundEffect(SFX_PUSH_BLOCK_END, &item->pos, SFX_ALWAYS);
			sfx = 0;
		}

		GetLaraJointPos(&pos, LJ_LHAND);

		switch (quadrant)
		{
		case NORTH:
			offset = pos.z + *(long*)&item->item_flags[2] - *(long*)&lara_item->item_flags[2];

			if (abs(item->pos.z_pos - offset) < 512 && item->pos.z_pos > offset)
				item->pos.z_pos = offset;

			break;

		case EAST:
			offset = pos.x + *(long*)&item->item_flags[0] - *(long*)&lara_item->item_flags[0];

			if (abs(item->pos.x_pos - offset) < 512 && item->pos.x_pos > offset)
				item->pos.x_pos = offset;

			break;

		case SOUTH:
			offset = pos.z + *(long*)&item->item_flags[2] - *(long*)&lara_item->item_flags[2];

			if (abs(item->pos.z_pos - offset) < 512 && item->pos.z_pos < offset)
				item->pos.z_pos = offset;

			break;

		case WEST:
			offset = pos.x + *(long*)&item->item_flags[0] - *(long*)&lara_item->item_flags[0];

			if (abs(item->pos.x_pos - offset) < 512 && item->pos.x_pos < offset)
				item->pos.x_pos = offset;

			break;
		}

		if (lara_item->frame_number == anims[lara_item->anim_number].frame_end - 1)
		{
			if (!(input & IN_ACTION))
				lara_item->goal_anim_state = STATE_LARA_STOP;
			else if (!TestBlockPull(item, 1024, quadrant))
				lara_item->goal_anim_state = STATE_LARA_STOP;
		}

		break;

	case ANIMATION_LARA_PUSHABLE_PUSH_TO_STAND:
	case ANIMATION_LARA_PUSHABLE_PULL_TO_STAND:
		frame = lara_item->frame_number;

		if (frame == anims[ANIMATION_LARA_PUSHABLE_PUSH_TO_STAND].frame_base || frame == anims[ANIMATION_LARA_PUSHABLE_PULL_TO_STAND].frame_base)
		{
			item->pos.x_pos = (item->pos.x_pos & -512) | 512;
			item->pos.z_pos = (item->pos.z_pos & -512) | 512;
		}

		if (frame == anims[lara_item->anim_number].frame_end)
		{
			room_number = item->room_number;
			floor = GetFloor(item->pos.x_pos, item->pos.y_pos - 256, item->pos.z_pos, &room_number);
			GetHeight(floor, item->pos.x_pos, item->pos.y_pos - 256, item->pos.z_pos);
			TestTriggers(trigger_index, 1, item->flags & 0x3E00);
			RemoveActiveItem(item_number);
			item->status = ITEM_INACTIVE;
		}

		break;
	}
}

void MovableBlockCollision(short item_number, struct ITEM_INFO* l, struct COLL_INFO* coll)
{
	struct ITEM_INFO* item = &items[item_number];
	struct FLOOR_INFO* floor;
	struct PHD_VECTOR pos;
	short* bounds;
	short room_number, yrot;
	int quadrant;

	room_number = item->room_number;
	floor = GetFloor(item->pos.x_pos, item->pos.y_pos, item->pos.z_pos, &room_number);
	item->pos.y_pos = GetHeight(floor, item->pos.x_pos, item->pos.y_pos, item->pos.z_pos);

	if (item->room_number != room_number)
		ItemNewRoom(item_number, room_number);

	if ((input & IN_ACTION && l->current_anim_state == STATE_LARA_STOP && l->anim_number == ANIMATION_LARA_STAY_IDLE && !l->gravity_status &&
		lara.gun_status == LG_NO_ARMS && item->status == ITEM_INACTIVE && item->trigger_flags >= 0) ||
		(lara.IsMoving && lara.GeneralPtr == (void*)item_number))
	{
		room_number = l->room_number;
		GetFloor(item->pos.x_pos, item->pos.y_pos - 256, item->pos.z_pos, &room_number);

		if (item->room_number == room_number)
		{
			bounds = GetBoundsAccurate(item);
			MovingBlockBounds[0] = (bounds[0] >> 1) - 100;
			MovingBlockBounds[1] = (bounds[1] >> 1) + 100;
			MovingBlockBounds[4] = bounds[4] - 200;
			MovingBlockBounds[5] = 0;
			yrot = item->pos.y_rot;
			item->pos.y_rot = (l->pos.y_rot + 0x2000) & 0xC000;

			if (TestLaraPosition(MovingBlockBounds, item, l))
			{
				if ((((unsigned short)(yrot + 0x2000) / 0x4000) + ((unsigned short)item->pos.y_rot / 0x4000)) & 1)
					MovingBlockPos.z = bounds[0] - 95;
				else
					MovingBlockPos.z = bounds[4] - 95;

				if (MoveLaraPosition(&MovingBlockPos, item, l))
				{
					l->anim_number = ANIMATION_LARA_START_OBJECT_MOVING;
					l->frame_number = anims[ANIMATION_LARA_START_OBJECT_MOVING].frame_base;
					l->current_anim_state = STATE_LARA_PUSHABLE_GRAB;
					l->goal_anim_state = STATE_LARA_PUSHABLE_GRAB;
					lara.IsMoving = 0;
					lara.gun_status = LG_HANDS_BUSY;
					lara.CornerX = (long)item;
				}
				else
					lara.GeneralPtr = (void*)item_number;
			}
			else if (lara.IsMoving && lara.GeneralPtr == (void*)item_number)
			{
				lara.IsMoving = 0;
				lara.gun_status = LG_NO_ARMS;
			}

			item->pos.y_rot = yrot;
		}
	}
	else if (l->current_anim_state == STATE_LARA_PUSHABLE_GRAB && l->frame_number == anims[ANIMATION_LARA_START_OBJECT_MOVING].frame_base + 19 && (struct ITEM_INFO*)lara.CornerX == item)
	{
		pos.x = 0;
		pos.y = 0;
		pos.z = 0;
		quadrant = PushPullQuadrant();

		if (input & IN_FORWARD)
		{
			if (!TestBlockPush(item, 1024, quadrant))
				return;

			l->goal_anim_state = STATE_LARA_PUSHABLE_PUSH;
		}
		else if (input & IN_BACK)
		{
			if (!TestBlockPull(item, 1024, quadrant))
				return;

			l->goal_anim_state = STATE_LARA_PUSHABLE_PULL;
		}
		else
			return;

		AddActiveItem(item_number);
		item->status = ITEM_ACTIVE;
		lara.head_y_rot = 0;
		lara.head_x_rot = 0;
		lara.torso_y_rot = 0;
		lara.torso_x_rot = 0;
		GetLaraJointPos(&pos, LJ_LHAND);
		*(long*)&l->item_flags[0] = pos.x;
		*(long*)&l->item_flags[2] = pos.z;
		*(long*)&item->item_flags[0] = item->pos.x_pos;
		*(long*)&item->item_flags[2] = item->pos.z_pos;
	}
	else
		ObjectCollision(item_number, l, coll);
}

int TestBlockPush(struct ITEM_INFO* item, long height, int quadrant)
{
	struct ITEM_INFO* itemlist[64];
	struct FLOOR_INFO* floor;
	struct room_info* r;
	long x, y, z, rx, rz;
	short room_number;

	x = item->pos.x_pos;
	y = item->pos.y_pos;
	z = item->pos.z_pos;

	switch (quadrant)
	{
	case NORTH:
		z += 1024;
		break;

	case EAST:
		x += 1024;
		break;

	case SOUTH:
		z -= 1024;
		break;

	case WEST:
		x -= 1024;
		break;
	}

	room_number = item->room_number;
	floor = GetFloor(x, y - 256, z, &room_number);
	r = &room[room_number];
	rx = (x - r->x) >> 10;
	rz = (z - r->z) >> 10;

	if (r->floor[rx * r->x_size + rz].stopper)
		return 0;

	if (GetHeight(floor, x, y - 256, z) != y)
		return 0;

	GetHeight(floor, x, y, z);

	if (height_type != WALL)
		return 0;

	y -= height - 100;
	floor = GetFloor(x, y, z, &room_number);

	if (GetCeiling(floor, x, y, z) > y)
		return 0;

	rx = item->pos.x_pos;
	rz = item->pos.z_pos;
	item->pos.x_pos = x;
	item->pos.z_pos = z;
	PortCollidedObjects(item, 256, 1, itemlist);
	item->pos.x_pos = rx;
	item->pos.z_pos = rz;
	return !itemlist[0];
}

int TestBlockPull(struct ITEM_INFO* item, long height, int quadrant)
{
	struct ITEM_INFO* itemlist[64];
	struct FLOOR_INFO* floor;
	struct room_info* r;
	long x, y, z, destx, destz, rx, rz;
	short room_number;

	destx = 0;
	destz = 0;

	switch (quadrant)
	{
	case NORTH:
		destz = -1024;
		break;

	case EAST:
		destx = -1024;
		break;

	case SOUTH:
		destz = 1024;
		break;

	case WEST:
		destx = 1024;
		break;
	}

	x = item->pos.x_pos + destx;
	y = item->pos.y_pos;
	z = item->pos.z_pos + destz;
	room_number = item->room_number;
	floor = GetFloor(x, y - 256, z, &room_number);
	r = &room[room_number];
	rx = (x - r->x) >> 10;
	rz = (z - r->z) >> 10;

	if (r->floor[rx * r->x_size + rz].stopper)
		return 0;

	if (GetHeight(floor, x, y - 256, z) != y)
		return 0;

	floor = GetFloor(x, y - height, z, &room_number);

	if (floor->ceiling << 8 > y - height)
		return 0;

	rx = item->pos.x_pos;
	rz = item->pos.z_pos;
	PortCollidedObjects(item, 256, 1, itemlist);
	item->pos.x_pos = rx;
	item->pos.z_pos = rz;

	if (itemlist[0])
		return 0;

	x += destx;
	z += destz;
	room_number = item->room_number;
	floor = GetFloor(x, y - 256, z, &room_number);

	if (GetHeight(floor, x, y - 256, z) != y)
		return 0;

	floor = GetFloor(x, y - 762, z, &room_number);

	if (floor->ceiling << 8 > y - 762)
		return 0;

	x = lara_item->pos.x_pos + destx;
	y = lara_item->pos.y_pos;
	z = lara_item->pos.z_pos + destz;
	room_number = lara_item->room_number;
	GetFloor(x, y, z, &room_number);
	r = &room[room_number];
	rx = (x - r->x) >> 10;
	rz = (z - r->z) >> 10;

	if (r->floor[rx * r->x_size + rz].stopper)
		return 0;

	rx = lara_item->pos.x_pos;
	rz = lara_item->pos.z_pos;
	lara_item->pos.x_pos = x;
	lara_item->pos.z_pos = z;
	PortCollidedObjects(lara_item, 256, 1, itemlist);
	lara_item->pos.x_pos = rx;
	lara_item->pos.z_pos = rz;
	return !itemlist[0] || itemlist[0] == item;
}
