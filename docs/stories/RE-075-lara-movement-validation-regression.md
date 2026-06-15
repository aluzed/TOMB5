# RE-075 — Lara movement validation regression

Status: Done

## Goal

Advance `ledge-and-vault-tests` within `lara-movement-support` using metadata-only evidence for RE-075.

## Progress tracker

- [x] RE-069 plan consumed.
- [x] Source-level movement metadata mapped.
- [x] Patch readiness checked.
- [x] Forbidden raw evidence excluded.

## Generated artifacts

- `docs/reverse/generated/re070-re076-lara-movement-chain.csv`
- `docs/reverse/generated/re070-lara-movement-scope.csv`
- `docs/reverse/generated/re070-lara-movement-callsite-map.csv`
- `docs/reverse/generated/re071-lara-movement-argument-state-taxonomy.csv`
- `docs/reverse/generated/re076-lara-movement-handoff.csv`
- `docs/reverse/functions/re070-re076-lara-movement-chain.md`

## Findings

- source-level caller/state metadata is available
- no source or marker patch is admitted without non-raw binary equivalence proof
- continue current chain

## Readiness decision

- decision: `metadata-validation-published`
- code change readiness: `blocked`
- next ticket: `RE-076`

Do not patch production source or add/remove proof markers from this story alone.

## Validation

- `python3 -m pytest tests/reverse/test_re070_re076_lara_movement_chain.py -q`
- `python3 -m pytest tests/reverse -q`
- metadata-only guard over generated RE-070..RE-076 artifacts
