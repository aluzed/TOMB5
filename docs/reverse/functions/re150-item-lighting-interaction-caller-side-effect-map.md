# RE-150 — Item lighting interaction caller and side-effect map

Cluster: `item-lighting-interaction`
Decision: `caller-side-effect-map-blocked`
Next: `RE-151`

## Progress tracker

- [x] RE-149 ticket plan consumed.
- [x] Item-lighting callsites mapped.
- [x] Torch and alert-light side-effect surfaces classified.
- [x] Patch and marker readiness kept blocked.

## Findings

- `LaraGun` -> `DoFlameTorch` in `GAME/LARAFIRE.C`; shape `shape-item-lighting-void-torch-update`; patch `no`
- `ControlStrobeLight` -> `TriggerAlertLight` in `GAME/OBJLIGHT.C`; shape `shape-item-lighting-alert-light-parameters`; patch `no`

No production source or marker change is authorized by this map.
