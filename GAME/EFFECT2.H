#ifndef EFFECT2_H
#define EFFECT2_H

#include "STYPES.H"

extern long wibble;
extern long SplashCount;
extern long KillEverythingFlag;
extern long next_spark;
extern unsigned char TES_extra_tab[6];
extern long DeadlyBounds[6];
extern struct SPLASH_STRUCT splashes[4];
extern struct RIPPLE_STRUCT ripples[32];
extern struct DYNAMIC dynamics[64];
extern struct SPLASH_SETUP splash_setup;
extern struct SP_DYNAMIC spark_dynamics[8];
extern long SmokeWeapon;
extern long SmokeWindX;
extern long SmokeWindZ;
extern long SmokeCountL;
extern long SmokeCountR;
extern struct SPARKS spark[128];
extern short angle;

enum spark_flags
{
	SF_NONE = 0x0,
	SF_FIRE = 0x1,
	SF_SCALE = 0x2,
	SF_UNUSED = 0x4,
	SF_DEF = 0x8,
	SF_ROTATE = 0x10,
	SF_NOKILL = 0x20,
	SF_FX = 0x40,
	SF_ITEM = 0x80,
	SF_OUTSIDE = 0x100,
	SF_UNUSED2 = 0x200,
	SF_DAMAGE = 0x400,
	SF_UNWATER = 0x800,
	SF_ATTACHEDNODE = 0x1000,
	SF_GREEN = 0x2000
};

extern void TriggerRipple(long x, long y, long z, short size, int flags);
extern void ControlEnemyMissile(short fx_number);
extern void ControlSmokeEmitter(short item_number);
extern void KillEverything();
extern void KillAllCurrentItems(short item_number);
extern void TriggerDartSmoke(long x, long y, long z, long xv, long zv, long hit);
extern void TriggerWaterfallMist(long x, long y, long z, long angle);
extern void TriggerSuperJetFlame(struct ITEM_INFO* item, long yvel, long deadly);
extern void DetatchSpark(long num, long type);
extern void TriggerGunSmoke(long x, long y, long z, long xv, long yv, long zv, int arg7, int arg8, int arg9);
extern void TriggerDynamic(long x, long y, long z, int falloff, int r, int g, int b);
extern void TriggerExplosionSmoke(long x, long y, long z, long uw);
extern void TriggerFireFlame(int x, int y, int z, int fxObj, signed int a5);
extern void TriggerFontFire(struct ITEM_INFO* item, int a2, int a3);
extern void TriggerHydraMissileFlame(struct PHD_VECTOR* pos, long x, long y, long z);
extern void TriggerRomanGodMissileFlame(struct PHD_VECTOR* pos, long fx_number);
extern void TriggerTorpedoSteam(struct PHD_VECTOR *pos, struct PHD_VECTOR *a2, int a3);
extern void TriggerSubMist(struct PHD_VECTOR *pos, struct PHD_VECTOR *a4, int a5);
extern void TriggerEngineEffects();
extern void TriggerAirBubbles();
extern void FlamingHell(struct PHD_VECTOR* pos);

#endif