# RE-367 runtime callee bridge candidate callsite map

## Summary

Mapped `1` source-backed callsite metadata row across `11` runtime/callee bridge context functions.
Source-backed callsite rows are not source-patch authorization; they are an input to the next readiness gate.

## Counts

- implemented context functions: `1`
- stub context functions: `1`
- no-callsite context functions: `9`
- candidate-level proof rows: `0`

## Readiness decision

Domain and pivot remain `none`; code readiness remains blocked until RE-368 gates the callsite map.
