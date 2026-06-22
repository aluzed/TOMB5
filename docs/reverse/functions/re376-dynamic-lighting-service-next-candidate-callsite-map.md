# RE-376 dynamic-lighting service next-candidate callsite map

## Summary

Mapped `40` source-backed callsite metadata rows across `21` dynamic-lighting next-candidate context functions.
Source-backed callsite rows are not source-patch authorization; they are an input to the next readiness gate.

## Counts

- implemented context functions: `9`
- stub context functions: `12`
- no-callsite context functions: `0`
- candidate-level proof rows: `0`

## Readiness decision

Domain and pivot remain `none`; code readiness remains blocked until RE-377 gates the next-candidate callsite map.
