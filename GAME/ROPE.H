#ifndef ROPE_H
#define ROPE_H

#include "TYPES.H"

extern void SaveRope();
extern void LoadRope();
extern void Straighten(struct ROPE_STRUCT* a1, struct PHD_VECTOR* a2, struct PHD_VECTOR* a3, long a4);
extern void StraightenRope(struct ITEM_INFO* item);
extern void InitialiseRope(short item_number);
extern void RopeControl(short item_number);
extern void RopeCollision(short item_number, struct ITEM_INFO* l, struct COLL_INFO* coll);
extern void AlignLaraToRope(struct ITEM_INFO* item);
extern void init_all_ropes();
extern struct PHD_VECTOR* Normalise(struct PHD_VECTOR* v);

#endif