# RE-309 Ghidra unmapped bridge candidates

## Goal

Use the available Ghidra function export proactively after RE-308 to produce a safe source-symbolic candidate list for further reverse-engineering exploration.

## Inputs

- Upstream handoff: `docs/reverse/generated/re308-new-non-raw-proof-evidence-exploration-handoff.csv`
- Ghidra export: `docs/reverse/generated/ghidra-functions.csv`
- Repo mapping: `docs/reverse/generated/repo-function-map.csv`
- Mapping summary: `docs/reverse/generated/function-map-summary.json`

## Progress tracker

- [x] RE-308 handoff validated.
- [x] Ghidra function export consumed as source-symbolic metadata.
- [x] Repo mapped symbols joined to unmapped Ghidra caller/callee bridges.
- [x] Raw Ghidra names and entry addresses excluded from versioned candidate rows.
- [x] Source/code readiness remains blocked pending a readiness gate.

## Generated artifacts

- `docs/reverse/generated/re309-ghidra-unmapped-bridge-candidates.csv`
- `docs/reverse/generated/re309-ghidra-unmapped-bridge-candidates-summary.csv`
- `docs/reverse/generated/re309-ghidra-unmapped-bridge-candidates-handoff.csv`
- `docs/reverse/functions/re309-ghidra-unmapped-bridge-candidates.md`

## Findings

- Ghidra functions: `1440`
- Ghidra-only functions: `723`
- Bridge candidates: `317`
- Top testable-now candidates emitted: `25`
- Ready to reopen proof-domain selection: `0`
- Source patch authorized rows: `0`

## Readiness decision

The new source-symbolic export is ready for gating, but it is not yet a proof-domain selection. No production source or marker change is authorized.

## Follow-up ticket breakdown

- `RE-310` / `ghidra-bridge-candidate-readiness-gate`: gate the top bridge candidates, group them by source-symbolic context, and decide whether one can open a proof-first domain.
  - Inputs: RE-309 candidate CSV plus the existing Ghidra/repo map exports.
  - Stop condition: if every candidate remains generic helper context, keep selected domain/pivot `none` and request a narrower Ghidra export.

## Validation commands

- `python -m pytest tests/reverse/test_re309_ghidra_unmapped_bridge_candidates.py -q`
- `python scripts/reverse/re309_ghidra_unmapped_bridge_candidates.py --repo .`
- `python -m pytest tests/reverse -q`
