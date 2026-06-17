# RE-323 switch-door-control helper readiness gate

## Summary

Gated `1` switch-door-control helper candidate from RE-322.
No proof-domain is reopened by this gate; every row still needs candidate-level source-symbolic proof.

## Candidate gates

- rank `1` candidate `8d1fc6fc3cfc`: gate `blocked-needs-candidate-level-proof`, proof signal `caller-switch-door-control-context-only`, next `candidate-proof-export`

## Readiness decision

The selected subcluster has source-symbolic switch/door/control context, but not candidate-level proof sufficient to select a proof domain, pivot, source patch, or marker update.
The next safe action is `RE-324` / `switch-door-control-helper-candidate-proof-export` for candidate `8d1fc6fc3cfc`.
