# RE-227 — traps-switches-doors-source-patch-gate

Status: Done

## Goal

Advance `traps-switches-doors-source-patch-gate` within the traps-switches-doors epic using metadata-only proof artifacts.

## Scope

- scope: `ready traps-switches-doors rows`
- candidates: `20`
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
Blocker: `missing-traps-switches-doors-source-contract-and-non-raw-equivalence-proof`

## Validation

- `python3 -m pytest tests/reverse/test_re222_re228_traps_switches_doors_epic.py -q`
- `python3 -m pytest tests/reverse -q`
- metadata-only guard over RE-222..RE-228 outputs

## Next step

Epic handoff: `RE-229` / `module-spec-psxpc-proof-first-audit`.
