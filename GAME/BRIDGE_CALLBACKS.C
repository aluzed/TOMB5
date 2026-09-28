// BLOCKED-001: exactly-typed wrappers. No incompatible pointer cast (scalar conversions only).
#if PSX_VERSION && PSXPC_TEST
#include "OBJECTS.H"
#include "CONTROL.H"
#include "BRIDGE_CALLBACKS.H"
/* precondition: h points to a valid initialized int (never NULL). */
void BridgeCallbackFlatFloor(struct ITEM_INFO* i,int x,int y,int z,int* h){ long t=*h; BridgeFlatFloor(i,x,y,z,&t); *h=(int)t; }
void BridgeCallbackFlatCeiling(struct ITEM_INFO* i,int x,int y,int z,int* h){ long t=*h; BridgeFlatCeiling(i,x,y,z,&t); *h=(int)t; }
void BridgeCallbackTilt1Floor(struct ITEM_INFO* i,int x,int y,int z,int* h){ long t=*h; BridgeTilt1Floor(i,x,y,z,&t); *h=(int)t; }
void BridgeCallbackTilt1Ceiling(struct ITEM_INFO* i,int x,int y,int z,int* h){ long t=*h; BridgeTilt1Ceiling(i,x,y,z,&t); *h=(int)t; }
void BridgeCallbackTilt2Floor(struct ITEM_INFO* i,int x,int y,int z,int* h){ long t=*h; BridgeTilt2Floor(i,x,y,z,&t); *h=(int)t; }
void BridgeCallbackTilt2Ceiling(struct ITEM_INFO* i,int x,int y,int z,int* h){ long t=*h; BridgeTilt2Ceiling(i,x,y,z,&t); *h=(int)t; }
#endif
