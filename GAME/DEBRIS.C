#include "DEBRIS.H"

#include "SPECIFIC.H"
#include "CAMERA.H"
#include "CONTROL.H"
#include "DRAW.H"
#include "MISC.H"
#include "SETUP.H"
#include "GPU.H"
#include "TOMB4FX.H"
#include "MATHS.H"

#include "TYPES.H"

struct DEBRIS_STRUCT debris[128];
short DebrisFlags;
long next_debris;

long GetFreeDebris()//366B0(<), 36BB0(<) (F)
{
	struct DEBRIS_STRUCT* dptr;
	long lp = 0;
	long eldestage = -16383;
	long eldestfree = 0;
	long free = next_debris;

	dptr = &debris[free];

	for (lp = 0; lp < 128; lp++)
	{
		if (!dptr->On)
		{
			next_debris = (free + 1) & 0x7F;
			return free;
		}

		if (eldestage < dptr->Yvel)
		{
			eldestfree = free;
			eldestage = dptr->Yvel;
		}

		if (free == 0x7F)
		{
			free = 0;
			dptr = &debris[free];
		}
		else
		{
			dptr++;
		}
	}

	next_debris = (eldestfree + 1) & 0x7F;

	return eldestfree;
}

void TriggerDebris(struct GAME_VECTOR* pos, void* TextInfo, short* Offsets, long* Vels, int rgb)//3675C, 36C5C (F)
{
	struct DEBRIS_STRUCT* d;
	short colour;
	int i;

	colour = (short)rgb;

	if ((GetRandomControl() & 3) == 0 && colour >= 0)
		TriggerShatterSmoke(pos->x, pos->y, pos->z);

	if (colour < 0)
		colour = -colour;

	d = &debris[GetFreeDebris()];
	d->On = 2;

	d->x = pos->x;
	d->y = pos->y;
	d->z = pos->z;

	if (DebrisFlags & 1)
	{
		/* Random shatter: no meaningful source velocity is available. */
		d->Dir = GetRandomControl() << 1;
		d->Speed = (GetRandomControl() & 0xF) + 16;
		d->Yvel = -(GetRandomControl() & 0x7F) - 64;
		d->Gravity = (GetRandomControl() & 0x1F) + 16;
	}
	else
	{
		/* Velocity is the vector from the model centre to the face centre. */
		d->Dir = phd_atan_asm(Vels[2], Vels[0]);
		d->Speed = phd_sqrt_asm(Vels[0] * Vels[0] + Vels[2] * Vels[2]) >> 3;

		if (Vels[1] == 0)
		{
			d->Yvel = 0;
			d->Gravity = (GetRandomControl() & 0x1F) + 32;
		}
		else
		{
			d->Yvel = -(GetRandomControl() & 0x1FF) - 512;
			d->Gravity = (GetRandomControl() & 0x3F) + 64;

			if (Vels[1] == -1)
				d->Yvel = (short)((unsigned short)d->Yvel << 1);
		}
	}

	d->RoomNumber = pos->room_number;

	for (i = 0; i < 3; i++)
	{
		d->XYZOffsets1[i] = Offsets[i];
		d->XYZOffsets2[i] = Offsets[i + 3];
		d->XYZOffsets3[i] = Offsets[i + 6];
	}

	if (DebrisFlags & 1)
	{
		d->XRot = d->YRot = (unsigned char)(GetRandomControl() << 1);
	}
	else
	{
		d->XRot = 0;
		d->YRot = 0;
	}

	d->TextInfo = TextInfo;

	/* Expand the packed 5:5:5 face colour to 8:8:8. */
	d->r = (unsigned char)(colour << 3);
	d->g = (unsigned char)((colour >> 2) & 0xF8);
	d->b = (unsigned char)((colour >> 7) & 0xF8);
}

void ShatterObject(struct SHATTER_ITEM* shatter_item, struct MESH_INFO* StaticMesh, short Num, short RoomNumber, int NoXZVel)//36A3C, 36F3C (F)
{
	struct GAME_VECTOR pos;
	short* meshp;
	short* vptr;
	short* facep;
	short* fp;
	short trans[160 * 3];
	short offsets[9];
	long vels[3];
	short yrot;
	short siny;
	short cosy;
	short centre_shift;
	short face_offset;
	short num_tris;
	short num_quads;
	short shade;
	short light;
	short colour;
	long x;
	long y;
	long z;
	long sumx;
	long sumy;
	long sumz;
	long avgx;
	long avgy;
	long avgz;
	long cx;
	long cy;
	long cz;
	long v0x;
	long v0y;
	long v0z;
	long v1x;
	long v1y;
	long v1z;
	long v2x;
	long v2y;
	long v2z;
	long texword;
	long idxword;
	int num_verts;
	int count;
	int neg;
	int i;
	int j;
	int idx0;
	int idx1;
	int idx2;
	int page;
	int tex;

	if (shatter_item == NULL && StaticMesh == NULL)
		return;

	centre_shift = 0;
	light = 0;

	if (shatter_item == NULL)
	{
		/* Static-mesh path: the mesh comes from the room's static object. */
		x = StaticMesh->x;
		y = StaticMesh->y;
		z = StaticMesh->z;
		yrot = StaticMesh->y_rot;
		light = StaticMesh->shade;

		if (StaticMesh->static_number >= 0)
			meshp = meshes[static_objects[StaticMesh->static_number].mesh_number];
		else
			meshp = NULL;
	}
	else
	{
		x = shatter_item->Sphere.x;
		y = shatter_item->Sphere.y;
		z = shatter_item->Sphere.z;
		yrot = shatter_item->YRot;
		meshp = shatter_item->meshp;

		if (shatter_item->Flags & 0x1000)
			centre_shift = 2;

		/* Light[3] holds the three 12-bit channel values written by
		 * S_CalculateLight; pack them into 5:5:5. */
		if (shatter_item->il != NULL)
		{
			int* il = (int*)shatter_item->il;
			light = (short)(((unsigned)il[9] >> 7) |
				(((unsigned)il[10] >> 7) << 5) |
				(((unsigned)il[11] >> 7) << 10));
		}
	}

	if (meshp == NULL)
		return;

	if (Num < 0)
	{
		neg = 1;
		count = -Num;
	}
	else
	{
		neg = 0;
		count = Num;
	}

	if (count == 0)
		return;

	/* PSX mesh header: vertex count in the low byte at offset 8 and the
	 * face-data offset (in bytes, bit 0 unused) in the word at offset 10. */
	num_verts = *((unsigned char*)meshp + 8);
	if (num_verts > 160)
		num_verts = 160;

	face_offset = (short)(meshp[5] & ~1);
	vptr = (short*)((char*)meshp + 12);
	facep = (short*)((char*)vptr + face_offset);
	num_tris = *facep++;
	num_quads = *facep++;
	fp = facep;

	siny = SIN(yrot);
	cosy = COS(yrot);

	/* Rotate every vertex into object space around the Y axis and keep the
	 * running average used as the model centre. */
	sumx = 0;
	sumy = 0;
	sumz = 0;

	for (i = 0; i < num_verts; i++)
	{
		short* sv = vptr + i * 4;
		long tx = ((long)sv[0] * cosy + (long)sv[2] * siny) >> W2V_SHIFT;
		long ty = sv[1];
		long tz = ((long)sv[2] * cosy - (long)sv[0] * siny) >> W2V_SHIFT;

		trans[i * 3 + 0] = (short)tx;
		trans[i * 3 + 1] = (short)ty;
		trans[i * 3 + 2] = (short)tz;

		sumx += tx;
		sumy += ty;
		sumz += tz;
	}

	if (num_verts != 0)
	{
		avgx = sumx / num_verts;
		avgy = sumy / num_verts;
		avgz = sumz / num_verts;
	}
	else
	{
		avgx = 0;
		avgy = 0;
		avgz = 0;
	}

	pos.room_number = RoomNumber;

	/* Triangle batches: one long of four texture indices, then up to four
	 * index words (three vertex bytes plus a texture-page nibble). */
	for (i = 0; i < num_tris && count > 0; )
	{
		texword = *(long*)fp;
		fp += 2;

		for (j = 0; j < 4 && i < num_tris && count > 0; j++, i++)
		{
			idxword = *(long*)fp;
			fp += 2;

			idx0 = (int)(idxword & 0xFF);
			idx1 = (int)((idxword >> 8) & 0xFF);
			idx2 = (int)((idxword >> 16) & 0xFF);
			page = (int)(((unsigned long)idxword >> 24) & 0xF);

			if (idx0 >= num_verts || idx1 >= num_verts || idx2 >= num_verts)
				continue;

			if (neg && (GetRandomControl() & 1) == 0)
				continue;

			shade = vptr[idx0 * 4 + 3];

			v0x = trans[idx0 * 3 + 0];
			v0y = trans[idx0 * 3 + 1];
			v0z = trans[idx0 * 3 + 2];
			v1x = trans[idx1 * 3 + 0];
			v1y = trans[idx1 * 3 + 1];
			v1z = trans[idx1 * 3 + 2];
			v2x = trans[idx2 * 3 + 0];
			v2y = trans[idx2 * 3 + 1];
			v2z = trans[idx2 * 3 + 2];

			cx = (v0x + v1x + v2x) / 3;
			cy = (v0y + v1y + v2y) / 3;
			cz = (v0z + v1z + v2z) / 3;

			offsets[0] = (short)(v0x - (cx >> centre_shift));
			offsets[1] = (short)(v0y - (cy >> centre_shift));
			offsets[2] = (short)(v0z - (cz >> centre_shift));
			offsets[3] = (short)(v1x - (cx >> centre_shift));
			offsets[4] = (short)(v1y - (cy >> centre_shift));
			offsets[5] = (short)(v1z - (cz >> centre_shift));
			offsets[6] = (short)(v2x - (cx >> centre_shift));
			offsets[7] = (short)(v2y - (cy >> centre_shift));
			offsets[8] = (short)(v2z - (cz >> centre_shift));

			vels[0] = cx - avgx;
			vels[1] = cy - avgy;
			vels[2] = cz - avgz;

			if (NoXZVel > 0)
			{
				light = 3171;
				vels[0] = 0;
				vels[1] = 0;
				vels[2] = 0;
			}
			else if (NoXZVel < 0)
			{
				vels[1] = NoXZVel;
			}

			pos.x = cx + x;
			pos.y = cy + y;
			pos.z = cz + z;

			tex = (page << 8) | (int)(((unsigned long)texword >> (j * 8)) & 0xFF);

			if (shatter_item == NULL)
				colour = (short)(((shade >> 1) & 0x3DEF) + ((StaticMesh->shade >> 1) & 0x3DEF));
			else
			{
				colour = light;

				if (shatter_item->Flags & 0x400)
					colour = (short)-colour;
			}

			TriggerDebris(&pos, &psxtextinfo[tex], offsets, vels, colour);
			count--;
		}
	}

	/* Quad batches: one long with a 12-bit texture id, then two index words. */
	for (i = 0; i < num_quads && count > 0; )
	{
		texword = *(long*)fp;
		fp += 2;

		for (j = 0; j < 2 && i < num_quads && count > 0; j++, i++)
		{
			idxword = *(long*)fp;
			fp += 2;

			idx0 = (int)(idxword & 0xFF);
			idx1 = (int)((idxword >> 8) & 0xFF);
			idx2 = (int)((idxword >> 16) & 0xFF);

			if (idx0 >= num_verts || idx1 >= num_verts || idx2 >= num_verts)
				continue;

			if (neg && (GetRandomControl() & 1) == 0)
				continue;

			shade = vptr[idx0 * 4 + 3];

			v0x = trans[idx0 * 3 + 0];
			v0y = trans[idx0 * 3 + 1];
			v0z = trans[idx0 * 3 + 2];
			v1x = trans[idx1 * 3 + 0];
			v1y = trans[idx1 * 3 + 1];
			v1z = trans[idx1 * 3 + 2];
			v2x = trans[idx2 * 3 + 0];
			v2y = trans[idx2 * 3 + 1];
			v2z = trans[idx2 * 3 + 2];

			cx = (v0x + v1x + v2x) / 3;
			cy = (v0y + v1y + v2y) / 3;
			cz = (v0z + v1z + v2z) / 3;

			offsets[0] = (short)(v0x - (cx >> centre_shift));
			offsets[1] = (short)(v0y - (cy >> centre_shift));
			offsets[2] = (short)(v0z - (cz >> centre_shift));
			offsets[3] = (short)(v1x - (cx >> centre_shift));
			offsets[4] = (short)(v1y - (cy >> centre_shift));
			offsets[5] = (short)(v1z - (cz >> centre_shift));
			offsets[6] = (short)(v2x - (cx >> centre_shift));
			offsets[7] = (short)(v2y - (cy >> centre_shift));
			offsets[8] = (short)(v2z - (cz >> centre_shift));

			vels[0] = cx - avgx;
			vels[1] = cy - avgy;
			vels[2] = cz - avgz;

			if (NoXZVel > 0)
			{
				light = 3171;
				vels[0] = 0;
				vels[1] = 0;
				vels[2] = 0;
			}
			else if (NoXZVel < 0)
			{
				vels[1] = NoXZVel;
			}

			pos.x = cx + x;
			pos.y = cy + y;
			pos.z = cz + z;

			tex = (int)(((unsigned long)texword >> (j * 16)) & 0xFFF);

			if (shatter_item == NULL)
				colour = (short)(((shade >> 1) & 0x3DEF) + ((StaticMesh->shade >> 1) & 0x3DEF));
			else
			{
				colour = light;

				if (shatter_item->Flags & 0x400)
					colour = (short)-colour;
			}

			TriggerDebris(&pos, &psxtextinfo[tex], offsets, vels, colour);
			count--;
		}
	}
}
