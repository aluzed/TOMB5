# RE-335 door-save-runtime helper candidate callsite map

## Summary

Mapped `185` source-backed callsite metadata rows across `14` candidate context functions.
Source-backed callsite rows are not source-patch authorization; they are an input to the next readiness gate.

## Counts

- implemented context functions: `13`
- stub context functions: `1`
- no-callsite context functions: `0`
- candidate-level proof rows: `0`

## Readiness decision

Domain and pivot remain `none`; code readiness remains blocked until RE-336 gates the callsite map.
