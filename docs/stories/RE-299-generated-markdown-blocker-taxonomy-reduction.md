# RE-299 — generated-Markdown blocker taxonomy reduction

Status: Done

## Goal

Normalize generated reverse-function Markdown blocker and readiness statements into reusable metadata classes, then hand off to a gate before proof-domain selection can reopen.

## Progress tracker

- [x] RE-298 readiness-gate handoff validated.
- [x] RE-296 generated-Markdown candidate validated as safe metadata work.
- [x] Generated Markdown evidence reduced to hashed metadata rows.
- [x] Story-tracker taxonomy correlation recorded.
- [x] Code/source readiness remains blocked.

## Artifacts

- Taxonomy CSV: `docs/reverse/generated/re299-generated-markdown-blocker-taxonomy-reduction.csv`
- Evidence CSV: `docs/reverse/generated/re299-generated-markdown-blocker-taxonomy-reduction-evidence.csv`
- Summary CSV: `docs/reverse/generated/re299-generated-markdown-blocker-taxonomy-reduction-summary.csv`
- Handoff CSV: `docs/reverse/generated/re299-generated-markdown-blocker-taxonomy-reduction-handoff.csv`
- Markdown: `docs/reverse/functions/re299-generated-markdown-blocker-taxonomy-reduction.md`

## Findings

- Generated Markdown files scanned: `88`
- Evidence lines reduced: `1402`
- Normalized classes: `7`
- Metadata-ready classes: `7`
- Domain-selection-ready classes: `0`
- Story-tracker-correlated classes: `7`
- Raw/asset sources admitted: `0`

The reduction confirms that generated Markdown carries corroborating blocker taxonomy, but it does not by itself authorize proof-domain selection, source patches, or marker patches.

## Follow-up ticket breakdown

### RE-300 — generated-markdown-blocker-taxonomy-readiness-gate

- Goal: gate the generated-Markdown taxonomy against story-tracker classes and decide whether another metadata source is required.
- Inputs: `docs/reverse/generated/re299-generated-markdown-blocker-taxonomy-reduction.csv`, `docs/reverse/generated/re299-generated-markdown-blocker-taxonomy-reduction-evidence.csv`, `docs/reverse/generated/re298-story-tracker-blocker-taxonomy-readiness-gate.csv`.
- Deliverables: readiness-gate CSV, summary/handoff CSV, story file with progress tracker.
- Validation: targeted pytest, reverse suite, metadata-only forbidden-fragment guard, asset staging guard.
- Stop condition: keep proof-domain selection blocked unless the gate can justify a non-raw metadata selection step.

## Readiness

- Metadata work readiness: `ready`
- Code/source readiness: `blocked`
- Selected domain: `none`
- Selected pivot: `none`
- Stop condition: `gate generated-markdown taxonomy before proof-domain selection can reopen`

No production source or marker change is authorized by this story.
