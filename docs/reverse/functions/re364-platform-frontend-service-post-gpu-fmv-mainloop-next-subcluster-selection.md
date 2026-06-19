# RE-364 platform/frontend service post gpu/fmv mainloop next subcluster selection

## Summary

Selected `runtime-callee-bridge` after RE-363 exhausted the gpu/fmv mainloop service candidate queue.
The selected candidates are `a01f47cb95a4` and must pass a readiness gate before any proof domain can reopen.

## Selected subcluster

- `runtime-callee-bridge`: `1` candidate(s), status `selected-next`.

## Readiness decision

- ready-to-reopen rows: `0`
- source-patch authorized rows: `0`
- selected domain: `none`
- selected pivot: `none`
- next ticket: `RE-365` / `runtime-callee-bridge-readiness-gate`

Code readiness remains `blocked`.
