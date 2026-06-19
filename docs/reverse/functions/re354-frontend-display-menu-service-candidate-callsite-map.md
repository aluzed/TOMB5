# RE-354 frontend display/menu service candidate callsite map

## Summary

Mapped `326` source-backed callsite metadata rows across `25` frontend display/menu candidate context functions.
Source-backed callsite rows are not source-patch authorization; they are an input to the next readiness gate.

## Counts

- implemented context functions: `23`
- stub context functions: `0`
- no-callsite context functions: `2`
- candidate-level proof rows: `0`

## Readiness decision

Domain and pivot remain `none`; code readiness remains blocked until RE-355 gates the callsite map.
