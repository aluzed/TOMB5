# RE-151 — Item lighting interaction argument and state taxonomy

Cluster: `item-lighting-interaction`
Decision: `argument-state-taxonomy-blocked`
Next: `RE-152`

## Progress tracker

- [x] RE-150 callsite map consumed.
- [x] Argument and state taxonomy emitted.
- [x] Alert-light source call arguments canonicalized to position/color/room taxonomy.
- [x] Patch and marker readiness kept blocked.

## Findings

- `shape-item-lighting-alert-light-parameters` — callees `TriggerAlertLight`; arguments `position-color-room-arguments`; state `alert-light-state;dynamic-light-state;room-light-state`; patch `no`
- `shape-item-lighting-void-torch-update` — callees `DoFlameTorch`; arguments `void`; state `item-flame-state;lara-torch-state;left-arm-state;torch-item-state;torch-particle-state`; patch `no`

No production source or marker change is authorized by this taxonomy.
