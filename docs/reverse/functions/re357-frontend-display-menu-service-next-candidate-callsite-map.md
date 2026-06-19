# RE-357 frontend display/menu service next candidate callsite map

## Summary

Mapped `126` source-backed callsite metadata rows across `18` candidate context functions.
Source-backed callsite rows are still not source-patch authorization; they are an input to the next readiness gate.

## Counts

- implemented context functions: `17`
- stub context functions: `0`
- no-callsite context functions: `1`
- candidate-level proof rows: `0`

## Readiness decision

Domain and pivot remain `none`; code readiness remains blocked until RE-358 gates the next-candidate callsite map.
