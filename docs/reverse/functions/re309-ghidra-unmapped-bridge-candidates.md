# RE-309 Ghidra unmapped bridge candidates

## Summary

Consumed the Ghidra function export and repo function map to identify `317` unmapped Ghidra functions that are connected to mapped source symbols.
The top `25` candidates are emitted as safe metadata for the next readiness gate.

No raw Ghidra function names or entry addresses are emitted in the versioned artifacts; candidate handles are hashed and source context uses repo symbols only.

## Top bridge classes

- `mapped-callee-bridge`: `2`
- `mapped-caller-callee-bridge`: `5`
- `mapped-caller-heavy`: `18`

## Readiness decision

The export is metadata-ready for a candidate readiness gate. It does not reopen proof-domain selection and does not authorize source or marker patches.
