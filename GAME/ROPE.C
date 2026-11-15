#include "ROPE.H"

#include "CONTROL.H"
#include "LARA.H"
#include "CAMERA.H"
#include INPUT_H
#include "SAVEGAME.H"
#include "MATHS.H"
#include "CALCLARA.H"
#include "DRAW.H"
#include "LOAD_LEV.H"
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
struct PHD_VECTOR* Normalise(struct PHD_VECTOR* v)
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
	Normalise(a3);
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
/* ===== Côté objet de la corde (port de TOMB5pc/game/rope.cpp) ===== */

static struct PENDULUM NullPendulum = { { 0, 0, 0 }, { 0, 0, 0 }, 0, 0 };

void CreateRope(struct ROPE_STRUCT* rope, struct PHD_VECTOR* pos, struct PHD_VECTOR* dir, long slength, struct ITEM_INFO* item)
{
	long lp;

	rope->Position = *pos;
	rope->SegmentLength = slength << 16;
	dir->x <<= 16;
	dir->y <<= 16;
	dir->z <<= 16;
	Normalise(dir);

	if (item->trigger_flags == -1)
		rope->Coiled = 30;
	else
		rope->Coiled = 0;

	for (lp = 0; lp < 24; lp++)
	{
		rope->Segment[lp].x = (long)(((long long)(rope->SegmentLength * lp) * dir->x) >> 16);
		rope->Segment[lp].y = (long)(((long long)(rope->SegmentLength * lp) * dir->y) >> 16);
		rope->Segment[lp].z = (long)(((long long)(rope->SegmentLength * lp) * dir->z) >> 16);
		rope->Velocity[lp].x = 0;
		rope->Velocity[lp].y = 0;
		rope->Velocity[lp].z = 0;

		if (item->trigger_flags == -1)
		{
			rope->Segment[lp].x = 1024 * lp;
			rope->Segment[lp].y >>= 4;
			rope->Velocity[lp].x = 0x4000;
			rope->Velocity[lp].y = 0x300000 - 0x20000 * lp;
			rope->Velocity[lp].z = 0x4000;
		}
	}

	rope->Active = 0;
}

void InitialiseRope(short item_number)
{
	struct ITEM_INFO* item;
	struct FLOOR_INFO* floor;
	struct PHD_VECTOR pos;
	struct PHD_VECTOR dir;
	short room_number;

	item = &items[item_number];
	room_number = item->room_number;
	pos.x = item->pos.x_pos;
	pos.y = item->pos.y_pos;
	pos.z = item->pos.z_pos;
	floor = GetFloor(pos.x, pos.y, pos.z, &room_number);
	pos.y = GetCeiling(floor, pos.x, pos.y, pos.z);

	dir.x = 0;
	dir.y = 0x4000;
	dir.z = 0;
	CreateRope(&Ropes[nRope], &pos, &dir, 128, item);
	item->trigger_flags = (short)nRope++;
}

void GetRopePos(struct ROPE_STRUCT* rope, long pos, long* x, long* y, long* z)
{
	long segment;

	segment = pos >> 7;
	*x = (rope->NormalisedSegment[segment].x * (pos & 0x7F) >> 16) + (rope->MeshSegment[segment].x >> 16) + rope->Position.x;
	*y = (rope->NormalisedSegment[segment].y * (pos & 0x7F) >> 16) + (rope->MeshSegment[segment].y >> 16) + rope->Position.y;
	*z = (rope->NormalisedSegment[segment].z * (pos & 0x7F) >> 16) + (rope->MeshSegment[segment].z >> 16) + rope->Position.z;
}

long mDotProduct(struct PHD_VECTOR* a, struct PHD_VECTOR* b)
{
	return (a->x * b->x + a->y * b->y + a->z * b->z) >> W2V_SHIFT;
}

void vMul(struct PHD_VECTOR* v, long scale, struct PHD_VECTOR* d)
{
	d->x = scale * v->x >> W2V_SHIFT;
	d->y = scale * v->y >> W2V_SHIFT;
	d->z = scale * v->z >> W2V_SHIFT;
}

void mCrossProduct(struct PHD_VECTOR* a, struct PHD_VECTOR* b, struct PHD_VECTOR* n)
{
	struct PHD_VECTOR t;

	t.x = a->y * b->z - a->z * b->y;
	t.y = a->z * b->x - a->x * b->z;
	t.z = a->x * b->y - a->y * b->x;
	n->x = t.x >> W2V_SHIFT;
	n->y = t.y >> W2V_SHIFT;
	n->z = t.z >> W2V_SHIFT;
}

void phd_GetMatrixAngles(long* m, short* dest)
{
	long sy, cy;
	short roll, pitch, yaw;

	pitch = (short)phd_atan_asm(phd_sqrt_asm((m[M22] * m[M22]) + (m[M02] * m[M02])), m[M12]);

	if ((m[M12] >= 0 && pitch > 0) || (m[M12] < 0 && pitch < 0))
		pitch = -pitch;

	yaw = (short)phd_atan_asm(m[M22], m[M02]);
	sy = SIN(yaw);
	cy = COS(yaw);
	roll = (short)phd_atan_asm(m[M00] * cy - m[M20] * sy, m[M21] * sy - m[M01] * cy);
	dest[0] = pitch;
	dest[1] = yaw;
	dest[2] = roll;
}

void ModelRigidRope(struct PHD_VECTOR* pa, struct PHD_VECTOR* pb, struct PHD_VECTOR* va, struct PHD_VECTOR* vb, long rlength)
{
	struct PHD_VECTOR delta, d, a, b;
	long length, scale;

	a.x = pb->x - pa->x;
	a.y = pb->y - pa->y;
	a.z = pb->z - pa->z;
	b.x = vb->x;
	b.y = vb->y;
	b.z = vb->z;
	d.x = a.x + b.x;
	d.y = a.y + b.y;
	d.z = a.z + b.z;
	length = phd_sqrt_asm(abs((d.x >> 16) * (d.x >> 16) + (d.y >> 16) * (d.y >> 16) + (d.z >> 16) * (d.z >> 16)));
	scale = (length << 16) - rlength;
	Normalise(&d);
	delta.x = (long)(((long long)scale * d.x) >> 16);
	delta.y = (long)(((long long)scale * d.y) >> 16);
	delta.z = (long)(((long long)scale * d.z) >> 16);
	vb->x -= delta.x;
	vb->y -= delta.y;
	vb->z -= delta.z;
}

void ModelRigid(struct PHD_VECTOR* pa, struct PHD_VECTOR* pb, struct PHD_VECTOR* va, struct PHD_VECTOR* vb, long rlength)
{
	struct PHD_VECTOR delta, d, a, b;
	long length, scale;

	a.x = pb->x - pa->x;
	a.y = pb->y - pa->y;
	a.z = pb->z - pa->z;
	b.x = vb->x - va->x;
	b.y = vb->y - va->y;
	b.z = vb->z - va->z;
	d.x = a.x + b.x;
	d.y = a.y + b.y;
	d.z = a.z + b.z;
	length = phd_sqrt_asm(abs((d.x >> 16) * (d.x >> 16) + (d.y >> 16) * (d.y >> 16) + (d.z >> 16) * (d.z >> 16)));
	scale = ((length << 16) - rlength) >> 1;
	Normalise(&d);
	delta.x = (long)(((long long)scale * d.x) >> 16);
	delta.y = (long)(((long long)scale * d.y) >> 16);
	delta.z = (long)(((long long)scale * d.z) >> 16);
	va->x += delta.x;
	va->y += delta.y;
	va->z += delta.z;
	vb->x -= delta.x;
	vb->y -= delta.y;
	vb->z -= delta.z;
}

void SetPendulumPoint(struct ROPE_STRUCT* Rope, long node)
{
	CurrentPendulum.Position.x = Rope->Segment[node].x;
	CurrentPendulum.Position.y = Rope->Segment[node].y;
	CurrentPendulum.Position.z = Rope->Segment[node].z;

	if (CurrentPendulum.node == -1)
	{
		CurrentPendulum.Velocity.x += Rope->Velocity[node].x;
		CurrentPendulum.Velocity.y += Rope->Velocity[node].y;
		CurrentPendulum.Velocity.z += Rope->Velocity[node].z;
	}

	CurrentPendulum.node = node;
	CurrentPendulum.Rope = Rope;
}

void CalculateRope(struct ROPE_STRUCT* Rope)
{
	struct PENDULUM* Pendulum;
	struct PHD_VECTOR dir;
	long n, bSetFlag;

	bSetFlag = 0;

	if (Rope->Coiled)
	{
		Rope->Coiled--;

		if (!Rope->Coiled)
		{
			for (n = 0; n < 24; n++)
				Rope->Velocity[n].y = 0;
		}
	}

	if (Rope == &Ropes[lara.RopePtr])
	{
		Pendulum = &CurrentPendulum;

		if (CurrentPendulum.node != lara.RopeSegment + 1)
		{
			SetPendulumPoint(Rope, lara.RopeSegment + 1);
			bSetFlag = 1;
		}
	}
	else
	{
		Pendulum = &NullPendulum;

		if (lara.RopePtr == -1 && CurrentPendulum.Rope)
		{
			for (n = 0; n < CurrentPendulum.node; n++)
			{
				CurrentPendulum.Rope->Velocity[n].x = CurrentPendulum.Rope->Velocity[CurrentPendulum.node].x;
				CurrentPendulum.Rope->Velocity[n].y = CurrentPendulum.Rope->Velocity[CurrentPendulum.node].y;
				CurrentPendulum.Rope->Velocity[n].z = CurrentPendulum.Rope->Velocity[CurrentPendulum.node].z;
			}

			CurrentPendulum.Position.x = 0;
			CurrentPendulum.Position.y = 0;
			CurrentPendulum.Position.z = 0;
			CurrentPendulum.Velocity.x = 0;
			CurrentPendulum.Velocity.y = 0;
			CurrentPendulum.Velocity.z = 0;
			CurrentPendulum.node = -1;
			CurrentPendulum.Rope = 0;
		}
	}

	if (lara.RopePtr != -1)
	{
		dir.x = Pendulum->Position.x - Rope->Segment[0].x;
		dir.y = Pendulum->Position.y - Rope->Segment[0].y;
		dir.z = Pendulum->Position.z - Rope->Segment[0].z;
		Normalise(&dir);

		for (n = Pendulum->node; n >= 0; n--)
		{
			Rope->Segment[n].x = Rope->MeshSegment[n - 1].x + (long)(((long long)Rope->SegmentLength * dir.x) >> 16);
			Rope->Segment[n].y = Rope->MeshSegment[n - 1].y + (long)(((long long)Rope->SegmentLength * dir.y) >> 16);
			Rope->Segment[n].z = Rope->MeshSegment[n - 1].z + (long)(((long long)Rope->SegmentLength * dir.z) >> 16);
			Rope->Velocity[n].x = 0;
			Rope->Velocity[n].y = 0;
			Rope->Velocity[n].z = 0;
		}

		if (bSetFlag)
		{
			dir.x = Pendulum->Position.x - Rope->Segment[Pendulum->node].x;
			dir.y = Pendulum->Position.y - Rope->Segment[Pendulum->node].y;
			dir.z = Pendulum->Position.z - Rope->Segment[Pendulum->node].z;
			Rope->Segment[Pendulum->node].x = Pendulum->Position.x;
			Rope->Segment[Pendulum->node].y = Pendulum->Position.y;
			Rope->Segment[Pendulum->node].z = Pendulum->Position.z;

			for (n = Pendulum->node; n < 24; n++)
			{
				Rope->Segment[n].x -= dir.x;
				Rope->Segment[n].y -= dir.y;
				Rope->Segment[n].z -= dir.z;
				Rope->Velocity[n].x = 0;
				Rope->Velocity[n].y = 0;
				Rope->Velocity[n].z = 0;
			}
		}

		ModelRigidRope(&Rope->Segment[0], &Pendulum->Position, &Rope->Velocity[0], &Pendulum->Velocity, Rope->SegmentLength * Pendulum->node);
		Pendulum->Velocity.y += 393216;
		Pendulum->Position.x += Pendulum->Velocity.x;
		Pendulum->Position.y += Pendulum->Velocity.y;
		Pendulum->Position.z += Pendulum->Velocity.z;
		Pendulum->Velocity.x -= Pendulum->Velocity.x >> 8;
		Pendulum->Velocity.z -= Pendulum->Velocity.z >> 8;
	}

	for (n = Pendulum->node; n < 23; n++)
		ModelRigid(&Rope->Segment[n], &Rope->Segment[n + 1], &Rope->Velocity[n], &Rope->Velocity[n + 1], Rope->SegmentLength);

	for (n = 0; n < 24; n++)
	{
		Rope->Segment[n].x += Rope->Velocity[n].x;
		Rope->Segment[n].y += Rope->Velocity[n].y;
		Rope->Segment[n].z += Rope->Velocity[n].z;
	}

	for (n = Pendulum->node; n < 24; n++)
	{
		Rope->Velocity[n].y += 0x30000;

		if (Pendulum->Rope)
		{
			Rope->Velocity[n].x -= Rope->Velocity[n].x >> 4;
			Rope->Velocity[n].z -= Rope->Velocity[n].z >> 4;
		}
		else
		{
			Rope->Velocity[n].x -= Rope->Velocity[n].x >> 7;
			Rope->Velocity[n].z -= Rope->Velocity[n].z >> 7;
		}
	}

	Rope->Segment[0].x = 0;
	Rope->Segment[0].y = 0;
	Rope->Segment[0].z = 0;
	Rope->Velocity[0].x = 0;
	Rope->Velocity[0].y = 0;
	Rope->Velocity[0].z = 0;

	for (n = 0; n < 23; n++)
	{
		Rope->NormalisedSegment[n].x = Rope->Segment[n + 1].x - Rope->Segment[n].x;
		Rope->NormalisedSegment[n].y = Rope->Segment[n + 1].y - Rope->Segment[n].y;
		Rope->NormalisedSegment[n].z = Rope->Segment[n + 1].z - Rope->Segment[n].z;
		Normalise(&Rope->NormalisedSegment[n]);
	}

	if (Rope != &Ropes[lara.RopePtr])
	{
		Rope->MeshSegment[0].x = Rope->Segment[0].x;
		Rope->MeshSegment[0].y = Rope->Segment[0].y;
		Rope->MeshSegment[0].z = Rope->Segment[0].z;
		Rope->MeshSegment[1].x = Rope->Segment[0].x + (long)(((long long)Rope->SegmentLength * Rope->NormalisedSegment[0].x) >> 16);
		Rope->MeshSegment[1].y = Rope->Segment[0].y + (long)(((long long)Rope->SegmentLength * Rope->NormalisedSegment[0].y) >> 16);
		Rope->MeshSegment[1].z = Rope->Segment[0].z + (long)(((long long)Rope->SegmentLength * Rope->NormalisedSegment[0].z) >> 16);

		for (n = 2; n < 24; n++)
		{
			Rope->MeshSegment[n].x = Rope->MeshSegment[n - 1].x + (long)(((long long)Rope->SegmentLength * Rope->NormalisedSegment[n - 1].x) >> 16);
			Rope->MeshSegment[n].y = Rope->MeshSegment[n - 1].y + (long)(((long long)Rope->SegmentLength * Rope->NormalisedSegment[n - 1].y) >> 16);
			Rope->MeshSegment[n].z = Rope->MeshSegment[n - 1].z + (long)(((long long)Rope->SegmentLength * Rope->NormalisedSegment[n - 1].z) >> 16);
		}
	}
	else
	{
		Rope->MeshSegment[Pendulum->node].x = Rope->Segment[Pendulum->node].x;
		Rope->MeshSegment[Pendulum->node].y = Rope->Segment[Pendulum->node].y;
		Rope->MeshSegment[Pendulum->node].z = Rope->Segment[Pendulum->node].z;
		Rope->MeshSegment[Pendulum->node + 1].x = Rope->Segment[Pendulum->node].x + (long)(((long long)Rope->SegmentLength * Rope->NormalisedSegment[Pendulum->node].x) >> 16);
		Rope->MeshSegment[Pendulum->node + 1].y = Rope->Segment[Pendulum->node].y + (long)(((long long)Rope->SegmentLength * Rope->NormalisedSegment[Pendulum->node].y) >> 16);
		Rope->MeshSegment[Pendulum->node + 1].z = Rope->Segment[Pendulum->node].z + (long)(((long long)Rope->SegmentLength * Rope->NormalisedSegment[Pendulum->node].z) >> 16);

		for (n = Pendulum->node + 1; n < 23; n++)
		{
			Rope->MeshSegment[n + 1].x = Rope->MeshSegment[n].x + (long)(((long long)Rope->SegmentLength * Rope->NormalisedSegment[n].x) >> 16);
			Rope->MeshSegment[n + 1].y = Rope->MeshSegment[n].y + (long)(((long long)Rope->SegmentLength * Rope->NormalisedSegment[n].y) >> 16);
			Rope->MeshSegment[n + 1].z = Rope->MeshSegment[n].z + (long)(((long long)Rope->SegmentLength * Rope->NormalisedSegment[n].z) >> 16);
		}

		for (n = 0; n < Pendulum->node; n++)
		{
			Rope->MeshSegment[n].x = Rope->Segment[n].x;
			Rope->MeshSegment[n].y = Rope->Segment[n].y;
			Rope->MeshSegment[n].z = Rope->Segment[n].z;
		}
	}
}

long RopeNodeCollision(struct ROPE_STRUCT* rope, long x, long y, long z, long rad)
{
	long i, rx, ry, rz;

	for (i = 0; i < 22; i++)
	{
		if (y > rope->Position.y + (rope->MeshSegment[i].y >> 16) && y < rope->Position.y + (rope->MeshSegment[i + 1].y >> 16))
		{
			rx = x - ((rope->MeshSegment[i + 1].x + rope->MeshSegment[i].x) >> 17) - rope->Position.x;
			ry = y - ((rope->MeshSegment[i + 1].y + rope->MeshSegment[i].y) >> 17) - rope->Position.y;
			rz = z - ((rope->MeshSegment[i + 1].z + rope->MeshSegment[i].z) >> 17) - rope->Position.z;

			if ((rx * rx + ry * ry + rz * rz) < ((rad + 64) * (rad + 64)))
				return i;
		}
	}

	return -1;
}

void AlignLaraToRope(struct ITEM_INFO* l)
{
	struct ROPE_STRUCT* rope;
	struct PHD_VECTOR v, u, n, up, v1, v2, n2;
	short* frame;
	long x, y, z, x1, y1, z1, i;
	long temp[12];
	short xyz[3];
	short ropeangle;

	up.x = 4096;
	up.y = 0;
	up.z = 0;
	frame = GetBestFrame(l);
	ropeangle = lara.RopeY - 16380;
	rope = &Ropes[lara.RopePtr];
	i = lara.RopeSegment;
	GetRopePos(rope, (i - 1) * 128 + frame[7], &x, &y, &z);
	GetRopePos(rope, (i - 1) * 128 + frame[7] - 192, &x1, &y1, &z1);
	u.x = (x - x1) << 16;
	u.y = (y - y1) << 16;
	u.z = (z - z1) << 16;
	Normalise(&u);
	u.x >>= 2;
	u.y >>= 2;
	u.z >>= 2;
	vMul(&u, mDotProduct(&up, &u), &v);
	v.x = up.x - v.x;
	v.y = up.y - v.y;
	v.z = up.z - v.z;
	v1 = v;
	v2 = v;
	n2 = u;
	vMul(&v1, COS(ropeangle), &v1);
	vMul(&n2, mDotProduct(&n2, &v), &n2);
	vMul(&n2, 4096 - COS(ropeangle), &n2);
	mCrossProduct(&u, &v, &v2);
	vMul(&v2, SIN(ropeangle), &v2);
	n2.x += v1.x;
	n2.y += v1.y;
	n2.z += v1.z;
	v.x = (n2.x + v2.x) << 16;
	v.y = (n2.y + v2.y) << 16;
	v.z = (n2.z + v2.z) << 16;
	Normalise(&v);
	v.x >>= 2;
	v.y >>= 2;
	v.z >>= 2;
	mCrossProduct(&u, &v, &n);
	n.x <<= 16;
	n.y <<= 16;
	n.z <<= 16;
	Normalise(&n);
	n.x >>= 2;
	n.y >>= 2;
	n.z >>= 2;
	temp[M00] = n.x;
	temp[M01] = u.x;
	temp[M02] = v.x;
	temp[M10] = n.y;
	temp[M11] = u.y;
	temp[M12] = v.y;
	temp[M20] = n.z;
	temp[M21] = u.z;
	temp[M22] = v.z;
	phd_GetMatrixAngles(temp, xyz);
	l->pos.x_pos = rope->Position.x + (rope->MeshSegment[i].x >> 16);
	l->pos.y_pos = rope->Position.y + (rope->MeshSegment[i].y >> 16) + lara.RopeOffset;
	l->pos.z_pos = rope->Position.z + (rope->MeshSegment[i].z >> 16);
	mPushUnitMatrix();
	mRotYXZ(xyz[1], xyz[0], xyz[2]);
	l->pos.x_pos += -112 * Matrix->m02 >> W2V_SHIFT;
	l->pos.y_pos += -112 * Matrix->m12 >> W2V_SHIFT;
	l->pos.z_pos += -112 * Matrix->m22 >> W2V_SHIFT;
	mPopMatrix();
	l->pos.x_rot = xyz[0];
	l->pos.y_rot = xyz[1];
	l->pos.z_rot = xyz[2];
}

void RopeCollision(short item_number, struct ITEM_INFO* l, struct COLL_INFO* coll)
{
	struct ROPE_STRUCT* rope;
	short* bounds;
	long i, x, y, z, rad;

	rope = &Ropes[items[item_number].trigger_flags];

	if ((input & IN_ACTION) && lara.gun_status == LG_NO_ARMS &&
		(l->current_anim_state == STATE_LARA_REACH || l->current_anim_state == STATE_LARA_JUMP_UP) &&
		l->gravity_status && l->fallspeed > 0 && rope->Active)
	{
		bounds = GetBoundsAccurate(l);
		x = l->pos.x_pos;
		y = l->pos.y_pos + bounds[2] + 512;
		z = l->pos.z_pos + (bounds[5] * COS(l->pos.y_rot) >> W2V_SHIFT);
		rad = l->current_anim_state == STATE_LARA_REACH ? 128 : 320;
		i = RopeNodeCollision(rope, x, y, z, rad);

		if (i >= 0)
		{
			if (l->current_anim_state == STATE_LARA_REACH)
			{
				l->anim_number = ANIMATION_LARA_ROPE_JUMP_TO_GRAB;
				l->current_anim_state = STATE_LARA_ROPE_SWING;
				lara.RopeFrame = (anims[ANIMATION_LARA_ROPE_SWING_FORWARD_SEMIHARD].frame_base + 32) * 256;
				lara.RopeDFrame = (anims[ANIMATION_LARA_ROPE_SWING_FORWARD_SEMIHARD].frame_base + 60) * 256;
			}
			else
			{
				l->anim_number = ANIMATION_LARA_MONKEY_TO_ROPE_BEGIN;
				l->current_anim_state = STATE_LARA_ROPE_IDLE;
			}

			l->frame_number = anims[l->anim_number].frame_base;
			l->gravity_status = 0;
			l->fallspeed = 0;
			lara.gun_status = LG_HANDS_BUSY;
			lara.RopePtr = items[item_number].trigger_flags;
			lara.RopeSegment = (char)i;
			lara.RopeY = l->pos.y_rot;
			AlignLaraToRope(l);
			CurrentPendulum.Velocity.x = 0;
			CurrentPendulum.Velocity.y = 0;
			CurrentPendulum.Velocity.z = 0;
			ApplyVelocityToRope(i, l->pos.y_rot, 16 * lara_item->speed);
		}
	}
}

void RopeControl(short item_number)
{
	struct ROPE_STRUCT* currope;

	currope = &Ropes[items[item_number].trigger_flags];

	if (TriggerActive(&items[item_number]))
	{
		currope->Active = 1;
		CalculateRope(currope);
	}
	else
		currope->Active = 0;
}

void init_all_ropes()
{
	int i;

	for (i = 0; i < 8; i++)
		Ropes[i].Active = 0;

	nRope = 0;
}
