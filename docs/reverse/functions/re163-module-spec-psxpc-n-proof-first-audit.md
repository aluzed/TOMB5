# RE-163 — Module SPEC_PSXPC_N proof-first audit

## Scope

- Domain: `module-spec_psxpc_n`
- Selected pivot: `PrintString`
- Selected initial cluster: `ui-text-rendering`
- Inputs: `docs/reverse/generated/re162-post-module-game-domain-reprioritization.csv`, `docs/reverse/generated/re044-domain-reprioritization.csv`, `docs/reverse/generated/function-priority.csv`

## Summary

- candidates from upstream domain row: `27`
- mapped candidates from upstream domain row: `27`
- ND candidates from upstream domain row: `7`
- runtime candidates from upstream domain row: `5`
- classified non-keyword candidates emitted: `24`
- clusters: `7`
- code-change-ready candidates: `0`
- marker-ready candidates: `0`
- Recommended next ticket: `RE-164`

## Cluster classification

- `ui-text-rendering`: 2 candidate(s), readiness `best-initial-proof-cluster`, next `RE-164`.
- `geometry-support`: 7 candidate(s), readiness `proof-needed`, next `defer`.
- `platform-gpu-display`: 4 candidate(s), readiness `nd-marker-audit-later`, next `after-RE-164`.
- `frontend-loadsave`: 3 candidate(s), readiness `proof-needed`, next `defer`.
- `platform-main-lifecycle`: 3 candidate(s), readiness `nd-marker-audit-later`, next `after-RE-164`.
- `platform-memory`: 3 candidate(s), readiness `nd-marker-audit-later`, next `after-RE-164`.
- `frontend-sequence`: 2 candidate(s), readiness `proof-needed`, next `defer`.

## Readiness decision

This is a proof-first audit gate. No production source or marker change is authorized until caller/state contracts and non-raw equivalence evidence are published. Current code change readiness: `blocked`.

## Multi-ticket plan

- `RE-164` `ui-text-rendering-caller-side-effect-map` — Map PrintString/GetStringLength callsites, callers, flags, text sources, and visible side-effect categories. Exit: Caller/state map published with source-backed callsite rows only.
- `RE-165` `ui-text-rendering-argument-taxonomy` — Classify PrintString coordinate, colour, string source, and flag argument shapes into stable metadata categories. Exit: Taxonomy distinguishes source-backed shapes from unproven runtime payload assumptions.
- `RE-166` `ui-text-rendering-state-contract` — Document text/font/global state dependencies and blockers for safe reconstruction or marker decisions. Exit: State-contract matrix either unblocks a comparison gate or records exact remaining blockers.
- `RE-167` `ui-text-rendering-equivalence-gate` — Compare source-level semantics against non-raw binary metadata without versioning instruction text or addresses. Exit: Readiness matrix names any code-change-ready or marker-ready rows, otherwise remains blocked.
- `RE-168` `ui-text-rendering-source-patch-gate` — Apply a minimal source or marker patch only if RE-167 marks rows ready. Exit: Patch/build/tests pass, or a no-patch blocker is published.
- `RE-169` `module-spec-psxpc-n-next-cluster-selection` — Select the next SPEC_PSXPC_N cluster after ui text rendering closes or blocks. Exit: Next cluster/handoff artifact names the smallest useful proof gate.
- `RE-170` `module-spec-psxpc-n-closure-or-handoff` — Close the module SPEC_PSXPC_N domain when clusters are proved or terminally blocked, then hand off to the next domain. Exit: Closure or exhausted handoff is emitted with next objective.

## Safety contract

Generated rows are metadata-only: symbolic function names, source paths, counts, clusters, blockers, and ticket IDs. Raw binary evidence, instruction text, machine words, raw branch/call targets, payload coordinates, and copied dump records are excluded.
