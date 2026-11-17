#ifndef SPECIFIC_H
#define SPECIFIC_H

#include <stdio.h>
#include "STYPES.H"
#include <stdint.h>

/* Diagnostics des fonctions encore non portees qui sont appelees a chaque
 * frame (UpdateFireSparks, ProcessClosedDoors, ...). Sans garde, le log
 * devient illisible et le printf coute cher : on n'annonce la fonction
 * qu'une seule fois. Le comportement (no-op) est inchange. */
#define UNIMPLEMENTED_ONCE() \
	do { static int _unimplemented_once_ = 0; \
	     if (!_unimplemented_once_) { _unimplemented_once_ = 1; \
	         printf("[%s] - Unimplemented (once)!\n", __func__); } } while (0)

/* RE-739: backend-local replacement for the target's inherited colour word.
 * The last S_UpdateInput / AnimateWaterfalls invocation publishes it;
 * UpdatePulseColour consumes it without changing either public call signature.
 * This capability belongs to this backend, not the PSXPC_TEST build option. */
#define PSXPC_N_INHERITED_PULSE_COLOUR 1
extern uint32_t SecondaryPulseColour;

#define WARN_HACK(x) printf("%s\n", x);


#if PSXPC_VERSION
#define UNIMPLEMENTED() __asm("nop");
#else
#ifdef _MSC_VER
#define FUNCNAME __FUNCTION__
#else
#define FUNCNAME __func__
#endif

#if defined(__EMSCRIPTEN__)
#define UNIMPLEMENTED()
#else
#define UNIMPLEMENTED() S_Warn("[%s] - Unimplemented!\n", FUNCNAME);
#endif

#endif

extern unsigned short AnimComp;
extern short AnimatingTexturesVOffset;
extern struct REQUESTER SettingsReq;
extern struct REQUESTER ConfigReq;
extern unsigned char SoundFXVolume;
extern unsigned short nAnimTextureRanges;
extern unsigned short* AnimTextureRanges;
extern unsigned short nAnimUVRanges;
extern int GtSFXEnabled;
extern short AnimatingTexturesV[16][8][3];

extern void S_control_screen_position();
extern long S_DumpScreen();
extern void S_ExitSystem(char* exit_message);
extern void DisplayConfig(int x, int y);
extern int DoPauseMenu();
extern void gInit();
extern short S_Death();
extern void DisplayStatsUCunt();
//extern void S_Warn(const char* warning_message);
extern int sub_62190();

#define S_Warn printf

#endif