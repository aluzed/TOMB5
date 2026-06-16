# RE-307 blocker-reduction source exhaustion audit

## Goal

Audit whether the RE-296 blocker-reduction metadata sources have all been reduced and gated, and whether any safe source remains before selecting another proof domain.

## Inputs

- Upstream handoff: `docs/reverse/generated/re306-handoff-stop-condition-readiness-gate-handoff.csv`
- Candidate source list: `docs/reverse/generated/re296-blocker-reduction-candidate-selection.csv`
- Reduction/gate handoffs: RE-297 through RE-306.

## Progress tracker

- [x] RE-306 handoff stop-condition readiness gate validated.
- [x] RE-296 candidate source ordering and safety flags validated.
- [x] Each candidate source matched to its reduction and readiness gate handoff.
- [x] Exhaustion matrix, summary, handoff, Markdown, and story generated.
- [x] Source/code readiness remains blocked.

## Generated artifacts

- `docs/reverse/generated/re307-blocker-reduction-source-exhaustion-audit.csv`
- `docs/reverse/generated/re307-blocker-reduction-source-exhaustion-audit-summary.csv`
- `docs/reverse/generated/re307-blocker-reduction-source-exhaustion-audit-handoff.csv`
- `docs/reverse/functions/re307-blocker-reduction-source-exhaustion-audit.md`

## Findings

- Candidate metadata sources: `5`
- Reduction-complete sources: `5`
- Readiness-gate-complete sources: `5`
- Remaining metadata sources: `0`
- Ready to reopen proof-domain selection: `0`
- Source patch authorized rows: `0`

- `story-tracker`: `exhausted-blocked` via `RE-297` -> `RE-298`.
- `generated-markdown`: `exhausted-blocked` via `RE-299` -> `RE-300`.
- `proof-audits`: `exhausted-blocked` via `RE-301` -> `RE-302`.
- `source-patch-gates`: `exhausted-blocked` via `RE-303` -> `RE-304`.
- `handoff-csvs`: `exhausted-blocked` via `RE-305` -> `RE-306`.

## Readiness decision

All blocker-reduction metadata sources have been reduced and gated without reopening a proof domain. Metadata work is now blocked until changed upstream mapping or new non-raw proof evidence appears.

## Follow-up ticket breakdown

- `TBD` / `changed-upstream-mapping-refresh`: if `repo-function-map.csv` or equivalent upstream mapping changes, rerun the function-priority refresh/selection chain.
  - Inputs: changed upstream mapping artifact.
  - Stop condition: no mapping delta keeps selected domain/pivot `none`.
- `TBD` / `new-non-raw-proof-evidence-intake`: if a new safe proof artifact appears, inventory and rank it before selecting a proof domain.
  - Inputs: metadata-only or source-symbolic proof evidence; no raw/binary/asset dumps.
  - Stop condition: no actionable non-raw evidence keeps source/code readiness blocked.

## Validation commands

- `python -m pytest tests/reverse/test_re307_blocker_reduction_source_exhaustion_audit.py -q`
- `python scripts/reverse/re307_blocker_reduction_source_exhaustion_audit.py --repo .`
- `python -m pytest tests/reverse -q`
