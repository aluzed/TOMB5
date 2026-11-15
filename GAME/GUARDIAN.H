#ifndef GUARDIAN_H
#define GUARDIAN_H

#include "TYPES.H"

extern void InitialiseGuardian(short item_number);
extern void TriggerGuardianSparks(struct GAME_VECTOR* pos, long size, long rgb, long power);
extern void TriggerBaseLightning(struct ITEM_INFO* item);
extern void GuardianControl(short item_number);

#endif
