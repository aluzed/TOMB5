#ifndef ROMANGOD_H
#define ROMANGOD_H

#include "TYPES.H"

extern void TriggerRomanGodSparks(long x, long y, long z, long xv, long yv, long zv, long god);
extern void TriggerRomanGodMissileFlame(struct PHD_VECTOR* pos, long fxnum);
extern void TriggerRomanGodMissile(struct PHD_3DPOS* pos, short room_number, short num);
extern void TriggerRomanGodLightningGlow(long x, long y, long z, long rgb);
extern void TriggerRomanGodPowerupFlames(short item_number, long shade);
extern void TriggerRomangodGravel(struct ITEM_INFO* item, struct PHD_VECTOR* pos, long node);
extern void InitialiseRomangod(short item_number);
extern void RomangodControl(short item_number);

#endif
