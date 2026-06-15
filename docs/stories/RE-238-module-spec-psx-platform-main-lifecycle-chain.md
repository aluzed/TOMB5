# RE-238 — module-spec-psx-platform-main-lifecycle-chain

Status: Done

## Goal

Advance `module-spec-psx-platform-main-lifecycle-chain` within the module-spec_psx epic using metadata-only proof artifacts.

## Scope

- scope: `platform-main-lifecycle candidates`
- candidates: `3`
- source contract: generated metadata only; no source or marker edit

## Progress tracker

- [x] Upstream handoff consumed.
- [x] Story outcome generated deterministically.
- [x] Readiness and blocker recorded.
- [x] No production source or marker change is authorized.

## Readiness

Readiness: `blocked`
Source patch ready: `no`
Marker ready: `no`
Blocker: `missing-module-spec-psx-source-contract-and-non-raw-equivalence-proof`

## Validation

- `python3 -m pytest tests/reverse/test_re237_re244_module_spec_psx_epic.py -q`
- `python3 -m pytest tests/reverse -q`
- metadata-only guard over RE-237..RE-244 outputs

## Next step

Epic handoff: `RE-245` / `lara-combat-proof-first-audit`.
