# RE-163 — Module SPEC_PSXPC_N proof-first audit

Status: Done

## Goal

Open the `module-spec_psxpc_n` proof chain selected by RE-162 and scope the `PrintString` pivot without changing production source or completion markers.

## Progress

- [x] RE-162 selection loaded.
- [x] RE-044 domain row consumed.
- [x] SPEC_PSXPC_N candidates classified into proof clusters.
- [x] Blockers and follow-up ticket plan recorded.
- [x] Forbidden raw evidence excluded from generated outputs.

## Generated artifacts

- `docs/reverse/generated/re163-module-spec-psxpc-n-proof-first-audit.csv`
- `docs/reverse/generated/re163-module-spec-psxpc-n-clusters.csv`
- `docs/reverse/generated/re163-module-spec-psxpc-n-ticket-plan.csv`
- `docs/reverse/functions/re163-module-spec-psxpc-n-proof-first-audit.md`

## Readiness decision

- code change readiness: `blocked`
- marker readiness: `blocked`
- selected cluster: `ui-text-rendering`
- next ticket: `RE-164`

No production source or marker change is authorized by RE-163. The next step is a metadata-only caller/side-effect map for `PrintString` and related ui text rendering support rows.

## Follow-up ticket plan

- [ ] `RE-164` `ui-text-rendering-caller-side-effect-map`: Map PrintString/GetStringLength callsites, callers, flags, text sources, and visible side-effect categories.
- [ ] `RE-165` `ui-text-rendering-argument-taxonomy`: Classify PrintString coordinate, colour, string source, and flag argument shapes into stable metadata categories.
- [ ] `RE-166` `ui-text-rendering-state-contract`: Document text/font/global state dependencies and blockers for safe reconstruction or marker decisions.
- [ ] `RE-167` `ui-text-rendering-equivalence-gate`: Compare source-level semantics against non-raw binary metadata without versioning instruction text or addresses.
- [ ] `RE-168` `ui-text-rendering-source-patch-gate`: Apply a minimal source or marker patch only if RE-167 marks rows ready.
- [ ] `RE-169` `module-spec-psxpc-n-next-cluster-selection`: Select the next SPEC_PSXPC_N cluster after ui text rendering closes or blocks.
- [ ] `RE-170` `module-spec-psxpc-n-closure-or-handoff`: Close the module SPEC_PSXPC_N domain when clusters are proved or terminally blocked, then hand off to the next domain.

## Validation

- `python3 -m pytest tests/reverse/test_re163_module_spec_psxpc_n_audit.py -q`
- `python3 -m pytest tests/reverse -q`
- metadata-only guard over RE-163 generated outputs
