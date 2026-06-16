# RE-298 — story-tracker blocker taxonomy readiness gate

Status: Done

## Goal

Gate the normalized story-tracker blocker taxonomy and decide whether it can safely reopen proof-domain selection or must be corroborated by another metadata source.

## Progress tracker

- [x] RE-297 taxonomy handoff validated.
- [x] Evidence CSV confirmed metadata-only and fingerprint-based.
- [x] All taxonomy classes evaluated for proof-domain reopen readiness.
- [x] Proof-domain selection kept blocked.
- [x] Generated-Markdown blocker reduction emitted as next safe metadata step.

## Artifacts

- Gate CSV: `docs/reverse/generated/re298-story-tracker-blocker-taxonomy-readiness-gate.csv`
- Summary CSV: `docs/reverse/generated/re298-story-tracker-blocker-taxonomy-readiness-gate-summary.csv`
- Handoff CSV: `docs/reverse/generated/re298-story-tracker-blocker-taxonomy-readiness-gate-handoff.csv`
- Markdown: `docs/reverse/functions/re298-story-tracker-blocker-taxonomy-readiness-gate.md`

## Findings

- Taxonomy classes gated: `7`
- Ready to reopen proof-domain selection: `0`
- Classes needing more metadata: `7`
- Raw/asset sources admitted: `0`

The story-tracker taxonomy is still too broad and tracker-local to select a proof domain. Generated Markdown blockers are the next safe metadata surface to reduce before domain selection can reopen.

## Follow-up ticket breakdown

### RE-299 — generated-markdown-blocker-taxonomy-reduction

- Goal: normalize generated reverse-function Markdown blockers and compare them with the story-tracker taxonomy.
- Inputs: `docs/reverse/generated/re298-story-tracker-blocker-taxonomy-readiness-gate.csv`, `docs/reverse/generated/re296-blocker-reduction-candidate-selection.csv`, generated Markdown under `docs/reverse/functions/`.
- Deliverables: generated-Markdown blocker taxonomy CSV, summary/handoff CSV, story file with progress tracker.
- Validation: targeted pytest, reverse suite, metadata-only forbidden-fragment guard, asset staging guard.
- Stop condition: do not reopen proof-domain selection until generated-Markdown blockers are normalized and gated.

## Readiness

- Metadata work readiness: `ready`
- Code/source readiness: `blocked`
- Selected domain: `none`
- Selected pivot: `none`
- Stop condition: `reduce generated-markdown blockers before proof-domain selection can reopen`

No production source or marker change is authorized by this story.
