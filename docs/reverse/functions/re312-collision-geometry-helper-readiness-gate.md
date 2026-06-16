# RE-312 collision geometry helper readiness gate

## Summary

Gated `3` collision-geometry helper candidates from RE-311.
No proof-domain is reopened by this gate; every row still needs candidate-level source-symbolic proof.

## Candidate gates

- rank `1` candidate `5e99f39fd8ef`: gate `blocked-needs-candidate-level-proof`, proof signal `callee-geometry-context-only`, next `candidate-proof-export`
- rank `2` candidate `d96359c1d9f3`: gate `blocked-needs-candidate-level-proof`, proof signal `callee-geometry-context-only`, next `defer-after-re313`
- rank `3` candidate `61d55bb1809b`: gate `blocked-needs-candidate-level-proof`, proof signal `callee-geometry-context-only`, next `defer-after-re313`

## Readiness decision

The selected subcluster has source-symbolic context, but not candidate-level proof sufficient to select a proof domain, pivot, source patch, or marker update.
The next safe action is `RE-313` / `collision-geometry-helper-candidate-proof-export` for candidate `5e99f39fd8ef`.
