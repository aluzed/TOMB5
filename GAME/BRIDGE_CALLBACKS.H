#pragma once
// BLOCKED-001: exactly-typed bridge callback adapters (int/int* slot <-> long/long* body).
// Guard: PSX_VERSION && PSXPC_TEST only. Precondition: height output valid AND initialized.
#if PSX_VERSION && PSXPC_TEST
struct ITEM_INFO;
void BridgeCallbackFlatFloor(struct ITEM_INFO*, int, int, int, int*);
void BridgeCallbackFlatCeiling(struct ITEM_INFO*, int, int, int, int*);
void BridgeCallbackTilt1Floor(struct ITEM_INFO*, int, int, int, int*);
void BridgeCallbackTilt1Ceiling(struct ITEM_INFO*, int, int, int, int*);
void BridgeCallbackTilt2Floor(struct ITEM_INFO*, int, int, int, int*);
void BridgeCallbackTilt2Ceiling(struct ITEM_INFO*, int, int, int, int*);
#endif
