# RE-394 lara combat camera post lara control next subcluster selection

## Purpose

Close the exhausted lara-control path and select the next deferred lara/combat/camera subcluster without authorizing a proof domain or source patch.

## Inputs

- Exhaustion handoff: `docs/reverse/generated/re393-lara-control-service-readiness-gate-handoff.csv`
- Parent subcluster queue: `docs/reverse/generated/re392-ghidra-lara-combat-camera-cluster-narrow-subclusters.csv`
- Parent candidates: `docs/reverse/generated/re392-ghidra-lara-combat-camera-cluster-narrow-candidates.csv`

## Selection

Selected `combat-camera-service` with `1` source-symbolic candidate.

## Readiness

Domain and pivot remain `none` / `none`. Code readiness remains `blocked` pending candidate-level proof.

## Handoff

- Next ticket: `RE-395`
- Next topic: `combat-camera-service-readiness-gate`
- Stop condition: `lara control service queue exhausted; select next deferred lara/combat/camera subcluster`
