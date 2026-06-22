# RE-381 explosion/flare effect service candidate callsite map

## Summary

Mapped `121` source-backed callsite metadata rows across `18` explosion/flare candidate context functions.
Source-backed callsite rows are not source-patch authorization; they are an input to the next readiness gate.

## Counts

- implemented context functions: `12`
- stub context functions: `6`
- no-callsite context functions: `0`
- candidate-level proof rows: `0`

## Readiness decision

Domain and pivot remain `none`; code readiness remains blocked until RE-382 gates the callsite map.
