# RE-169 — Module SPEC_PSXPC_N next-cluster selection

Status: Done

## Goal

Select the next SPEC_PSXPC_N cluster after the UI text rendering no-patch gate.

## Scope

- depends on: `RE-168`, `RE-163`
- safety contract: metadata-only cluster ranking; no production source or marker updates

## Progress tracker

- [x] RE-168 no-patch handoff consumed.
- [x] Remaining SPEC_PSXPC_N clusters loaded from RE-163.
- [x] Next-cluster ranking emitted.
- [x] RE-170 handoff emitted.
- [x] Forbidden raw evidence excluded from generated artifacts.

## Generated artifacts

- `docs/reverse/generated/re169-module-spec-psxpc-n-next-cluster-selection.csv`
- `docs/reverse/generated/re169-module-spec-psxpc-n-next-cluster-handoff.csv`
- `docs/reverse/functions/re169-module-spec-psxpc-n-next-cluster-selection.md`

## Findings

- upstream cluster: `ui-text-rendering`
- upstream outcome: `ui-text-rendering-source-patch-denied`
- selected next cluster: `geometry-support`
- selected pivot: `GetBoundsAccurate`
- readiness: source and marker changes remain blocked pending cluster-specific proof

## Follow-up breakdown

- `RE-170` `module-spec-psxpc-n-closure-or-handoff`: consume this selection, decide whether `geometry-support` can open a bounded proof chain, or emit module closure/handoff.
- Stop condition: closure or handoff artifact names the next objective without touching source unless an explicit readiness gate marks rows ready.

## Validation

- `python3 -m pytest tests/reverse/test_re169_module_spec_psxpc_n_next_cluster_selection.py -q`
- `python3 -m pytest tests/reverse -q`
- metadata-only guard over RE-169 outputs

## Decision

Recommended next ticket: `RE-170`
Code-change readiness: `documentation-only-selection-gate`
No production source or marker change is authorized by this selection gate.
