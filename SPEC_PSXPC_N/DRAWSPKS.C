#include "DRAWSPKS.H"

#include "SPECIFIC.H"

#include "TYPES.H"
#include "GPU.H"
#include "3D_GEN.H"
#include "CAMERA.H"
#include "DRAW.H"
#include "OBJECTS.H"
#include "SETUP.H"
#include "EFFECT2.H"
#include "TOMB4FX.H"
#include "DRAWPHAS.H"
#include "MATHS.H"

#include <math.h>

long TorchWibble[] =
{
	0x0000FBE7, 0x040000FB, 0xF6040000, 0x00F60400, 
	0x0000F604, 0x5C0000F6, 0xEF5C0000, 0x00EF5C00
};

struct MATRIX3D CamGTE;
struct MATRIX3D LightPos;

/* Projette un point du monde à l'écran à partir de la matrice vue courante
   (w2v_matrix) et de la caméra. */
static int ProjectEffectPoint(long x, long y, long z, long* sx, long* sy, long* zv)
{
	long dx, dy, dz, vx, vy, vz;

	dx = x - camera.pos.x;
	dy = y - camera.pos.y;
	dz = z - camera.pos.z;

	vx = ((short)w2v_matrix[0] * dx + (short)w2v_matrix[1] * dy + (short)w2v_matrix[2] * dz) >> W2V_SHIFT;
	vy = ((short)w2v_matrix[4] * dx + (short)w2v_matrix[5] * dy + (short)w2v_matrix[6] * dz) >> W2V_SHIFT;
	vz = ((short)w2v_matrix[8] * dx + (short)w2v_matrix[9] * dy + (short)w2v_matrix[10] * dz) >> W2V_SHIFT;

	if (vz < 64)
		return 0;

	*sx = SCREEN_WIDTH / 2 + (vx * phd_persp) / vz;
	*sy = SCREEN_HEIGHT / 2 - (vy * phd_persp) / vz;
	*zv = vz;

	return *sx > -1024 && *sx < SCREEN_WIDTH + 1024 && *sy > -1024 && *sy < SCREEN_HEIGHT + 1024;
}

static void EmitSprite(long x, long y, long def, long size, long r, long g, long b)
{
	if ((unsigned long)db.polyptr >= (unsigned long)db.polybuf_limit)
		return;

	MGDrawSprite((int)x, (int)y, (int)def, 0, (int)size, (int)size, genRGB(r, g, b));
}

void S_DrawDarts(struct ITEM_INFO* item)
{
	UNIMPLEMENTED();
}

void S_DrawSparks()
{
	struct SPARKS* sptr;
	long i, sx, sy, zv, size, def, base;

	base = objects[DEFAULT_SPRITES].mesh_index;

	for (i = 0; i < 128; i++)
	{
		sptr = &spark[i];

		if (!sptr->On)
			continue;

		if (!ProjectEffectPoint(sptr->x, sptr->y, sptr->z, &sx, &sy, &zv))
			continue;

		size = sptr->Size;

		if (sptr->Flags & SF_SCALE)
			size <<= sptr->Scalar;

		if (size < 1)
			size = 1;

		size = (size * phd_persp) / zv;

		if (size < 1)
			size = 1;
		else if (size > 128)
			size = 128;

		if (sx + size < 0 || sx - size > SCREEN_WIDTH || sy + size < 0 || sy - size > SCREEN_HEIGHT)
			continue;

		def = sptr->Def - base;

		if (def < 0 || def > 63)
			def = 0;

		EmitSprite(sx, sy, def, size, sptr->R, sptr->G, sptr->B);
	}
}

static void EmitLightningQuad(long x0, long y0, long x1, long y1, long width, long r, long g, long b, struct PSXSPRITESTRUCT* sprite)
{
	POLY_FT4* ptr;
	long dx, dy, nx, ny, len;

	if ((unsigned long)db.polyptr >= (unsigned long)db.polybuf_limit)
		return;

	dx = x1 - x0;
	dy = y1 - y0;
	len = (long)sqrtf((float)(dx * dx + dy * dy));

	if (len < 1)
		return;

	nx = (-dy * width) / (2 * len);
	ny = (dx * width) / (2 * len);

	if (!nx && !ny)
	{
		nx = 1;
		ny = 1;
	}

	ptr = (POLY_FT4*)db.polyptr;

	setPolyFT4(ptr);
	setSemiTrans(ptr, TRUE);
	setRGB0(ptr, r, g, b);

	setXY4(ptr,
		x0 - nx, y0 - ny,
		x1 - nx, y1 - ny,
		x0 + nx, y0 + ny,
		x1 + nx, y1 + ny);

	ptr->tpage = sprite->tpage;
	ptr->clut = sprite->clut;

	setUV4(ptr,
		sprite->u1, sprite->v1,
		sprite->u2, sprite->v1,
		sprite->u1, sprite->v2,
		sprite->u2, sprite->v2);

	addPrim(db.ot, ptr);

	db.polyptr += sizeof(POLY_FT4);
}

void DrawLightning()
{
	/* Version PSXPC de DrawLightning (reference TOMB5pc/specific/specificfx.cpp).
	   Les 32 points de la foudre sont calcules comme sur PC, puis projetes
	   a l'ecran et rendus sous forme de rubans de sprites. */
	struct LIGHTNING_STRUCT* l;
	struct PSXSPRITESTRUCT* sprite;
	float px, py, pz, px1, py1, pz1, px2, py2, pz2, px3, py3, pz3, n, nx, ny, nz;
	float pos[32][3];
	long r1, r2, r3, r, g, b, lp, width, flags[32];
	long sx[32], sy[32], sz[32];
	static long rnd = 0xD371F947;

	sprite = &psxspriteinfo[objects[DEFAULT_SPRITES].mesh_index + 28];
	r1 = rnd;

	for (int i = 0; i < 16; i++)
	{
		l = &Lightning[i];

		if (!l->Life)
			continue;

		px = (float)l->Point[0].x;
		py = (float)l->Point[0].y;
		pz = (float)l->Point[0].z;

		px1 = (float)l->Point[1].x - px;
		py1 = (float)l->Point[1].y - py;
		pz1 = (float)l->Point[1].z - pz;

		px2 = (float)l->Point[2].x - px;
		py2 = (float)l->Point[2].y - py;
		pz2 = (float)l->Point[2].z - pz;

		px3 = (float)l->Point[3].x - px;
		py3 = (float)l->Point[3].y - py;
		pz3 = (float)l->Point[3].z - pz;

		n = 0;

		for (lp = 0; lp < 32; lp++)
		{
			float xAdd, yAdd, zAdd;

			if (!lp || lp == 31)
			{
				xAdd = 0;
				yAdd = 0;
				zAdd = 0;
			}
			else
			{
				r2 = 0x41C64E6D * r1 + 0x3039;
				r3 = 0x41C64E6D * r2 + 0x3039;
				r1 = 0x41C64E6D * r3 + 0x3039;
				xAdd = (float)(((r2 >> 10) & 0xF) - 8);
				yAdd = (float)(((r3 >> 10) & 0xF) - 8);
				zAdd = (float)(((r1 >> 10) & 0xF) - 8);
			}

			nx = (1.0F - n) * (1.0F - n) * n * 4.0F;
			ny = (1.0F - n) * (n * n) * 4.0F;
			nz = ((n + n) - 1.0F) * (n * n);
			pos[lp][0] = nx * px1 + ny * px2 + nz * px3 + px + xAdd;
			pos[lp][1] = nx * py1 + ny * py2 + nz * py3 + py + yAdd;
			pos[lp][2] = nx * pz1 + ny * pz2 + nz * pz3 + pz + zAdd;

			n += (1.0F / 32.0F);
			flags[lp] = 0;
		}

		for (lp = 0; lp < 32; lp++)
			flags[lp] = ProjectEffectPoint((long)pos[lp][0], (long)pos[lp][1], (long)pos[lp][2], &sx[lp], &sy[lp], &sz[lp]);

		if (l->Life < 16)
		{
			r = (l->Life * l->r) >> 4;
			g = (l->Life * l->g) >> 4;
			b = (l->Life * l->b) >> 4;
		}
		else
		{
			r = l->r;
			g = l->g;
			b = l->b;
		}

		for (lp = 0; lp < 31; lp++)
		{
			if (!flags[lp] || !flags[lp + 1])
				continue;

			width = (l->Size * phd_persp) / sz[lp];

			if (width < 1)
				width = 1;
			else if (width > 96)
				width = 96;

			EmitLightningQuad(sx[lp], sy[lp], sx[lp + 1], sy[lp + 1], width, r, g, b, sprite);
		}
	}

	rnd = r1;
}
