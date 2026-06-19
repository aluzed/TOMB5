# RE-346 cd-load-audio service candidate callsite map

## Summary

Mapped `266` source-backed callsite metadata rows across `34` candidate context functions.
Source-backed callsite rows are not source-patch authorization; they are an input to the next readiness gate.

## Counts

- implemented context functions: `32`
- stub context functions: `0`
- no-callsite context functions: `2`
- candidate-level proof rows: `0`

## Readiness decision

Domain and pivot remain `none`; code readiness remains blocked until RE-347 gates the callsite map.
