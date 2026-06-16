# RE-306 handoff stop-condition readiness gate

## Goal

Gate the RE-305 handoff stop-condition taxonomy to decide whether proof-domain selection can reopen.

## Inputs

- Upstream handoff: `docs/reverse/generated/re305-handoff-stop-condition-reduction-handoff.csv`
- Taxonomy: `docs/reverse/generated/re305-handoff-stop-condition-reduction.csv`
- Evidence: `docs/reverse/generated/re305-handoff-stop-condition-reduction-evidence.csv`
- Candidate source: `docs/reverse/generated/re296-blocker-reduction-candidate-selection.csv` / `handoff-csvs`

## Progress tracker

- [x] RE-305 handoff stop-condition reduction handoff validated.
- [x] RE-305 taxonomy readiness flags verified as metadata-only/non-authorizing.
- [x] RE-305 evidence schema verified as fingerprint-only.
- [x] Readiness gate CSV, summary, handoff, Markdown, and story generated.
- [x] Source/code readiness remains blocked.

## Generated artifacts

- `docs/reverse/generated/re306-handoff-stop-condition-readiness-gate.csv`
- `docs/reverse/generated/re306-handoff-stop-condition-readiness-gate-summary.csv`
- `docs/reverse/generated/re306-handoff-stop-condition-readiness-gate-handoff.csv`
- `docs/reverse/functions/re306-handoff-stop-condition-readiness-gate.md`

## Findings

- Handoff stop-condition classes gated: `5`
- Ready to reopen proof-domain selection: `0`
- Classes needing new evidence/input changes: `5`
- Source patch authorized rows: `0`

- `proof-blocked-or-no-marker-patch`: `needs-new-non-raw-proof-evidence`, evidence `27`.
- `metadata-reduction-before-domain-selection`: `needs-new-non-raw-proof-evidence`, evidence `12`.
- `generic-handoff-stop-condition`: `needs-new-non-raw-proof-evidence`, evidence `7`.
- `upstream-input-refresh-or-change-needed`: `needs-upstream-input-change`, evidence `3`.
- `readiness-gate-before-domain-selection`: `needs-new-non-raw-proof-evidence`, evidence `1`.

## Readiness decision

The handoff stop-condition taxonomy is not proof-domain-selection-ready. It points to new non-raw proof evidence, changed upstream inputs, or a source-exhaustion audit rather than a safe source/marker patch.

## Follow-up ticket breakdown

- `RE-307` / `blocker-reduction-source-exhaustion-audit`: audit whether all blocker-reduction metadata sources from RE-296 have been reduced/gated and whether any safe source remains before another proof-domain selection attempt.
  - Inputs: RE-296 candidate list and RE-297..RE-306 reduction/gate handoffs.
  - Deliverables: exhaustion matrix, summary, handoff, generated Markdown, and story tracker.
  - Stop condition: if no safe metadata source or non-raw proof evidence remains, keep selected domain/pivot `none` and request changed upstream mapping or new non-raw evidence.

## Validation commands

- `python -m pytest tests/reverse/test_re306_handoff_stop_condition_readiness_gate.py -q`
- `python scripts/reverse/re306_handoff_stop_condition_readiness_gate.py --repo .`
- `python -m pytest tests/reverse -q`
