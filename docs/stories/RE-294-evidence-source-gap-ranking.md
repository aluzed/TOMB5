# RE-294 — evidence source gap ranking

Status: Done

## Goal

Rank the safe evidence sources inventoried by RE-293 by their ability to reduce current blocker classes without using raw/binary/asset material.

## Progress tracker

- [x] RE-293 source inventory handoff validated.
- [x] Source classes scored for blocker-reduction potential.
- [x] Testable-now metadata sources separated from supporting-only sources.
- [x] Proof-domain selection kept blocked until blockers are extracted.
- [x] Next metadata-only extraction ticket emitted.

## Artifacts

- Ranking CSV: `docs/reverse/generated/re294-evidence-source-gap-ranking.csv`
- Summary CSV: `docs/reverse/generated/re294-evidence-source-gap-ranking-summary.csv`
- Handoff CSV: `docs/reverse/generated/re294-evidence-source-gap-ranking-handoff.csv`
- Markdown: `docs/reverse/functions/re294-evidence-source-gap-ranking.md`

## Findings

- Ranked sources: `15`
- Testable now: `5`
- Raw/asset sources admitted: `0`
- Top source: `generated-markdown`

Top testable-now sources:

- `generated-markdown` — `human-summary-blockers` — score `100`
- `story-tracker` — `progression-blockers` — score `96`
- `handoff-csvs` — `handoff-readiness` — score `92`
- `source-patch-gates` — `patch-gate-denials` — score `88`
- `proof-audits` — `proof-first-gaps` — score `84`

The ranking makes metadata work ready, but it still does not authorize production source or marker changes.

## Next objective

- Next ticket: `RE-295`
- Topic: `metadata-blocker-extraction`
- Goal: extract machine-readable blocker classes from the top-ranked metadata sources and determine whether any blocker can be reduced without new external evidence.

## Readiness

- Metadata work readiness: `ready`
- Code/source readiness: `blocked`
- Selected domain: `none`
- Selected pivot: `none`
- Stop condition: `extract machine-readable blockers from top-ranked metadata sources before selecting a proof domain`

No production source or marker change is authorized by this story.
