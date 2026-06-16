# RE-297 — story-tracker readiness statement reduction

Status: Done

## Goal

Normalize repeated story-tracker readiness and blocker statements into reusable metadata classes before reopening proof-domain selection.

## Progress tracker

- [x] RE-296 candidate-selection handoff validated.
- [x] Upstream story files scanned with RE-297+ outputs excluded for stable reruns.
- [x] Evidence lines reduced to hashed metadata rows without storing source line text.
- [x] Normalized taxonomy and follow-up readiness gate emitted.
- [x] Code/source readiness remains blocked.

## Artifacts

- Taxonomy CSV: `docs/reverse/generated/re297-story-tracker-readiness-statement-reduction.csv`
- Evidence CSV: `docs/reverse/generated/re297-story-tracker-readiness-statement-reduction-evidence.csv`
- Summary CSV: `docs/reverse/generated/re297-story-tracker-readiness-statement-reduction-summary.csv`
- Handoff CSV: `docs/reverse/generated/re297-story-tracker-readiness-statement-reduction-handoff.csv`
- Markdown: `docs/reverse/functions/re297-story-tracker-readiness-statement-reduction.md`

## Findings

- Story files scanned: `308`
- Evidence lines reduced: `836`
- Normalized classes: `7`
- Metadata-ready classes: `7`
- Domain-selection-ready classes: `0`
- Raw/asset sources admitted: `0`

The reduction converts repeated story readiness language into reusable metadata classes. It still does not select a proof domain, pivot, source patch, or marker patch.

## Follow-up ticket breakdown

### RE-298 — story-tracker-blocker-taxonomy-readiness-gate

- Goal: decide whether the normalized story-tracker blocker taxonomy is sufficient to reopen safe proof-domain selection or whether another metadata source must be reduced first.
- Inputs: `docs/reverse/generated/re297-story-tracker-readiness-statement-reduction.csv`, `docs/reverse/generated/re297-story-tracker-readiness-statement-reduction-evidence.csv`, `docs/reverse/generated/re296-blocker-reduction-candidate-selection.csv`.
- Deliverables: readiness-gate CSV, summary/handoff CSV, story file with progress tracker.
- Validation: targeted pytest, reverse suite, metadata-only forbidden-fragment guard, asset staging guard.
- Stop condition: keep proof-domain selection blocked unless the gate can justify a non-raw, metadata-only next selection step.

## Readiness

- Metadata work readiness: `ready`
- Code/source readiness: `blocked`
- Selected domain: `none`
- Selected pivot: `none`
- Stop condition: `run taxonomy readiness gate before reopening proof-domain selection`

No production source or marker change is authorized by this story.
