# RE-305 handoff stop-condition reduction

## Goal

Reduce safe handoff CSV stop-condition metadata into reusable classes before any proof-domain selection can reopen.

## Inputs

- Upstream handoff: `docs/reverse/generated/re304-source-patch-gate-denial-readiness-gate-handoff.csv`
- Candidate source: `docs/reverse/generated/re296-blocker-reduction-candidate-selection.csv` / `handoff-csvs`
- Scanned source: `docs/reverse/generated/*handoff*.csv` with RE-305+ outputs excluded.

## Progress tracker

- [x] RE-304 source-patch denial readiness gate handoff validated.
- [x] RE-296 handoff-csvs metadata candidate validated.
- [x] Handoff stop-condition fields normalized without raw text columns.
- [x] Taxonomy, evidence, summary, and handoff artifacts generated.
- [x] Source/code readiness remains blocked.

## Generated artifacts

- `docs/reverse/generated/re305-handoff-stop-condition-reduction.csv`
- `docs/reverse/generated/re305-handoff-stop-condition-reduction-evidence.csv`
- `docs/reverse/generated/re305-handoff-stop-condition-reduction-summary.csv`
- `docs/reverse/generated/re305-handoff-stop-condition-reduction-handoff.csv`
- `docs/reverse/functions/re305-handoff-stop-condition-reduction.md`

## Findings

- Handoff files scanned: `50`
- Stop-condition evidence rows: `50`
- Normalized classes: `5`
- Domain-selection-ready classes: `0`
- Source-patch-authorized classes: `0`

- `proof-blocked-or-no-marker-patch`: `27` rows, readiness `no`.
- `metadata-reduction-before-domain-selection`: `12` rows, readiness `no`.
- `generic-handoff-stop-condition`: `7` rows, readiness `no`.
- `upstream-input-refresh-or-change-needed`: `3` rows, readiness `no`.
- `readiness-gate-before-domain-selection`: `1` rows, readiness `no`.

## Readiness decision

The handoff stop-condition taxonomy is metadata-reduction-ready but not proof-domain-selection-ready. It does not introduce a selected domain/pivot, non-raw equivalence proof, or source patch authorization.

## Follow-up ticket breakdown

- `RE-306` / `handoff-stop-condition-readiness-gate`: gate the handoff stop-condition taxonomy and decide whether any class can reopen proof-domain selection.
  - Inputs: RE-305 taxonomy, evidence, summary, and handoff artifacts.
  - Deliverables: readiness-gate CSV, summary, handoff, generated Markdown, and story tracker.
  - Stop condition: if all classes remain non-authorizing metadata, keep selected domain/pivot `none` and route to the next safe metadata source or evidence refresh.

## Validation commands

- `python -m pytest tests/reverse/test_re305_handoff_stop_condition_reduction.py -q`
- `python scripts/reverse/re305_handoff_stop_condition_reduction.py --repo .`
- `python -m pytest tests/reverse -q`
