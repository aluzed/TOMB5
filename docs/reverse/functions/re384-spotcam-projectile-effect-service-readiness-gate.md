# RE-384 spotcam/projectile effect service readiness gate

## Purpose

Gate the RE-383 `spotcam-projectile-effect-service` candidate before any proof-domain or source-patch decision.

## Inputs

- Upstream handoff: `docs/reverse/generated/re383-effects-lighting-cluster-post-explosion-flare-next-subcluster-selection-handoff.csv`
- Candidate rows: `docs/reverse/generated/re383-effects-lighting-cluster-post-explosion-flare-next-subcluster-selection-candidates.csv`

## Decision

No proof-domain is reopened by this gate. The candidate remains source-symbolic context only because candidate-level proof is still missing.

## Counts

- Input candidates: `1`
- Gate rows: `1`
- Ready to reopen domain: `0`
- Source patch authorized: `0`

## Handoff

- Selected follow-up candidate: `b6d128932004`
- Next ticket: `RE-385`
- Next topic: `spotcam-projectile-effect-service-candidate-proof-export`
- Code readiness: `blocked`
- Stop condition: `spotcam/projectile effect candidate lacks candidate-level proof; export still narrower proof context before proof-domain selection`
