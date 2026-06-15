# RE-175 — geometry-support-equivalence-gate

## Goal
Advance `geometry-support` in `module-spec_psxpc_n` using metadata-only proof artifacts.

## Progress tracker
- [x] consumed upstream scope/plan
- [x] emitted deterministic metadata-only artifacts
- [x] kept source and marker changes blocked
- [x] recorded validation path and next dependency

## Generated artifacts
- `docs/reverse/generated/re175-geometry-support-equivalence-gate.csv`
- `docs/reverse/generated/re171-re177-geometry-support-chain.csv`
- `docs/reverse/functions/re171-re177-geometry-support-chain.md`

## Findings
- equivalence gate has zero code-change-ready rows
- non-raw binary equivalence proof remains the blocker

## Readiness decision
- status: `completed-documentation-only`
- decision: `blocked-no-source-or-marker-change`
- code change readiness: `blocked`
- next ticket: `RE-176`

## Validation
- `python3 -m pytest tests/reverse/test_re171_re177_geometry_support_chain.py -q`
- `python3 -m pytest tests/reverse -q`
- metadata-only guard over generated RE-171..RE-177 artifacts
