# RE-327 collision-switch-door post-switch-door next subcluster selection

## Summary

Selected `weapon-switch-effect-helper` after RE-326 exhausted the switch-door-control helper candidate queue.
The selected candidate is `1ddbda046e37` and must pass a readiness gate before any proof domain can reopen.

## Remaining subclusters

- `weapon-switch-effect-helper`: `1` candidate(s), status `selected-next`.
- `door-save-runtime-helper`: `1` candidate(s), status `deferred-after-selected-subcluster`.
- `camera-collision-helper`: `1` candidate(s), status `deferred-after-selected-subcluster`.

## Readiness decision

- ready-to-reopen rows: `0`
- source-patch authorized rows: `0`
- selected domain: `none`
- selected pivot: `none`
- next ticket: `RE-328` / `weapon-switch-effect-helper-readiness-gate`

Code readiness remains `blocked`.
