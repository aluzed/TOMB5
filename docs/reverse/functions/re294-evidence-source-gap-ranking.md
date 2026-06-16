# RE-294 evidence source gap ranking

## Progress tracker

- [x] RE-293 source inventory handoff validated.
- [x] Safe evidence sources ranked by blocker-reduction potential.
- [x] Raw/binary/asset source classes excluded from ranking.
- [x] Metadata-ready next ticket emitted without selecting a fake proof domain.

## Summary

- Ranked sources: `15`
- Testable now: `5`
- Testable with existing metadata: `2`
- Supporting-only sources: `6`
- Blocked/no-candidate baselines: `2`
- Raw/asset sources admitted: `0`
- Top source: `generated-markdown`

## Ranked evidence sources

### 1. generated-markdown

- Score: `100`
- Count: `94`
- Safety: `metadata-only`
- Actionability: `testable-now`
- Blocker class: `human-summary-blockers`
- Recommended use: extract explicit blocker statements into a machine-readable matrix.
- Next step: parse RE markdown sections for readiness and stop-condition language.

### 2. story-tracker

- Score: `96`
- Count: `304`
- Safety: `metadata-only`
- Actionability: `testable-now`
- Blocker class: `progression-blockers`
- Recommended use: normalize story progress trackers and blocked follow-up items.
- Next step: extract open blocker classes and dependency phrases from story files.

### 3. handoff-csvs

- Score: `92`
- Count: `38`
- Safety: `metadata-only`
- Actionability: `testable-now`
- Blocker class: `handoff-readiness`
- Recommended use: merge next_topic and readiness outcomes across closed chains.
- Next step: rank repeated handoff blockers by frequency and recency.

### 4. source-patch-gates

- Score: `88`
- Count: `16`
- Safety: `metadata-only`
- Actionability: `testable-now`
- Blocker class: `patch-gate-denials`
- Recommended use: identify why source or marker patches were denied.
- Next step: cluster denial reasons by evidence type needed.

### 5. proof-audits

- Score: `84`
- Count: `34`
- Safety: `metadata-only`
- Actionability: `testable-now`
- Blocker class: `proof-first-gaps`
- Recommended use: recover proof-first blocker wording from prior domain openings.
- Next step: extract proof gap classes from audit CSVs.

### 6. equivalence-gates

- Score: `76`
- Count: `7`
- Safety: `metadata-only`
- Actionability: `testable-with-existing-metadata`
- Blocker class: `equivalence-readiness`
- Recommended use: rank equivalence gates by what symbolic evidence is missing.
- Next step: compare gate blockers against available state contracts and taxonomies.

### 7. state-contracts

- Score: `72`
- Count: `7`
- Safety: `metadata-only`
- Actionability: `testable-with-existing-metadata`
- Blocker class: `state-contract-coverage`
- Recommended use: map contracts to equivalence gates that still need narrowing.
- Next step: join contract names to gate topics where possible.

### 8. argument-taxonomies

- Score: `68`
- Count: `22`
- Safety: `metadata-only`
- Actionability: `supporting-only`
- Blocker class: `argument-state-coverage`
- Recommended use: support blocker extraction with symbolic argument group names.
- Next step: link taxonomy topics to proof audit domains.

### 9. callsite-maps

- Score: `64`
- Count: `13`
- Safety: `metadata-only`
- Actionability: `supporting-only`
- Blocker class: `callsite-coverage`
- Recommended use: support source-context claims for already mapped callsite chains.
- Next step: compare map topics with blocked gate topics.

### 10. selection-gates

- Score: `60`
- Count: `15`
- Safety: `metadata-only`
- Actionability: `supporting-only`
- Blocker class: `selection-history`
- Recommended use: trace how prior domain selections were exhausted.
- Next step: use only after blocker extraction names a plausible domain.

### 11. comparison-gates

- Score: `56`
- Count: `2`
- Safety: `metadata-only`
- Actionability: `supporting-only`
- Blocker class: `comparison-readiness`
- Recommended use: preserve earlier comparison gate blockers.
- Next step: fold into unified gate blocker matrix.

### 12. caller-maps

- Score: `52`
- Count: `2`
- Safety: `metadata-only`
- Actionability: `supporting-only`
- Blocker class: `legacy-caller-context`
- Recommended use: normalize older caller maps with newer callsite records.
- Next step: deduplicate with callsite maps before domain selection.

### 13. source-corpus

- Score: `40`
- Count: `482`
- Safety: `source-symbolic`
- Actionability: `supporting-only`
- Blocker class: `source-symbol-context`
- Recommended use: provide symbolic names and source-level context only.
- Next step: do not use alone to reopen binary equivalence or patch readiness.

### 14. repo-function-map

- Score: `24`
- Count: `1250`
- Safety: `metadata-only`
- Actionability: `blocked-no-candidate`
- Blocker class: `unchanged-upstream-map`
- Recommended use: baseline function/domain map after unchanged refresh.
- Next step: wait for changed upstream mapping before reselection.

### 15. function-priority

- Score: `20`
- Count: `348`
- Safety: `metadata-only`
- Actionability: `blocked-no-candidate`
- Blocker class: `exhausted-priority-backlog`
- Recommended use: document exhausted ranked backlog.
- Next step: do not select a fake priority row.

## Readiness

- Metadata work readiness: `ready`
- Code/source readiness: `blocked`
- Next ticket: `RE-295`
- Next topic: `metadata-blocker-extraction`
- Selected domain: `none`
- Selected pivot: `none`
- Stop condition: `extract machine-readable blockers from top-ranked metadata sources before selecting a proof domain`

No production source or marker change is authorized by this ranking.
