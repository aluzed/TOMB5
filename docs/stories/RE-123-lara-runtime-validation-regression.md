# RE-123 — Lara runtime validation regression

Status: Done

## Goal

Advance `lara-runtime-control` within `gameflow-runtime-control` using metadata-only evidence for RE-123.

## Progress tracker

- [x] RE-117 ticket plan consumed.
- [x] Lara-runtime metadata mapped.
- [x] Patch and marker readiness checked.
- [x] Forbidden evidence excluded from generated artifacts.

## Generated artifacts

- `docs/reverse/generated/re118-re124-lara-runtime-chain.csv`
- `docs/reverse/generated/re118-lara-runtime-scope.csv`
- `docs/reverse/generated/re118-lara-runtime-callsite-map.csv`
- `docs/reverse/generated/re119-lara-runtime-argument-state-taxonomy.csv`
- `docs/reverse/generated/re124-lara-runtime-handoff.csv`
- `docs/reverse/functions/re118-re124-lara-runtime-chain.md`

## Findings

- lara-runtime rows include one source-visible LaraControl path with blocked proof gate
- no source or marker patch is admitted without Lara runtime state proof and symbolic equivalence proof
- continue current chain

## Readiness decision

- decision: `metadata-validation-published`
- code change readiness: `blocked`
- next ticket: `RE-124`

Do not patch production source or add/remove proof markers from this story alone.

## Validation

- `python3 -m pytest tests/reverse/test_re118_re124_lara_runtime_chain.py -q`
- `python3 -m pytest tests/reverse -q`
- metadata-only guard over generated RE-118..RE-124 artifacts
