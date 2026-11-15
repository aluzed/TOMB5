#include "ROPE.H"

#include "CONTROL.H"
#include "LARA.H"
#include "SAVEGAME.H"
#include "MATHS.H"
#include "SPECIFIC.H"

#if PSXPC_TEST
#include <stdint.h>
#elif PSX_VERSION || SAT_VERSION
typedef unsigned int uintptr_t;
#endif

#if PSXPC_TEST
#include <stdint.h>
#endif

#if PSX_VERSION || PSXPC_VERSION || SAT_VERSION || PS2_VERSION
#include "GETSTUFF.H"
#endif

void SaveRope()// (F)
{
	WriteSG((char*)&Ropes[lara.RopePtr], sizeof(struct ROPE_STRUCT));
	CurrentPendulum.Rope = (struct ROPE_STRUCT*)((char*)CurrentPendulum.Rope - (uintptr_t)Ropes);
	WriteSG((char*)&CurrentPendulum, sizeof(struct PENDULUM));
	CurrentPendulum.Rope = (struct ROPE_STRUCT*)((char*)CurrentPendulum.Rope + (uintptr_t)Ropes);
}

void LoadRope()// (F)
{
	ReadSG((char*)&Ropes[lara.RopePtr], sizeof(struct ROPE_STRUCT));
	ReadSG((char*)&CurrentPendulum, sizeof(struct PENDULUM));

	CurrentPendulum.Rope = (struct ROPE_STRUCT*)((char*)CurrentPendulum.Rope + (uintptr_t)Ropes);
}

/* Portés depuis TOMB5pc/game/rope.cpp (_Straighten / Normalise). */
static struct PHD_VECTOR* PortNormalise(struct PHD_VECTOR* v)
{
	long mod, x, y, z, dist;

	x = v->x >> 16;
	y = v->y >> 16;
	z = v->z >> 16;

	if (!x && !y && !z)
		return v;

	dist = phd_sqrt_asm(abs(x * x + y * y + z * z));
	mod = 0x10000 / dist;

	v->x = (long)(((long long)mod * v->x) >> 16);
	v->y = (long)(((long long)mod * v->y) >> 16);
	v->z = (long)(((long long)mod * v->z) >> 16);
	return v;
}

void Straighten(struct ROPE_STRUCT* a1, struct PHD_VECTOR* a2, struct PHD_VECTOR* a3, long a4)
{
	long n;

	a1->Position = *a2;
	a1->SegmentLength = a4 << 16;
	a3->x <<= 16;
	a3->y <<= 16;
	a3->z <<= 16;
	PortNormalise(a3);
	a1->Coiled = 0;

	for (n = 0; n < 24; n++)
	{
		a1->Segment[n].x = (long)(((long long)(a1->SegmentLength * n) * a3->x) >> 16);
		a1->Segment[n].y = (long)(((long long)(a1->SegmentLength * n) * a3->y) >> 16);
		a1->Segment[n].z = (long)(((long long)(a1->SegmentLength * n) * a3->z) >> 16);
		a1->Velocity[n].x = 0;
		a1->Velocity[n].y = 0;
		a1->Velocity[n].z = 0;
	}
}

void StraightenRope(struct ITEM_INFO* item)// (F)
{
	short room_num = item->room_number;
	struct PHD_VECTOR v1, v2;

	v1.x = item->pos.x_pos;
	v1.y = item->pos.y_pos;
	v1.z = item->pos.z_pos;

	v1.y = GetCeiling(GetFloor(v1.x, v1.y, v1.z, &room_num), v1.x, v1.y, v1.z);

	v2.x = 0;
	v2.y = 16384;
	v2.z = 0;

	Straighten(&Ropes[nRope], &v1, &v2, 128);
}