# RE-299 generated-Markdown blocker taxonomy reduction

## Progress tracker

- [x] RE-298 readiness-gate handoff validated.
- [x] Deferred generated-Markdown candidate from RE-296 validated.
- [x] Generated Markdown files scanned with RE-299+ outputs excluded for stable reruns.
- [x] Evidence reduced to hashed metadata rows without storing source line text.

## Findings

- Generated Markdown files scanned: `88`
- Evidence lines reduced: `1402`
- Normalized classes: `7`
- Domain-selection-ready classes: `0`

## Story-tracker correlation

Generated Markdown blockers overlap the story-tracker taxonomy, but this reduction still does not reopen proof-domain selection. It prepares the generated-Markdown taxonomy for a dedicated readiness gate.

## Taxonomy rows

### generic-blocker-reference

- Evidence count: `811`
- Markdown files: `86`
- Story-tracker correlated: `yes`
- Domain selection ready: `no`

### domain-selection-still-blocked

- Evidence count: `233`
- Markdown files: `56`
- Story-tracker correlated: `yes`
- Domain selection ready: `no`

### proof-or-marker-change-blocked

- Evidence count: `140`
- Markdown files: `66`
- Story-tracker correlated: `partial`
- Domain selection ready: `no`

### source-or-code-readiness-blocked

- Evidence count: `126`
- Markdown files: `44`
- Story-tracker correlated: `yes`
- Domain selection ready: `no`

### no-production-source-authorization

- Evidence count: `68`
- Markdown files: `66`
- Story-tracker correlated: `yes`
- Domain selection ready: `no`

### metadata-work-readiness-only

- Evidence count: `19`
- Markdown files: `16`
- Story-tracker correlated: `yes`
- Domain selection ready: `no`

### stop-condition-before-source-or-domain-work

- Evidence count: `5`
- Markdown files: `5`
- Story-tracker correlated: `yes`
- Domain selection ready: `no`

## Readiness

- Metadata work readiness: `ready`
- Code/source readiness: `blocked`
- Next ticket: `RE-300`
- Next topic: `generated-markdown-blocker-taxonomy-readiness-gate`
- Selected domain: `none`
- Selected pivot: `none`
- Stop condition: `gate generated-markdown taxonomy before proof-domain selection can reopen`

No production source or marker change is authorized by this reduction.
