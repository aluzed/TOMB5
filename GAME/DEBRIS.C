#include "DEBRIS.H"

#include "SPECIFIC.H"

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

void TriggerDebris(struct GAME_VECTOR* pos, void* TextInfo, short* Offsets, long* Vels, int rgb)//3675C, 36C5C
{
	struct DEBRIS_STRUCT* d;
	short angle;
	int i;

	if ((GetRandomControl() & 3) != 0)
		return;

	if (Vels[0] < 0)
	{
		d = (struct DEBRIS_STRUCT*)&pos->y;
		ShatterObject((struct SHATTER_ITEM*)pos, NULL, Vels[0], 0, 0);
		return;
	}

	d = &debris[GetFreeDebris()];

	d->On = 1;
	d->x = pos->x;
	d->y = pos->y;
	d->z = pos->z;
	d->RoomNumber = pos->room_number;

	d->Yvel = (GetRandomControl() & 0x1F) + 16;
	if (d->Yvel < 32)
		d->Yvel = 32;

	d->Gravity = 4;
	d->Speed = (GetRandomControl() & 0x3F) + 32;

	if (pos->y != 0) // dummy
	{
	}

	d->TextInfo = TextInfo;

	for (i = 0; i < 3; i++)
	{
		d->XYZOffsets1[i] = Offsets[i];
		d->XYZOffsets2[i] = Offsets[i + 3];
		d->XYZOffsets3[i] = Offsets[i + 6];
	}

	if (Vels[5])
	{
		d->Yvel = Vels[5];
		d->Speed = (GetRandomControl() & 0xFF) << 1;
		d->Yvel = Vels[5];
		d->Dir = (GetRandomControl() << 3) | 0x7000;
	}
	else
	{
		d->Dir = (GetRandomControl() << 4);
		d->XRot = 0;
		d->YRot = 0;
	}

	if (rgb & 0x800000)
	{
		d->r = (rgb >> 16) & 0xFF;
		d->g = (rgb >> 8) & 0xFF;
		d->b = rgb & 0xFF;
	}
	else
	{
		d->r = 0xFF;
		d->g = 0xFF;
		d->b = 0xFF;
	}
}


void ShatterObject(struct SHATTER_ITEM* ShatterItem, struct MESH_INFO* StaticMesh, short Num, short RoomNumber, int NoXZVel)//36A3C, 36F3C
{
	int i;
	short* sptr;
	short* dptr;
	long* vptr;
	long* nptr;
	struct DEBRIS_STRUCT* d;
	struct GAME_VECTOR pos;
	long x, y, z;
	short room_num;
	int lp;

	if (ShatterItem == NULL)
		return;

	if (Num < 0)
		Num = -Num;

	// Get debris mesh info
	sptr = (short*)ShatterItem->meshp;
	if (sptr == NULL)
		return;

	for (i = 0; i < Num; i++)
	{
		d = &debris[GetFreeDebris()];
		d->On = 1;
		d->TextInfo = NULL;

		// Copy position
		d->x = ShatterItem->Sphere.x;
		d->y = ShatterItem->Sphere.y;
		d->z = ShatterItem->Sphere.z;
		d->RoomNumber = RoomNumber;

		d->Speed = (GetRandomControl() & 0x1F) + 16;
		d->Yvel = (GetRandomControl() & 0xF) - 16;
		d->Gravity = 4;

		d->Dir = GetRandomControl() << 1;
		d->XRot = GetRandomControl();
		d->YRot = GetRandomControl();

		d->r = 0xFF;
		d->g = 0xFF;
		d->b = 0xFF;
	}
}
