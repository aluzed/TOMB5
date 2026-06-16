# RE-310 Ghidra bridge candidate readiness gate

## Goal

Gate the RE-309 Ghidra bridge candidates by source-symbolic context and decide whether any candidate can reopen proof-domain selection.

## Inputs

- Upstream handoff: `docs/reverse/generated/re309-ghidra-unmapped-bridge-candidates-handoff.csv`
- Candidate export: `docs/reverse/generated/re309-ghidra-unmapped-bridge-candidates.csv`

## Progress tracker

- [x] RE-309 candidate export validated.
- [x] Candidates grouped by safe source-symbolic context.
- [x] Cluster-level readiness gate emitted.
- [x] Source/marker patch authorization denied for every row.
- [x] Follow-up narrow export selected before proof-domain reopening.

## Generated artifacts

- `docs/reverse/generated/re310-ghidra-bridge-candidate-readiness-gate-clusters.csv`
- `docs/reverse/generated/re310-ghidra-bridge-candidate-readiness-gate-candidates.csv`
- `docs/reverse/generated/re310-ghidra-bridge-candidate-readiness-gate-summary.csv`
- `docs/reverse/generated/re310-ghidra-bridge-candidate-readiness-gate-handoff.csv`
- `docs/reverse/functions/re310-ghidra-bridge-candidate-readiness-gate.md`

## Findings

- Input candidates: `25`
- Source-symbolic clusters: `7`
- Selected follow-up cluster: `collision-switch-door-cluster`
- Focus candidates: `7`
- Ready to reopen domain selection: `0`
- Source patch authorized rows: `0`

## Readiness decision

The gate selects a narrowed metadata follow-up, not a proof domain. Domain/pivot remain `none` and code readiness remains blocked.

## Follow-up ticket breakdown

- `RE-311` / `ghidra-collision-switch-door-cluster-narrow-export`: produce a narrower metadata-only source-symbolic export for the selected collision/switch/door cluster.
  - Inputs: RE-310 clusters/candidates plus RE-309 candidate IDs and local Ghidra/repo maps.
  - Deliverables: cluster-specific candidate metadata, blocker rows, and a readiness handoff that still excludes raw Ghidra addresses/names from versioned outputs.
  - Stop condition: if the narrow export still cannot separate a proof-first pivot, keep selected domain/pivot `none` and hand off to a more specific source-symbolic evidence request.

## Validation commands

- `python -m pytest tests/reverse/test_re310_ghidra_bridge_candidate_readiness_gate.py -q`
- `python scripts/reverse/re310_ghidra_bridge_candidate_readiness_gate.py --repo .`
- `python -m pytest tests/reverse -q`
