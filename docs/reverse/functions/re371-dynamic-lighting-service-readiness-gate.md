# RE-371 dynamic-lighting service readiness gate

## Purpose

Gate the RE-370 `dynamic-lighting-service` candidate set before any proof-domain or source-patch decision.

## Inputs

- Upstream handoff: `docs/reverse/generated/re370-ghidra-effects-lighting-narrow-handoff.csv`
- Candidate rows: `docs/reverse/generated/re370-ghidra-effects-lighting-narrow-candidates.csv`

## Decision

No proof-domain is reopened by this gate. The candidates remain source-symbolic context only because candidate-level proof is still missing.

## Counts

- Input candidates: `2`
- Gate rows: `1`
- Ready to reopen domain: `0`
- Source patch authorized: `0`

## Handoff

- Selected follow-up candidate: `f5d0099b5511`
- Next ticket: `RE-372`
- Next topic: `dynamic-lighting-service-candidate-proof-export`
- Code readiness: `blocked`
- Stop condition: `dynamic-lighting candidates lack candidate-level proof; export still narrower proof context before proof-domain selection`
