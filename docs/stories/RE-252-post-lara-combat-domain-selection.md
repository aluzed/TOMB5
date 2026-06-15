# RE-252 — post-lara-combat-domain-selection

Status: Done

## Goal

Advance `post-lara-combat-domain-selection` within the lara-combat epic using metadata-only proof artifacts.

## Scope

- scope: `remaining domain backlog after lara-combat`
- candidates: `0`
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
Blocker: `missing-lara-combat-source-contract-and-non-raw-equivalence-proof`

## Validation

- `python3 -m pytest tests/reverse/test_re245_re252_lara_combat_epic.py -q`
- `python3 -m pytest tests/reverse -q`
- metadata-only guard over RE-245..RE-252 outputs

## Next step

Epic handoff: `RE-253` / `inventory-proof-first-audit`.
