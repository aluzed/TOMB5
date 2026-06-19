# RE-348 cd-load-audio service next candidate proof export

## Summary

Exported `18` source-symbolic context rows for next candidate `653df7c5909b` after previous candidate `1e35f3f4fb97` stayed blocked.
No proof-domain is reopened by this export; the candidate hash still lacks direct source-backed proof.

## Proof gate

- candidate `653df7c5909b`: contexts `18`, direct repo symbols `0`, gate `blocked-unmapped-candidate-identity`, next `cd-load-audio-service-next-candidate-callsite-map`

## Context families

- `cd-audio-service`: `15` rows
- `movie-playback`: `3` rows

## Readiness decision

The export is metadata-ready, but source/domain readiness remains blocked until a source-backed callsite map can prove candidate-level behavior without raw binary evidence.
