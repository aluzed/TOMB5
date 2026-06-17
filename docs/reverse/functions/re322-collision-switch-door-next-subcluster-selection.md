# RE-322 collision-switch-door next subcluster selection

## Summary

Validated RE-321 collision-geometry queue exhaustion and re-entered the RE-311 deferred subcluster queue.
Selected `switch-door-control-helper` with candidate `8d1fc6fc3cfc` for the next readiness gate.

## Deferred subclusters

- `switch-door-control-helper`: `1` candidate(s), status `selected-next`.
- `weapon-switch-effect-helper`: `1` candidate(s), status `deferred-after-selected-subcluster`.
- `door-save-runtime-helper`: `1` candidate(s), status `deferred-after-selected-subcluster`.
- `camera-collision-helper`: `1` candidate(s), status `deferred-after-selected-subcluster`.

## Readiness decision

No proof domain or source patch is reopened by this selection. Domain and pivot remain `none`; code readiness remains `blocked`.

## Next

- `RE-323` / `switch-door-control-helper-readiness-gate`
