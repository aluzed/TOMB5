# RE-296 — blocker reduction candidate selection

Status: Done

## Goal

Select the safest metadata-only blocker-reduction candidate from RE-295 before reopening any proof domain or considering source and marker changes.

## Progress tracker

- [x] RE-295 blocker extraction handoff validated.
- [x] Candidate rows scored from metadata-only extraction rows.
- [x] Selected candidate keeps domain and pivot scope at none.
- [x] Follow-up blocker-reduction ticket emitted.
- [x] Code/source readiness remains blocked.

## Artifacts

- Candidate CSV: `docs/reverse/generated/re296-blocker-reduction-candidate-selection.csv`
- Summary CSV: `docs/reverse/generated/re296-blocker-reduction-candidate-selection-summary.csv`
- Handoff CSV: `docs/reverse/generated/re296-blocker-reduction-candidate-selection-handoff.csv`
- Markdown: `docs/reverse/functions/re296-blocker-reduction-candidate-selection.md`

## Findings

- Candidate rows: `5`
- Selected candidate: `story-tracker-blocked-readiness-statements`
- Selected source: `story-tracker`
- Selected blocker: `blocked-readiness-statements`
- Metadata-ready candidates: `5`
- Domain-selection-ready candidates: `0`
- Raw/asset sources admitted: `0`

The selected work is intentionally still metadata-only: it narrows repeated readiness language in story trackers, but it does not make domain selection, pivot selection, or source patching ready.

## Follow-up ticket breakdown

### RE-297 — story-tracker-readiness-statement-reduction

- Goal: normalize story readiness blocker statements before any proof-domain selection.
- Inputs: `docs/reverse/generated/re296-blocker-reduction-candidate-selection.csv`, `docs/reverse/generated/re295-metadata-blocker-extraction.csv`, story tracker Markdown under `docs/stories/`.
- Deliverables: normalized blocker taxonomy CSV, summary/handoff CSV, story file with progress tracker.
- Validation: targeted pytest, reverse suite, metadata-only forbidden-fragment guard, asset staging guard.
- Stop condition: do not reopen proof-domain selection until the selected metadata blocker has been reduced into reusable classes.

## Readiness

- Metadata work readiness: `ready`
- Code/source readiness: `blocked`
- Selected domain: `none`
- Selected pivot: `none`
- Stop condition: `reduce selected metadata blocker candidate before reopening any proof domain`

No production source or marker change is authorized by this story.
