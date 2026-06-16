# RE-310 Ghidra bridge candidate readiness gate

## Summary

Gated `25` RE-309 bridge candidates into `7` source-symbolic clusters.
No proof-domain is reopened by this gate; the selected follow-up is a narrower metadata export for one cluster.

## Cluster decisions

- rank `1` `collision-switch-door-cluster`: candidates `7`, decision `needs-narrow-source-symbolic-export`, next `ghidra-collision-switch-door-cluster-narrow-export`
- rank `2` `platform-frontend-service-cluster`: candidates `6`, decision `defer-after-focus-cluster`, next `defer-after-re311`
- rank `3` `effects-lighting-cluster`: candidates `4`, decision `defer-after-focus-cluster`, next `defer-after-re311`
- rank `4` `maths-render-cluster`: candidates `3`, decision `defer-after-focus-cluster`, next `defer-after-re311`
- rank `5` `lara-combat-camera-cluster`: candidates `2`, decision `defer-after-focus-cluster`, next `defer-after-re311`
- rank `6` `gameflow-save-runtime-cluster`: candidates `2`, decision `defer-after-focus-cluster`, next `defer-after-re311`
- rank `7` `actor-ai-cluster`: candidates `1`, decision `defer-after-focus-cluster`, next `defer-after-re311`

## Readiness decision

All candidates remain blocked for source/marker changes and for proof-domain reopening until a narrower source-symbolic export exists.

