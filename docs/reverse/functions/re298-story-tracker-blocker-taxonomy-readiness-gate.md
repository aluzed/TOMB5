# RE-298 story-tracker blocker taxonomy readiness gate

## Progress tracker

- [x] RE-297 taxonomy handoff validated.
- [x] RE-297 evidence schema checked for metadata-only fingerprints.
- [x] Story-tracker taxonomy classes gated for proof-domain readiness.
- [x] Next metadata source selected without reopening source or domain work.

## Gate decision

- Taxonomy classes gated: `7`
- Ready to reopen proof-domain selection: `0`
- Classes needing more metadata: `7`
- Next metadata source: `generated-markdown`
- Next topic: `generated-markdown-blocker-taxonomy-reduction`

The story-tracker taxonomy is useful metadata, but it is not enough by itself to justify a safe proof-domain selection. The next safe step is to reduce generated Markdown blockers for corroboration.

## Gate rows

### no-production-source-authorization

- Evidence count: `243`
- Story count: `201`
- Decision: `needs-more-metadata`
- Reason: authorization denials confirm source work is blocked rather than reopenable.
- Ready to reopen domain: `no`

### generic-blocker-reference

- Evidence count: `197`
- Story count: `136`
- Decision: `needs-more-metadata`
- Reason: generic story references are not specific enough to justify a proof-domain selection.
- Ready to reopen domain: `no`

### source-or-code-readiness-blocked

- Evidence count: `187`
- Story count: `186`
- Decision: `needs-more-metadata`
- Reason: source/code readiness blockers still dominate the tracker.
- Ready to reopen domain: `no`

### blocked-readiness-status

- Evidence count: `169`
- Story count: `103`
- Decision: `needs-more-metadata`
- Reason: blocked status labels need corroboration from another metadata source.
- Ready to reopen domain: `no`

### domain-selection-still-blocked

- Evidence count: `27`
- Story count: `14`
- Decision: `needs-more-metadata`
- Reason: domain-selection rows explicitly remain blocked.
- Ready to reopen domain: `no`

### stop-condition-before-source-or-domain-work

- Evidence count: `10`
- Story count: `7`
- Decision: `needs-more-metadata`
- Reason: stop conditions require another metadata gate before proof-domain work.
- Ready to reopen domain: `no`

### metadata-work-readiness-only

- Evidence count: `3`
- Story count: `3`
- Decision: `needs-more-metadata`
- Reason: metadata readiness alone is insufficient to select a proof domain.
- Ready to reopen domain: `no`

## Readiness

- Metadata work readiness: `ready`
- Code/source readiness: `blocked`
- Next ticket: `RE-299`
- Next topic: `generated-markdown-blocker-taxonomy-reduction`
- Selected domain: `none`
- Selected pivot: `none`
- Stop condition: `reduce generated-markdown blockers before proof-domain selection can reopen`

No production source or marker change is authorized by this gate.
