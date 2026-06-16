# RE-301 — proof-audit blocker taxonomy reduction

Status: Done

## Goal

Normalize proof-audit blocker rows into reusable metadata classes without reopening proof-domain selection.

## Progress tracker

- [x] RE-300 proof-audit handoff validated.
- [x] RE-296 proof-audits candidate validated.
- [x] Upstream proof CSV rows reduced to hashed metadata evidence.
- [x] Normalized proof-audit blocker taxonomy emitted.
- [x] Proof-domain selection kept blocked until a readiness gate runs.

## Artifacts

- Taxonomy CSV: `docs/reverse/generated/re301-proof-audit-blocker-taxonomy-reduction.csv`
- Evidence CSV: `docs/reverse/generated/re301-proof-audit-blocker-taxonomy-reduction-evidence.csv`
- Summary CSV: `docs/reverse/generated/re301-proof-audit-blocker-taxonomy-reduction-summary.csv`
- Handoff CSV: `docs/reverse/generated/re301-proof-audit-blocker-taxonomy-reduction-handoff.csv`
- Markdown: `docs/reverse/functions/re301-proof-audit-blocker-taxonomy-reduction.md`

## Findings

- Proof CSV files scanned: `34`
- Evidence rows reduced: `384`
- Normalized classes: `8`
- Metadata-ready classes: `8`
- Domain-selection-ready classes: `0`
- Raw/asset sources admitted: `0`

The reduction consolidates proof-audit blockers, but the taxonomy remains a missing-evidence inventory rather than proof-domain readiness.

## Follow-up ticket breakdown

### RE-302 — proof-audit-blocker-taxonomy-readiness-gate

- Goal: gate the proof-audit blocker taxonomy and decide whether any non-raw metadata can reopen proof-domain selection.
- Inputs: `docs/reverse/generated/re301-proof-audit-blocker-taxonomy-reduction.csv`, `docs/reverse/generated/re301-proof-audit-blocker-taxonomy-reduction-evidence.csv`, `docs/reverse/generated/re301-proof-audit-blocker-taxonomy-reduction-handoff.csv`.
- Deliverables: readiness-gate CSV, summary/handoff CSV, story file with progress tracker.
- Validation: targeted pytest, reverse suite, metadata-only forbidden-fragment guard, asset staging guard.
- Stop condition: keep proof-domain selection blocked unless a non-raw proof-domain selection step is justified.

## Readiness

- Metadata work readiness: `ready`
- Code/source readiness: `blocked`
- Selected domain: `none`
- Selected pivot: `none`
- Stop condition: `gate proof-audit taxonomy before proof-domain selection can reopen`

No production source or marker change is authorized by this story.
