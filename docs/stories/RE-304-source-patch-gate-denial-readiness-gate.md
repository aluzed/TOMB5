# RE-304 — source-patch gate denial readiness gate

Status: Done

## Goal

Gate the source-patch denial taxonomy and decide whether proof-domain selection can reopen.

## Progress tracker

- [x] RE-303 source-patch denial taxonomy handoff validated.
- [x] RE-303 evidence CSV confirmed metadata-only and fingerprint-based.
- [x] All source-patch denial classes evaluated for proof-domain reopen readiness.
- [x] Proof-domain selection kept blocked.
- [x] Handoff stop-condition reduction emitted as next safe metadata step.

## Artifacts

- Gate CSV: `docs/reverse/generated/re304-source-patch-gate-denial-readiness-gate.csv`
- Summary CSV: `docs/reverse/generated/re304-source-patch-gate-denial-readiness-gate-summary.csv`
- Handoff CSV: `docs/reverse/generated/re304-source-patch-gate-denial-readiness-gate-handoff.csv`
- Markdown: `docs/reverse/functions/re304-source-patch-gate-denial-readiness-gate.md`

## Findings

- Source-patch denial classes gated: `5`
- Ready to reopen proof-domain selection: `0`
- Classes needing more metadata: `5`
- Source patch authorized rows: `0`
- Raw/asset sources admitted: `0`

The source-patch denial taxonomy is metadata-only and confirms blocked patch paths, not proof-domain readiness or source authorization.

## Follow-up ticket breakdown

### RE-305 — handoff-stop-condition-reduction

- Goal: normalize handoff stop conditions before any proof-domain selection can reopen.
- Inputs: `docs/reverse/generated/re304-source-patch-gate-denial-readiness-gate.csv`, `docs/reverse/generated/re296-blocker-reduction-candidate-selection.csv`, upstream handoff CSV artifacts.
- Deliverables: handoff stop-condition taxonomy CSV, metadata-only evidence CSV, summary/handoff CSV, story file with progress tracker.
- Validation: targeted pytest, reverse suite, metadata-only forbidden-fragment guard, asset staging guard.
- Stop condition: do not reopen proof-domain selection until handoff stop conditions are reduced and gated.

## Readiness

- Metadata work readiness: `ready`
- Code/source readiness: `blocked`
- Selected domain: `none`
- Selected pivot: `none`
- Stop condition: `reduce handoff stop conditions before proof-domain selection can reopen`

No production source or marker change is authorized by this story.
