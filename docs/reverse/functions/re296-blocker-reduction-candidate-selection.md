# RE-296 blocker reduction candidate selection

## Progress tracker

- [x] RE-295 blocker extraction handoff validated.
- [x] Metadata-only candidates scored without raw or asset inputs.
- [x] One blocker-reduction candidate selected while proof-domain selection remains blocked.
- [x] Source and marker patch readiness kept blocked.

## Summary

- Candidate rows: `5`
- Metadata-ready candidates: `5`
- Domain-selection-ready candidates: `0`
- Raw/asset sources admitted: `0`

## Selected candidate

- Candidate ID: `story-tracker-blocked-readiness-statements`
- Source: `story-tracker`
- Blocker class: `progression-blockers`
- Dominant blocker: `blocked-readiness-statements`
- Evidence count: `683`
- Unique blocker count: `149`
- Selection score: `1565`
- Reduction action: normalize story readiness blocker statements before any proof-domain selection.

## Candidate ranking

### story-tracker-blocked-readiness-statements

- Status: `selected`
- Score: `1565`
- Metadata candidate ready: `yes`
- Domain selection ready: `no`
- Next topic: `story-tracker-readiness-statement-reduction`

### generated-markdown-blocked-readiness-statements

- Status: `candidate`
- Score: `1234`
- Metadata candidate ready: `yes`
- Domain selection ready: `no`
- Next topic: `generated-markdown-blocker-taxonomy-reduction`

### proof-audits-missing-maths-render-source-contract-and-non-raw-equivalence-proof

- Status: `candidate`
- Score: `841`
- Metadata candidate ready: `yes`
- Domain selection ready: `no`
- Next topic: `proof-audit-blocker-taxonomy-reduction`

### source-patch-gates-missing-non-raw-binary-equivalence-proof

- Status: `candidate`
- Score: `147`
- Metadata candidate ready: `yes`
- Domain selection ready: `no`
- Next topic: `source-patch-gate-denial-reduction`

### handoff-csvs-debris-object-breakage-has-source-stubs-and-no-non-raw-binary-equivalence-proof-for-safe-patching

- Status: `candidate`
- Score: `130`
- Metadata candidate ready: `yes`
- Domain selection ready: `no`
- Next topic: `handoff-stop-condition-reduction`

## Readiness

- Metadata work readiness: `ready`
- Code/source readiness: `blocked`
- Next ticket: `RE-297`
- Next topic: `story-tracker-readiness-statement-reduction`
- Selected domain: `none`
- Selected pivot: `none`
- Stop condition: `reduce selected metadata blocker candidate before reopening any proof domain`

No production source or marker change is authorized by this selection.
