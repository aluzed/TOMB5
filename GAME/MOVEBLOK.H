#ifndef MOVEBLOK_H
#define MOVEBLOK_H

#include "STYPES.H"

extern void PortInitialiseFallingBlock2(short item_number);
extern void InitialiseMovingBlock(short item_number);
extern void MovableBlock(short item_number);
extern void MovableBlockCollision(short item_number, struct ITEM_INFO* l, struct COLL_INFO* coll);
extern int TestBlockPush(struct ITEM_INFO* item, long height, int quadrant);
extern int TestBlockPull(struct ITEM_INFO* item, long height, int quadrant);

#endif
