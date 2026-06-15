# RE-213 — Post-module-spec_psxpc_n domain selection

Status: Done

## Goal

Select the next reverse-engineering proof domain after the exhausted module-spec_psxpc_n parent domain.

## Scope

- depends on: `RE-212`, `RE-162`
- safety contract: metadata-only generated rows; binary instruction text, proprietary dump records, and raw address literals stay out of versioned outputs

## Progress tracker

- [x] RE-212 module-spec_psxpc_n exhaustion handoff consumed.
- [x] Closed/exhausted domains excluded.
- [x] Next-domain shortlist generated in logical order.
- [x] Readiness decision recorded.
- [x] Forbidden raw evidence excluded.

## Generated artifacts

- `docs/reverse/generated/re213-post-module-spec-psxpc-n-domain-selection.csv`
- `docs/reverse/generated/re213-post-module-spec-psxpc-n-domain-selection-handoff.csv`
- `docs/reverse/functions/re213-post-module-spec-psxpc-n-domain-selection.md`

## Findings

- selected next domain: `maths-render-support`
- selected pivot: `mTranslateXYZ`
- excluded closed/exhausted domains: `module-spec_psxpc_n`
- all rows remain blocked for source or marker changes until a domain-specific proof-first audit runs

## Selection decision

Recommended next ticket: `RE-214`
Code-change readiness: `documentation-only-selection-gate`
No production source or marker change is authorized by this selection gate.

## Validation

- `python3 -m pytest tests/reverse/test_re213_post_module_spec_psxpc_n_reprioritization.py -q`
- metadata-only guard over RE-213 outputs

## Next step

RE-214: open a proof-first audit for `maths-render-support` / `mTranslateXYZ`.
