# RE-386 spotcam/projectile effect service candidate callsite map

## Summary

Mapped `296` source-backed callsite metadata rows across `52` spotcam/projectile candidate context functions.
Source-backed callsite rows are not source-patch authorization; they are an input to the next readiness gate.

## Counts

- implemented context functions: `33`
- stub context functions: `19`
- no-callsite context functions: `0`
- candidate-level proof rows: `0`

## Readiness decision

Domain and pivot remain `none`; code readiness remains blocked until RE-387 gates the callsite map.
