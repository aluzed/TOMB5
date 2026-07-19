# RE-393 lara control service readiness gate

## Purpose

Gate the RE-392 `lara-control-service` candidate before any proof-domain or source-patch decision.

## Inputs

- Upstream handoff: `docs/reverse/generated/re392-ghidra-lara-combat-camera-cluster-narrow-handoff.csv`
- Candidate rows: `docs/reverse/generated/re392-ghidra-lara-combat-camera-cluster-narrow-candidates.csv`

## Decision

No proof-domain is reopened by this gate. The selected candidate has source-symbolic lara-control context, but no candidate-level proof rows.

## Counts

- Input candidates: `1`
- Candidate-level proof rows: `0`
- Ready to reopen domain: `0`
- Source patch authorized: `0`

## Handoff

- Next ticket: `RE-394`
- Next topic: `lara-combat-camera-post-lara-control-next-subcluster-selection`
- Stop condition: `lara control service candidate queue exhausted without candidate-level proof; select next deferred lara/combat/camera subcluster`
