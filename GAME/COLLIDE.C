#include "COLLIDE.H"

#include "CAMERA.H"
#include "CONTROL.H"
#include "ITEMS.H"
#include "LARA.H"
#include "OBJECTS.H"
#include "SETUP.H"
#include "SOUND.H"
#include "SPECIFIC.H"
#include "STYPES.H"
#include <stddef.h>
#include "TOMB4FX.H"
#include "SPHERE.H"
#include "TYPES.H"
#include "EFFECTS.H"

#if PSX_VERSION || PSXPC_VERSION || SAT_VERSION
#include "MISC.H"
#include "FXTRIG.H"
#include "GETSTUFF.H"
#include "CALCLARA.H"
#endif

#include <stdio.h>

long zfront;
long xfront;
short GlobalCollisionBounds[6];

char LM[] =
{
	LJ_HIPS,
	LJ_LTHIGH,
	LJ_LSHIN,
	LJ_LFOOT,
	LJ_RTHIGH,
	LJ_RSHIN,
	LJ_RFOOT,
	LJ_TORSO,
	LJ_RINARM,
	LJ_ROUTARM,
	LJ_RHAND,
	LJ_LINARM,
	LJ_LOUTARM,
	LJ_LHAND,
	LJ_HEAD,
};

void TestForObjectOnLedge(struct ITEM_INFO* item, struct COLL_INFO* coll)//2A940(<), 2AB68(<) (F)
{
	struct GAME_VECTOR s;
	struct GAME_VECTOR d;
	struct MESH_INFO* StaticMesh;
	struct PHD_VECTOR v;
	long lp;

	//loc_2A97C
	for(lp = 0; lp < 2; lp++)
	{
		s.x = (lp << 8) - 0x80;
		s.y = -256;
		s.z = 0;

		GetLaraJointPos((struct PHD_VECTOR*)&s, LJ_HEAD);
		s.room_number = lara_item->room_number;

		d.x = 0;
		d.x = (s.x + ((SIN(lara_item->pos.y_rot) << 1) + SIN(lara_item->pos.y_rot))) >> 4;
		d.y = s.y;
		d.z = (s.z + ((COS(lara_item->pos.y_rot) << 1) + COS(lara_item->pos.y_rot))) >> 4;
		LOS(&s, &d);
		if (ObjectOnLOS2(&s, &d, &v, &StaticMesh) != 0x3E7)
		{
			coll->hit_static = 1;
		}
	}
}

void TriggerLaraBlood()//2A838, 2AA60 (F)
{
	struct PHD_VECTOR vec;
	int node = 1;
	int i;
	for(i = 0; i < 15; i++)
	{
		if (node & lara_item->touch_bits)
		{
			vec.x = (GetRandomControl() & 0x1F) - 16;
			vec.y = (GetRandomControl() & 0x1F) - 16;
			vec.z = (GetRandomControl() & 0x1F) - 16;

			GetLaraJointPos(&vec, LM[i]);
			DoBloodSplat(vec.x, vec.y, vec.z, (GetRandomControl() & 7) + 8, 2 * GetRandomControl(), lara_item->room_number);
		}

		node <<= 1;
	}
}

void GenericSphereBoxCollision(short item_num, struct ITEM_INFO* laraitem, struct COLL_INFO* coll)//2A5EC, 2A814
{
	UNIMPLEMENTED();
}
//int ItemPushLaraStatic(struct ITEM_INFO *laraitem /*$s2*/, short *bounds /*$a1*/, struct PHD_3DPOS *pos /*$s0*/, struct COLL_INFO *coll /*$s1*/)
int ItemPushLaraStatic(struct ITEM_INFO* laraitem, short* bounds, struct PHD_3DPOS* pos, struct COLL_INFO* coll)//2A2D8, 2A500
{
	int x; // $a2
	int z; // $t2
	int rx; // $t0
	int rz; // $a0
	int c; // $t7
	int s; // $t6
	int minx; // $t4
	int maxx; // $t3
	int minz; // $t5
	int maxz; // $a3
	int l; // $v1
	int r; // $a1
	int t; // $a2
	int b; // $a3
	int ax; // $v1
	int az; // $a0

	c = COS(pos->y_rot);
	x = lara_item->pos.x_pos - pos->x_pos;

#if 0
	//t0 = rcossin_tbl
	//v1 = pos->y_rot;
	//a2 = lara_item->pos.x_pos;
	//a0 = pos->x_pos;


		subu    $a2, $a0
		mult    $t7, $a2
		sll     $v1, 1
		addu    $v1, $t0
		lw      $a0, 0x48($s2)
		lw      $v0, 8($s0)
		mflo    $t1
		lh      $t6, 0($v1)
		subu    $t2, $a0, $v0
		mult    $t6, $t2
		mflo    $t0
		nop
		nop
		mult    $t7, $t2
		move    $s1, $a3
		mflo    $v1
		lh      $t4, 0($a1)
		lh      $t3, 2($a1)
		mult    $t6, $a2
		lh      $t5, 8($a1)
		lw      $v0, 0x48($s1)
		lh      $a3, 0xA($a1)
		subu    $t4, $v0
		addu    $t3, $v0
		subu    $t5, $v0
		addu    $a3, $v0
		subu    $t1, $t0
		sra     $t0, $t1, 12
		bgez    $a2, loc_2A39C
		nop
		negu    $a2, $a2
			
		loc_2A39C :
		slti    $a2, 0x1201
		mflo    $a0
		addu    $v1, $a0
		beqz    $a2, loc_2A5D0
		sra     $a0, $v1, 12
		bgez    $t2, loc_2A3BC
		move    $v0, $t2
		negu    $v0, $v0
		
		loc_2A3BC :
		slti    $v0, 0x1201
		beqz    $v0, loc_2A5D0
		slt     $v0, $t4, $t0
		beqz    $v0, loc_2A5D0
		slt     $v0, $t0, $t3
		beqz    $v0, loc_2A5D0
		slt     $v0, $t5, $a0
		beqz    $v0, loc_2A5D0
		slt     $v0, $a0, $a3
		beqz    $v0, loc_2A5D0
		subu    $v1, $t0, $t4
		subu    $a1, $t3, $t0
		subu    $a2, $a3, $a0
		slt     $v0, $a1, $v1
		bnez    $v0, loc_2A41C
		subu    $a3, $a0, $t5
		slt     $v0, $a2, $v1
		bnez    $v0, loc_2A420
		slt     $v0, $v1, $a1
		slt     $v0, $a3, $v1
		bnez    $v0, loc_2A420
		slt     $v0, $v1, $a1
		j       loc_2A46C
		subu    $t0, $v1
			
		loc_2A41C :
		slt     $v0, $v1, $a1

		loc_2A420 :
		bnez    $v0, loc_2A448
		slt     $v0, $v1, $a2
		slt     $v0, $a2, $a1
		bnez    $v0, loc_2A448
		slt     $v0, $v1, $a2
		slt     $v0, $a3, $a1
		bnez    $v0, loc_2A448
		slt     $v0, $v1, $a2
		j       loc_2A46C
		addu    $t0, $a1

		loc_2A448 :
		bnez    $v0, loc_2A468
		slt     $v0, $a1, $a2
		bnez    $v0, loc_2A468
		slt     $v0, $a3, $a2
		bnez    $v0, loc_2A468
		nop
		j       loc_2A46C
		addu    $a0, $a2
			
		loc_2A468 :
		subu    $a0, $a3

		loc_2A46C :
		mult    $t7, $t0
		mflo    $v1
		nop
		nop
		mult    $t6, $a0
		mflo    $a1
		nop
		nop
		mult    $t7, $a0
		mflo    $a0
		nop
		nop
		mult    $t6, $t0
		lw      $v0, 0($s0)
		addu    $v1, $a1
		sra     $v1, 12
		addu    $v0, $v1
		li      $v1, 0x7F00
		sw      $v0, 0x40($s2)
		lw      $v0, 8($s0)
		mflo    $a2
		subu    $a0, $a2
		sra     $a0, 12
		addu    $v0, $a0
		sw      $v0, 0x48($s2)
		li      $v0, 0xFFFFFE80
		sw      $v1, 0x4C($s1)
		sw      $v0, 0x50($s1)
		sw      $zero, 0x54($s1)
		lw      $v1, 0x48($s2)
		lw      $a0, 0x6C($s1)
		lw      $v0, 0x40($s2)
		lw      $a1, 0x64($s1)
		lh      $s0, 0x76($s1)
		subu    $a0, $v1, $a0
		jal     sub_77A40
		subu    $a1, $v0, $a1
		move    $a0, $s1
		sh      $v0, 0x76($s1)
		lw      $a1, 0x40($s2)
		lh      $v1, 0x18($s2)
		lw      $a2, 0x44($s2)
		lw      $a3, 0x48($s2)
		li      $v0, 0x2FA
		sw      $v0, 0x28 + var_14($sp)
		jal     sub_7B210
		sw      $v1, 0x28 + var_18($sp)
		lh      $v0, 0x7A($s1)
		nop
		beqz    $v0, loc_2A550
		sh      $s0, 0x76($s1)
		lw      $v0, 0x64($s1)
		nop
		sw      $v0, 0x40($s2)
		lw      $v1, 0x6C($s1)
		j       loc_2A578
		sw      $v1, 0x48($s2)

		loc_2A550:
		lw      $v0, 0x40($s2)
		nop
		sw      $v0, 0x64($s1)
		lw      $v1, 0x44($s2)
		move    $a0, $s2
		sw      $v1, 0x68($s1)
				 lw      $v0, 0x48($s2)
				 li      $a1, 0xFFFFFFF6
				 jal     sub_7C58C
				 sw      $v0, 0x6C($s1)

				 loc_2A578:
			 lw      $v0, dword_800A2048
				 nop
				 bne     $s2, $v0, loc_2A5D4
				 li      $v0, 1
				 lui     $v0, 0xA
				 addiu   $v1, $v0, 0x57DC
				 lw      $a0, 0x44($v1)
				 nop
				 andi    $v0, $a0, 0x20
				 beqz    $v0, loc_2A5D4
				 li      $v0, 1
				 lbu     $v0, 0x115($v1)
				 nop
				 sltiu   $v0, 0x10
				 bnez    $v0, loc_2A5C8
				 li      $v0, 0xFFFFFFDF
				 and $v0, $a0, $v0
				 sw      $v0, 0x44($v1)
				 sh      $zero, 2($v1)

				 loc_2A5C8:
			 j       loc_2A5D4
				 li      $v0, 1

				 loc_2A5D0 :
				 move    $v0, $zero

				 loc_2A5D4 :
			 lw      $ra, 0x28 + var_4($sp)
				 lw      $s2, 0x28 + var_8($sp)
				 lw      $s1, 0x28 + var_C($sp)
				 lw      $s0, 0x28 + var_10($sp)
				 jr      $ra
				 addiu   $sp, 0x28
#endif

	UNIMPLEMENTED();
	return 0;
}

void AIPickupCollision(short item_num, struct ITEM_INFO* laraitem, struct COLL_INFO* coll)//2A03C(<), 2A264 (F)
{
	struct ITEM_INFO* item = &items[item_num];

	if (item->object_number == SWITCH_TYPE7 && !(item->mesh_bits & 1))
	{
		item->active = TRUE;
		item->status = ITEM_ACTIVE;
	}
}

void TrapCollision(short item_num, struct ITEM_INFO* laraitem, struct COLL_INFO* coll)//2A098(<), 2A2C0 (F)
{
	struct ITEM_INFO* item = &items[item_num];

	if (item->status == ITEM_ACTIVE)
	{
		if (TestBoundsCollide(item, laraitem, coll->radius) == 0)
		{
			return;
		}

		ObjectCollision(item_num, lara_item, coll);
	}
	else if(item->status == ITEM_INVISIBLE)
	{
		//0x2A110
		ObjectCollision(item_num, lara_item, coll);
	}

	//0x2A128
}

void CreatureCollision(short item_num, struct ITEM_INFO* laraitem, struct COLL_INFO* coll)//29E10, 2A024
{
	struct ITEM_INFO* item = &items[item_num];

	if (item->status == ITEM_INVISIBLE || item->hit_points <= 0)
	{
		return;
	}

	if (TestBoundsCollide(item, laraitem, coll->radius) && TestCollision(item, laraitem))
	{
		if (coll->enable_baddie_push)
		{
			ItemPushLara(item, laraitem, coll, 0, 1);
		}
	}
}

void LaraBaddieCollision(struct ITEM_INFO* laraitem, struct COLL_INFO* coll)//29A44, 29C58
{
	static int cooldown = 0;
	int i;

	if (cooldown > 0)
	{
		cooldown--;
	}

	for (i = 0; i < level_items; i++)
	{
		struct ITEM_INFO* item = &items[i];
		long dx;
		long dz;

		if (item == laraitem || item->hit_points <= 0 ||
			item->status == ITEM_INVISIBLE ||
			!objects[item->object_number].intelligent)
		{
			continue;
		}

		dx = item->pos.x_pos - laraitem->pos.x_pos;
		dz = item->pos.z_pos - laraitem->pos.z_pos;

		if (ABS(dx) > 512 || ABS(dz) > 512 || ABS(item->pos.y_pos - laraitem->pos.y_pos) > 512)
		{
			continue;
		}

		if (cooldown == 0)
		{
			laraitem->hit_points -= 5;
			laraitem->hit_status = 1;
			SoundEffect(SFX_LARA_INJURY_RND, &laraitem->pos, SFX_DEFAULT);
			cooldown = 45;
		}

		break;
	}
}

void ShiftItem(struct ITEM_INFO* item, struct COLL_INFO* coll)//7BEEC(<), 7DF30(<) (F)
{
	item->pos.x_pos += coll->shift.x;
	item->pos.y_pos += coll->shift.y;
	item->pos.z_pos += coll->shift.z;
	coll->shift.x = coll->shift.y = coll->shift.z = 0;
}

static void PortRotateXZ(long x, long z, short y_rot, long* rx, long* rz)
{
	*rx = (x * COS(y_rot) - z * SIN(y_rot)) >> W2V_SHIFT;
	*rz = (x * SIN(y_rot) + z * COS(y_rot)) >> W2V_SHIFT;
}

static int PortInside(long value, long low, long high)
{
	return value >= low && value <= high;
}

int TestBoundsCollideStatic(short* bounds, struct PHD_3DPOS* pos, long radius)
{
	long x = lara_item->pos.x_pos - pos->x_pos;
	long z = lara_item->pos.z_pos - pos->z_pos;
	long rx;
	long rz;

	PortRotateXZ(x, z, pos->y_rot, &rx, &rz);

	return PortInside(rx, bounds[0] - radius, bounds[1] + radius) &&
	       PortInside(rz, bounds[4] - radius, bounds[5] + radius);
}

int TestBoundsCollide(struct ITEM_INFO* item, struct ITEM_INFO* laraitem, long radius)
{
	short* bounds = GetBoundsAccurate(item);
	long x = laraitem->pos.x_pos - item->pos.x_pos;
	long z = laraitem->pos.z_pos - item->pos.z_pos;
	long rx;
	long rz;

	if (bounds == NULL)
	{
		return 0;
	}

	PortRotateXZ(x, z, item->pos.y_rot, &rx, &rz);

	return PortInside(rx, bounds[0] - radius, bounds[1] + radius) &&
	       PortInside(rz, bounds[4] - radius, bounds[5] + radius);
}

int TestLaraPosition(short* bounds, struct ITEM_INFO* item, struct ITEM_INFO* lara_item)
{
	short* lara_bounds = GetBoundsAccurate(lara_item);
	long x = lara_item->pos.x_pos - item->pos.x_pos;
	long y = lara_item->pos.y_pos - item->pos.y_pos;
	long z = lara_item->pos.z_pos - item->pos.z_pos;
	long rx;
	long rz;

	if (lara_bounds == NULL)
	{
		return 0;
	}

	PortRotateXZ(x, z, item->pos.y_rot, &rx, &rz);

	return rx + lara_bounds[1] >= bounds[0] &&
	       rx + lara_bounds[0] <= bounds[1] &&
	       y + lara_bounds[3] >= bounds[2] &&
	       y + lara_bounds[2] <= bounds[3] &&
	       rz + lara_bounds[5] >= bounds[4] &&
	       rz + lara_bounds[4] <= bounds[5];
}

int MoveLaraPosition(struct PHD_VECTOR* vector, struct ITEM_INFO* item, struct ITEM_INFO* lara_item)
{
	long x = item->pos.x_pos + ((vector->x * COS(item->pos.y_rot) - vector->z * SIN(item->pos.y_rot)) >> W2V_SHIFT);
	long y = item->pos.y_pos + vector->y;
	long z = item->pos.z_pos + ((vector->x * SIN(item->pos.y_rot) + vector->z * COS(item->pos.y_rot)) >> W2V_SHIFT);

	if (ABS(lara_item->pos.x_pos - x) <= 256 &&
		ABS(lara_item->pos.y_pos - y) <= 256 &&
		ABS(lara_item->pos.z_pos - z) <= 256)
	{
		lara_item->pos.x_pos = x;
		lara_item->pos.y_pos = y;
		lara_item->pos.z_pos = z;
		return 1;
	}

	return 0;
}

int ItemPushLara(struct ITEM_INFO* item, struct ITEM_INFO* laraitem, struct COLL_INFO* coll, int spaz, int big_push)
{
	short* bounds = GetBoundsAccurate(item);
	long x = laraitem->pos.x_pos - item->pos.x_pos;
	long z = laraitem->pos.z_pos - item->pos.z_pos;
	long rx;
	long rz;
	long minx;
	long maxx;
	long minz;
	long maxz;
	long push_x = 0;
	long push_z = 0;

	if (bounds == NULL)
	{
		return 0;
	}

	PortRotateXZ(x, z, item->pos.y_rot, &rx, &rz);

	minx = bounds[0] - coll->radius;
	maxx = bounds[1] + coll->radius;
	minz = bounds[4] - coll->radius;
	maxz = bounds[5] + coll->radius;

	if (!PortInside(rx, minx, maxx) || !PortInside(rz, minz, maxz))
	{
		return 0;
	}

	if (rx - minx < maxx - rx)
	{
		push_x = minx - rx;
	}
	else
	{
		push_x = maxx - rx;
	}

	if (rz - minz < maxz - rz)
	{
		push_z = minz - rz;
	}
	else
	{
		push_z = maxz - rz;
	}

	if (ABS(push_x) < ABS(push_z))
	{
		push_z = 0;
	}
	else
	{
		push_x = 0;
	}

	coll->shift.x = (push_x * COS(item->pos.y_rot) + push_z * SIN(item->pos.y_rot)) >> W2V_SHIFT;
	coll->shift.z = (push_z * COS(item->pos.y_rot) - push_x * SIN(item->pos.y_rot)) >> W2V_SHIFT;

	laraitem->pos.x_pos += coll->shift.x;
	laraitem->pos.z_pos += coll->shift.z;

	return 1;
}

#if PC_VERSION
void UpdateLaraRoom(struct ITEM_INFO* item, int height)//7C58C(<), 7E5D0(<) (F)
{
	short room_number = item->room_number;
	struct FLOOR_INFO* floor = GetFloor(item->pos.x_pos, item->pos.y_pos + height, item->pos.z_pos, &room_number);

	item->floor = GetHeight(floor, item->pos.x_pos, item->pos.y_pos + height, item->pos.z_pos);
	if (item->room_number != room_number)
	{
		printf("New Room switch! %d to %d\n", item->room_number, room_number);
		ItemNewRoom(lara.item_number, room_number);
	}
}
#endif

void ObjectCollision(short item_num, struct ITEM_INFO* lara_item, struct COLL_INFO* coll)// (F)
{
	struct ITEM_INFO* item = &items[item_num];

	if (TestBoundsCollide(&items[item_num], lara_item, coll->radius) && TestCollision(item, lara_item))
	{
		if (coll->enable_baddie_push)
			ItemPushLara(item, lara_item, coll, 0, 1);
	}
}

int GetCollidedObjects(struct ITEM_INFO* a1, long a2, int a3, struct ITEM_INFO** a4, struct MESH_INFO** a5, int a6)
{
	UNIMPLEMENTED();
	return 0;
}
