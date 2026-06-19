# RE-359 platform/frontend service post frontend display/menu next subcluster selection

## Summary

Selected `gpu-fmv-mainloop-service` after RE-358 exhausted the frontend display/menu service candidate queue.
The selected candidates are `1b3534d34062` and must pass a readiness gate before any proof domain can reopen.

## Selected subcluster

- `gpu-fmv-mainloop-service`: `1` candidate(s), status `selected-next`.

## Readiness decision

- ready-to-reopen rows: `0`
- source-patch authorized rows: `0`
- selected domain: `none`
- selected pivot: `none`
- next ticket: `RE-360` / `gpu-fmv-mainloop-service-readiness-gate`

Code readiness remains `blocked`.
