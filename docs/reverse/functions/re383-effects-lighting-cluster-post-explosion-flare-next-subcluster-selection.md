# RE-383 effects/lighting cluster post explosion/flare next subcluster selection

## Summary

Selected `spotcam-projectile-effect-service` after RE-382 exhausted the explosion/flare service candidate queue.
The selected candidates are `b6d128932004` and must pass a readiness gate before any proof domain can reopen.

## Selected subcluster

- `spotcam-projectile-effect-service`: `1` candidate(s), status `selected-next`.

## Readiness decision

- ready-to-reopen rows: `0`
- source-patch authorized rows: `0`
- selected domain: `none`
- selected pivot: `none`
- next ticket: `RE-384` / `spotcam-projectile-effect-service-readiness-gate`

Code readiness remains `blocked`.
