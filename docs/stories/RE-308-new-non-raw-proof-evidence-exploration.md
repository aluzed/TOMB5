# RE-308 new non-raw proof evidence exploration

## Goal

Explore the safe continuation path requested after RE-307 by checking whether a changed upstream mapping or new non-raw proof evidence is available before any domain selection.

## Inputs

- Upstream handoff: `docs/reverse/generated/re307-blocker-reduction-source-exhaustion-audit-handoff.csv`
- Existing generated metadata and story/Markdown taxonomies, counted only as exhausted context.
- Checked-in source-symbolic corpus, counted as context rather than proof readiness.

## Progress tracker

- [x] RE-307 exhaustion handoff validated.
- [x] Safe exploration vectors enumerated.
- [x] Existing metadata-only context classified as exhausted, not testable-now.
- [x] Unsafe evidence class rejected from committed outputs.
- [x] Source/code readiness remains blocked.

## Generated artifacts

- `docs/reverse/generated/re308-new-non-raw-proof-evidence-exploration.csv`
- `docs/reverse/generated/re308-new-non-raw-proof-evidence-exploration-summary.csv`
- `docs/reverse/generated/re308-new-non-raw-proof-evidence-exploration-handoff.csv`
- `docs/reverse/functions/re308-new-non-raw-proof-evidence-exploration.md`

## Findings

- Exploration vectors: `6`
- Testable now: `0`
- Need new export: `2`
- Exhausted metadata: `2`
- Missing user input: `1`
- Unsafe input class: `1`
- Ready to reopen proof-domain selection: `0`
- Source patch authorized rows: `0`

## Readiness decision

The exploration did not find a current testable-now vector. Existing metadata remains exhausted/gated blocked, the source-symbolic corpus is context only, and unsafe evidence classes are rejected. Domain and source readiness remain blocked.

## Follow-up ticket breakdown

- `TBD` / `changed-upstream-mapping-refresh`: run only after a changed `repo-function-map.csv` or equivalent priority export is available.
  - Inputs: changed safe mapping/export artifact.
  - Stop condition: no mapping delta keeps selected domain/pivot `none`.
- `TBD` / `new-safe-proof-evidence-intake`: run only after a new metadata-only or source-symbolic proof artifact is supplied.
  - Inputs: safe proof artifact, path, or generated export; no unsafe binary/asset-derived payloads.
  - Stop condition: artifact does not establish an actionable non-raw proof vector.

## Validation commands

- `python -m pytest tests/reverse/test_re308_new_non_raw_proof_evidence_exploration.py -q`
- `python scripts/reverse/re308_new_non_raw_proof_evidence_exploration.py --repo .`
- `python -m pytest tests/reverse -q`
