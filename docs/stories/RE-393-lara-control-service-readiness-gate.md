# RE-393 lara control service readiness gate

## Goal

Gate the RE-392 lara-control-service candidate and decide whether source-symbolic context can reopen a proof domain.

## Inputs

- Upstream handoff: `docs/reverse/generated/re392-ghidra-lara-combat-camera-cluster-narrow-handoff.csv`
- Candidate rows: `docs/reverse/generated/re392-ghidra-lara-combat-camera-cluster-narrow-candidates.csv`

## Progress tracker

- [x] RE-392 lara-control-service handoff validated.
- [x] Selected candidate queue gated fail-closed.
- [x] Source-symbolic lara-control context counted as prioritization signal only.
- [x] Domain and pivot selection kept blocked.
- [x] Source/code patch authorization denied.
- [x] Next deferred lara/combat/camera subcluster selection queued.

## Generated artifacts

- `docs/reverse/generated/re393-lara-control-service-readiness-gate-candidates.csv`
- `docs/reverse/generated/re393-lara-control-service-readiness-gate-gates.csv`
- `docs/reverse/generated/re393-lara-control-service-readiness-gate-summary.csv`
- `docs/reverse/generated/re393-lara-control-service-readiness-gate-handoff.csv`
- `docs/reverse/functions/re393-lara-control-service-readiness-gate.md`

## Findings

- Selected narrow subcluster: `lara-control-service`
- Input candidate count: `1`
- Candidate-level proof rows: `0`
- Ready to reopen domain selection: `0`
- Source patch authorized rows: `0`

## Readiness decision

The lara-control-service queue is source-symbolic only. Domain and pivot stay `none` / `none`, and code readiness remains `blocked` pending candidate-level proof in a later queue.

## Follow-up ticket breakdown

- `RE-394` / `lara-combat-camera-post-lara-control-next-subcluster-selection`: close `lara-control-service` and select the next deferred RE-392 lara/combat/camera subcluster.
  - Inputs: RE-393 handoff and RE-392 narrowed subcluster/candidate CSVs.
  - Deliverables: transition selection rows, summary/handoff, story.
  - Stop condition: select the next deferred subcluster without reopening domain/source/code readiness.

## Validation commands

- `python -m pytest tests/reverse/test_re393_lara_control_service_readiness_gate.py -q`
- `python scripts/reverse/re393_lara_control_service_readiness_gate.py --repo .`
- `python -m pytest tests/reverse -q`
