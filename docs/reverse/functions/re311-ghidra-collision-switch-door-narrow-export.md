# RE-311 Ghidra collision/switch/door narrow export

## Summary

Narrowed `7` focus candidates into `5` source-symbolic subclusters.
The raw Ghidra identity remains local-only; versioned rows use hashed candidate IDs and repo-symbol context.

## Subcluster decisions

- rank `1` `collision-geometry-helper`: candidates `3`, decision `gate-before-proof-domain`, next `collision-geometry-helper-readiness-gate`
- rank `2` `switch-door-control-helper`: candidates `1`, decision `defer-after-selected-subcluster`, next `defer-after-re312`
- rank `3` `weapon-switch-effect-helper`: candidates `1`, decision `defer-after-selected-subcluster`, next `defer-after-re312`
- rank `4` `door-save-runtime-helper`: candidates `1`, decision `defer-after-selected-subcluster`, next `defer-after-re312`
- rank `5` `camera-collision-helper`: candidates `1`, decision `defer-after-selected-subcluster`, next `defer-after-re312`

## Readiness decision

The narrow export is metadata-ready, but proof-domain selection and source/marker changes remain blocked until the selected subcluster is gated.
