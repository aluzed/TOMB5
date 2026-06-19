# RE-360 gpu/fmv mainloop service readiness gate

## Purpose

Gate the RE-359 `gpu-fmv-mainloop-service` candidate set before any proof-domain or source-patch decision.

## Inputs

- Upstream handoff: `docs/reverse/generated/re359-platform-frontend-service-post-frontend-display-menu-next-subcluster-selection-handoff.csv`
- Candidate rows: `docs/reverse/generated/re359-platform-frontend-service-post-frontend-display-menu-next-subcluster-selection-candidates.csv`
- Source-context metadata: `docs/reverse/generated/re343-ghidra-platform-frontend-service-narrow-candidates.csv`

## Decision

No proof-domain is reopened by this gate. The candidate remains source-symbolic context only because candidate-level proof is still missing.

## Counts

- Input candidates: `1`
- Gate rows: `1`
- Ready to reopen domain: `0`
- Source patch authorized: `0`

## Handoff

- Selected follow-up candidate: `1b3534d34062`
- Next ticket: `RE-361`
- Next topic: `gpu-fmv-mainloop-service-candidate-proof-export`
- Code readiness: `blocked`
- Stop condition: `gpu/fmv mainloop candidate lacks candidate-level proof; export still narrower proof context before proof-domain selection`
