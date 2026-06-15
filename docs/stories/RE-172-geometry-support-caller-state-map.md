# RE-172 — geometry-support-caller-state-map

## Goal
Advance `geometry-support` in `module-spec_psxpc_n` using metadata-only proof artifacts.

## Progress tracker
- [x] consumed upstream scope/plan
- [x] emitted deterministic metadata-only artifacts
- [x] kept source and marker changes blocked
- [x] recorded validation path and next dependency

## Generated artifacts
- `docs/reverse/generated/re172-geometry-support-caller-state-map.csv`
- `docs/reverse/generated/re171-re177-geometry-support-chain.csv`
- `docs/reverse/functions/re171-re177-geometry-support-chain.md`

## Findings
- source-backed callsites mapped without synthetic edges
- caller keyword artifacts rejected

## Readiness decision
- status: `completed-documentation-only`
- decision: `blocked-no-source-or-marker-change`
- code change readiness: `blocked`
- next ticket: `RE-173`

## Validation
- `python3 -m pytest tests/reverse/test_re171_re177_geometry_support_chain.py -q`
- `python3 -m pytest tests/reverse -q`
- metadata-only guard over generated RE-171..RE-177 artifacts
