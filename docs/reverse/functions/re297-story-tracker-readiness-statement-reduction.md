# RE-297 story-tracker readiness statement reduction

## Progress tracker

- [x] RE-296 candidate-selection handoff validated.
- [x] Story tracker readiness/blocker lines inventoried without raw or asset inputs.
- [x] Repeated readiness statements normalized into reusable blocker classes.
- [x] Domain selection and source patch readiness kept blocked.

## Summary

- Story files scanned: `308`
- Evidence lines reduced: `836`
- Normalized classes: `7`
- Metadata-ready classes: `7`
- Domain-selection-ready classes: `0`
- Raw/asset sources admitted: `0`

## Normalized blocker taxonomy

### no-production-source-authorization

- Evidence count: `243`
- Story count: `201`
- First story: `docs/stories/RE-051-audio-effects-terminal-blocker.md`
- Description: Statements that deny production source or marker changes.
- Domain selection ready: `no`
- Source patch authorized: `no`

### generic-blocker-reference

- Evidence count: `197`
- Story count: `136`
- First story: `docs/stories/RE-015-saveleveldata-active-item-serialization.md`
- Description: Other blocker mentions in story tracker prose or validation command text.
- Domain selection ready: `no`
- Source patch authorized: `no`

### source-or-code-readiness-blocked

- Evidence count: `187`
- Story count: `186`
- First story: `docs/stories/RE-031-limited-restoreleveldata-reconstruction-scope.md`
- Description: Rows that explicitly keep production source, marker, or code-change readiness blocked.
- Domain selection ready: `no`
- Source patch authorized: `no`

### blocked-readiness-status

- Evidence count: `169`
- Story count: `103`
- First story: `docs/stories/RE-027-restoreleveldata-readiness-refresh.md`
- Description: Status and readiness labels that encode a blocked or terminal-blocked state.
- Domain selection ready: `no`
- Source patch authorized: `no`

### domain-selection-still-blocked

- Evidence count: `27`
- Story count: `14`
- First story: `docs/stories/RE-044-post-restoreleveldata-domain-reprioritization.md`
- Description: Statements that keep domain or pivot selection unavailable.
- Domain selection ready: `no`
- Source patch authorized: `no`

### stop-condition-before-source-or-domain-work

- Evidence count: `10`
- Story count: `7`
- First story: `docs/stories/RE-169-module-spec-psxpc-n-next-cluster-selection.md`
- Description: Stop conditions that must be satisfied before source or proof-domain work resumes.
- Domain selection ready: `no`
- Source patch authorized: `no`

### metadata-work-readiness-only

- Evidence count: `3`
- Story count: `3`
- First story: `docs/stories/RE-294-evidence-source-gap-ranking.md`
- Description: Statements where only metadata work is ready while proof/source work remains blocked.
- Domain selection ready: `no`
- Source patch authorized: `no`

## Readiness

- Metadata work readiness: `ready`
- Code/source readiness: `blocked`
- Next ticket: `RE-298`
- Next topic: `story-tracker-blocker-taxonomy-readiness-gate`
- Selected domain: `none`
- Selected pivot: `none`
- Stop condition: `run taxonomy readiness gate before reopening proof-domain selection`

No production source or marker change is authorized by this reduction.
