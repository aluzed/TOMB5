#ifndef INPUTUI_H
#define INPUTUI_H

/*
 * In-game input configuration overlay.
 *
 * State and SDL event handling live in EMULATOR (no game rendering
 * dependency); SPEC_PSXPC_N/INPUTUIDRAW.C renders the state with the game's
 * own font/primitive helpers.
 */

#if defined(SDL2)
union SDL_Event;
extern int InputUI_HandleEvent(const union SDL_Event* event);
#endif

extern int InputUI_IsOpen(void);
extern void InputUI_Open(void);
extern void InputUI_Close(void);

/* Called once per drawn frame so F1 is only accepted when the normal draw
 * path is active (not during an FMV, inventory or pause loop). */
extern void InputUI_NotifyDraw(void);
extern int InputUI_CanOpen(void);

/* Read-only state for the renderer. */
extern int InputUI_Screen(void);
extern int InputUI_SelectedAction(void);
extern int InputUI_SelectedColumn(void);
extern int InputUI_DeviceRow(void);
extern int InputUI_IsCapturing(void);
extern const char* InputUI_Status(void);

/* Implemented by SPEC_PSXPC_N/INPUTUIDRAW.C. */
extern void InputUI_Draw(void);

#endif
