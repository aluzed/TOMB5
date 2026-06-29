# RE-387 spotcam/projectile effect service callsite readiness gate

## Progress tracker

- [x] RE-386 callsite-map handoff validated.
- [x] RE-384 single-candidate queue checked.
- [x] Parent RE-370 effects/lighting subcluster queue checked.
- [x] Callsite families gated with metadata-only outputs.
- [x] Domain/source/code readiness kept blocked.
- [x] Effects/lighting queue exhaustion handoff emitted.

## Gated families

- [x] Family `spotcam-projectile-helper` gated: `204` rows, `blocked-no-candidate-level-proof`.
- [x] Family `ambient-combat-effect-helper` gated: `32` rows, `blocked-no-candidate-level-proof`.
- [x] Family `room-floor-helper` gated: `16` rows, `blocked-no-candidate-level-proof`.
- [x] Family `runtime-effect-support` gated: `16` rows, `blocked-no-candidate-level-proof`.
- [x] Family `conversation-helper` gated: `6` rows, `blocked-no-candidate-level-proof`.
- [x] Family `audio-camera-helper` gated: `2` rows, `blocked-no-candidate-level-proof`.
- [x] Family `trap-effect-helper` gated: `1` rows, `blocked-no-candidate-level-proof`.
- [x] Family `stub-marker` gated: `19` rows, `blocked-stub-only-family`.

## Readiness decision

The selected candidate `b6d128932004` still has `0` candidate-level proof rows. Implemented source-backed helper families do not authorize a source patch without direct proof.

## Follow-up ticket breakdown

- Next ticket: `TBD`
- Next topic: `effects-lighting-cluster-subcluster-queue-exhausted`
- Next deferred candidate: `none`
- Next subcluster: `none`
- Stop condition: `spotcam/projectile candidate queue exhausted; effects/lighting service subcluster queue is exhausted`
