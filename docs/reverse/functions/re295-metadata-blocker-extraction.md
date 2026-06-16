# RE-295 metadata blocker extraction

## Progress tracker

- [x] RE-294 ranking handoff validated.
- [x] Top testable metadata sources consumed.
- [x] Blocker evidence counts and dominant blockers extracted.
- [x] Domain selection kept blocked until a reduction candidate is selected.

## Summary

- Sources extracted: `5`
- Extraction rows: `5`
- Metadata reduction ready rows: `5`
- Domain selection ready rows: `0`
- Raw/asset sources admitted: `0`
- Top source: `story-tracker`

## Extracted blocker sources

### story-tracker

- Blocker class: `progression-blockers`
- Evidence count: `683`
- Unique blocker count: `149`
- Dominant blocker: `blocked-readiness-statements`
- Metadata reduction ready: `yes`
- Domain selection ready: `no`
- Next step: extract blocked progress tracker and next-objective dependencies from stories.

### generated-markdown

- Blocker class: `human-summary-blockers`
- Evidence count: `472`
- Unique blocker count: `250`
- Dominant blocker: `blocked-readiness-statements`
- Metadata reduction ready: `yes`
- Domain selection ready: `no`
- Next step: extract normalized blocker phrases from reverse function Markdown.

### proof-audits

- Blocker class: `proof-first-gaps`
- Evidence count: `384`
- Unique blocker count: `43`
- Dominant blocker: `missing-maths-render-source-contract-and-non-raw-equivalence-proof`
- Metadata reduction ready: `yes`
- Domain selection ready: `no`
- Next step: cluster proof-first blockers by domain and missing evidence class.

### source-patch-gates

- Blocker class: `patch-gate-denials`
- Evidence count: `58`
- Unique blocker count: `11`
- Dominant blocker: `missing-non-raw-binary-equivalence-proof`
- Metadata reduction ready: `yes`
- Domain selection ready: `no`
- Next step: cluster patch denial reasons by missing proof class.

### handoff-csvs

- Blocker class: `handoff-readiness`
- Evidence count: `40`
- Unique blocker count: `40`
- Dominant blocker: `debris/object-breakage has source stubs and no non-raw binary equivalence proof for safe patching`
- Metadata reduction ready: `yes`
- Domain selection ready: `no`
- Next step: consolidate repeated handoff blockers and terminal stop conditions.

## Readiness

- Metadata work readiness: `ready`
- Code/source readiness: `blocked`
- Next ticket: `RE-296`
- Next topic: `blocker-reduction-candidate-selection`
- Selected domain: `none`
- Selected pivot: `none`
- Stop condition: `select a metadata blocker-reduction candidate before reopening any proof domain`

No production source or marker change is authorized by this extraction.
