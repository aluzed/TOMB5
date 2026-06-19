# RE-356 frontend display/menu service next candidate proof export

## Summary

Exported `18` source-symbolic context rows for next candidate `4c90c6af8f9d` after previous candidate `de919274685f` stayed blocked.
No proof-domain is reopened by this export; the candidate hash still lacks direct source-backed proof.

## Proof gate

- candidate `4c90c6af8f9d`: contexts `18`, direct repo symbols `0`, gate `blocked-unmapped-candidate-identity`, next `frontend-display-menu-service-next-candidate-callsite-map`

## Context families

- `cd-init-service`: `3` rows
- `file-service`: `6` rows
- `hud-display`: `1` rows
- `inventory-menu`: `2` rows
- `loadsave-menu`: `6` rows

## Readiness decision

The export is metadata-ready, but source/domain readiness remains blocked until a source-backed callsite map can prove candidate-level behavior without raw binary evidence.
