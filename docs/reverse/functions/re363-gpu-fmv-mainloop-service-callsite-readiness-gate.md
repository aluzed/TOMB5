# RE-363 gpu/fmv mainloop service callsite readiness gate

## Summary

Gated `8` source-backed callsite families for candidate `1b3534d34062`.
No gpu/fmv mainloop callsite family proves candidate-level behavior, so the proof domain and pivot remain `none`.

## Family gates

- `load-file-helper`: `21` rows, gate `blocked-no-candidate-level-proof`.
- `gpu-display-helper`: `18` rows, gate `blocked-no-candidate-level-proof`.
- `profiling-helper`: `15` rows, gate `blocked-no-candidate-level-proof`.
- `audio-sound-helper`: `12` rows, gate `blocked-no-candidate-level-proof`.
- `memory-allocation-helper`: `9` rows, gate `blocked-no-candidate-level-proof`.
- `platform-lifecycle-helper`: `6` rows, gate `blocked-no-candidate-level-proof`.
- `movie-playback-helper`: `3` rows, gate `blocked-no-candidate-level-proof`.
- `text-ui-helper`: `3` rows, gate `blocked-no-candidate-level-proof`.

## Readiness decision

- candidate-level proof rows: `0`
- ready-to-reopen rows: `0`
- source-patch authorized rows: `0`
- next deferred candidate: `none`
- next subcluster: `runtime-callee-bridge`
- next ticket: `RE-364` / `platform-frontend-service-post-gpu-fmv-mainloop-next-subcluster-selection`

Code readiness remains `blocked`.
