# RE-091 — Object runtime validation regression

Status: Done

## Goal

Advance `torch-and-flare-control` within `gameflow-runtime-control` using metadata-only evidence for RE-091.

## Progress tracker

- [x] RE-085 ticket plan consumed.
- [x] Torch/flare object runtime metadata mapped.
- [x] Patch and marker readiness checked.
- [x] Forbidden evidence excluded from generated artifacts.

## Generated artifacts

- `docs/reverse/generated/re086-re092-object-runtime-chain.csv`
- `docs/reverse/generated/re086-object-runtime-scope.csv`
- `docs/reverse/generated/re086-object-runtime-callsite-map.csv`
- `docs/reverse/generated/re087-object-runtime-argument-state-taxonomy.csv`
- `docs/reverse/generated/re092-object-runtime-handoff.csv`
- `docs/reverse/functions/re086-re092-object-runtime-chain.md`

## Findings

- torch/flare control rows are source-level stubs in this branch
- no source or marker patch is admitted without object state source body proof and symbolic equivalence proof
- continue current chain

## Readiness decision

- decision: `metadata-validation-published`
- code change readiness: `blocked`
- next ticket: `RE-092`

Do not patch production source or add/remove proof markers from this story alone.

## Validation

- `python3 -m pytest tests/reverse/test_re086_re092_object_runtime_chain.py -q`
- `python3 -m pytest tests/reverse -q`
- metadata-only guard over generated RE-086..RE-092 artifacts
