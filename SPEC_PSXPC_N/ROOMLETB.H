#ifndef ROOMLETB_H
#define ROOMLETB_H

#include "STYPES.H"

extern void DrawRoomsAsm();
extern void DrawRoomletListAsmBinocular(long underwater, struct room_info* r);
extern void DrawRoomletListAsm(long unk, struct room_info* r);
extern short LOffset[];
extern char LTab[];
#if defined(__LP64__)
extern short* YOffset;
#else
extern short YOffset[];
#endif
extern unsigned short QuadVertTable[];
extern unsigned short TriVertTable[];
extern unsigned short* TriVertTables[];
extern unsigned short* QuadVertTables[];

#endif