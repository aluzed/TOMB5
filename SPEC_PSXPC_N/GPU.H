#ifndef GPU_H
#define GPU_H

#include "STYPES.H"

//#include <sys/types.h>
#include <LIBGPU.H>

#if defined(USE_32_BIT_ADDR)
#define POLYGON_BUFFER_MULT (2)
#else
#define POLYGON_BUFFER_MULT (1)
#endif

extern unsigned long GnFrameCounter;
extern unsigned long GnLastFrameCount;
extern struct PSXTEXTSTRUCT* psxtextinfo;
extern struct PSXSPRITESTRUCT* psxspriteinfo;
extern int rgbscaleme;
extern int gfx_debugging_mode;
extern struct DB_STRUCT db;
extern struct MMTEXTURE* RoomTextInfo;
#define GADW_OT_V2_WORDS (512 * POLYGON_BUFFER_MULT)
#define GADW_OT_WORDS (5128 * POLYGON_BUFFER_MULT)
#define GADW_PB_WORDS (52260 * POLYGON_BUFFER_MULT)
#define GADW_OT_V2_BYTES (GADW_OT_V2_WORDS * (int)sizeof(PSX_ULONG))
#define GADW_OT_BYTES (GADW_OT_WORDS * (int)sizeof(PSX_ULONG))
#define GADW_PB_BYTES (GADW_PB_WORDS * (int)sizeof(PSX_ULONG))
#if defined(__LP64__)
extern unsigned long* GadwOrderingTables_V2;
extern unsigned long* GadwOrderingTables;
extern unsigned long* GadwPolygonBuffers;
#else
extern unsigned long GadwOrderingTables_V2[];
extern unsigned long GadwOrderingTables[GADW_OT_WORDS];
extern unsigned long GadwPolygonBuffers[GADW_PB_WORDS];
#endif

extern void GPU_UseOrderingTables(unsigned long* pBuffers, int nOTSize);
extern void GPU_UsePolygonBuffers(unsigned long* pBuffers, int nPBSize);
extern void GPU_EndScene();
extern int GPU_FlipNoIdle();
extern void do_gfx_debug_mode(unsigned long* otstart);
extern void GPU_FlipStory(unsigned long* gfx);

#define SCREEN_WIDTH 512

#if NTSC_VERSION
#define SCREEN_HEIGHT 240
#else
#define SCREEN_HEIGHT 256
#endif

#endif