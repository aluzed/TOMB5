#ifndef PORTSAVE_H
#define PORTSAVE_H

#ifdef __cplusplus
extern "C" {
#endif

/* Port-level quick save/load.
 *
 * The original memory-card save path is not implemented for PSXPC_N.  This
 * module serialises the same 8192-byte buffer used by sgSaveGame() to a host
 * file instead.  F5 requests a save during gameplay; F6 requests a load at the
 * title screen (a normal level load path follows).  The keys are reserved port
 * keys and are intentionally not part of INPUT.CFG. */

#define PORTSAVE_DEFAULT_FILE "TOMB5.SAV"

extern void PortSave_RequestSave(void);
extern void PortSave_RequestLoad(void);

/* Returns 1 once per request and clears the flag. */
extern int PortSave_TakeSaveRequest(void);
extern int PortSave_TakeLoadRequest(void);

extern int PortSave_Write(void);
extern int PortSave_Read(void);

/* Called once after a level has been loaded in response to PortSave_Read(). */
extern void PortSave_ApplyPending(void);

extern const char* PortSave_Path(void);

#ifdef __cplusplus
}
#endif

#endif
