# RE-300 — generated-Markdown blocker taxonomy readiness gate

Status: Done

## Goal

Gate the generated-Markdown blocker taxonomy against story-tracker correlation and decide whether proof-domain selection can reopen.

## Progress tracker

- [x] RE-299 generated-Markdown taxonomy handoff validated.
- [x] RE-299 evidence CSV confirmed metadata-only and fingerprint-based.
- [x] All generated-Markdown taxonomy classes evaluated for proof-domain reopen readiness.
- [x] Proof-domain selection kept blocked.
- [x] Proof-audit blocker reduction emitted as next safe metadata step.

## Artifacts

- Gate CSV: `docs/reverse/generated/re300-generated-markdown-blocker-taxonomy-readiness-gate.csv`
- Summary CSV: `docs/reverse/generated/re300-generated-markdown-blocker-taxonomy-readiness-gate-summary.csv`
- Handoff CSV: `docs/reverse/generated/re300-generated-markdown-blocker-taxonomy-readiness-gate-handoff.csv`
- Markdown: `docs/reverse/functions/re300-generated-markdown-blocker-taxonomy-readiness-gate.md`

## Findings

- Generated-Markdown classes gated: `7`
- Story-tracker-correlated classes: `7`
- Ready to reopen proof-domain selection: `0`
- Classes needing more metadata: `7`
- Raw/asset sources admitted: `0`

The generated-Markdown taxonomy corroborates blockers already seen in story tracking, but the gate still lacks proof-audit corroboration. Proof-domain selection remains blocked.

## Follow-up ticket breakdown

### RE-301 — proof-audit-blocker-taxonomy-reduction

- Goal: normalize proof-audit blocker rows into reusable missing-evidence classes.
- Inputs: `docs/reverse/generated/re300-generated-markdown-blocker-taxonomy-readiness-gate.csv`, `docs/reverse/generated/re296-blocker-reduction-candidate-selection.csv`, proof-audit generated CSV/Markdown artifacts.
- Deliverables: proof-audit blocker taxonomy CSV, summary/handoff CSV, story file with progress tracker.
- Validation: targeted pytest, reverse suite, metadata-only forbidden-fragment guard, asset staging guard.
- Stop condition: do not reopen proof-domain selection until proof-audit blockers are normalized and gated.

## Readiness

- Metadata work readiness: `ready`
- Code/source readiness: `blocked`
- Selected domain: `none`
- Selected pivot: `none`
- Stop condition: `reduce proof-audit blockers before proof-domain selection can reopen`

No production source or marker change is authorized by this story.
