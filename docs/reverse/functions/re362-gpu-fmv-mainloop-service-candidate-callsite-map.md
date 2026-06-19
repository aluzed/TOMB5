# RE-362 gpu/fmv mainloop service candidate callsite map

## Summary

Mapped `87` source-backed callsite metadata rows across `14` gpu/fmv mainloop candidate context functions.
Source-backed callsite rows are not source-patch authorization; they are an input to the next readiness gate.

## Counts

- implemented context functions: `12`
- stub context functions: `0`
- no-callsite context functions: `2`
- candidate-level proof rows: `0`

## Readiness decision

Domain and pivot remain `none`; code readiness remains blocked until RE-363 gates the callsite map.
