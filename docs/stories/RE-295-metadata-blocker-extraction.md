# RE-295 — metadata blocker extraction

Status: Done

## Goal

Extract machine-readable blocker classes from the top-ranked metadata sources produced by RE-294 without selecting a proof domain or using raw/binary/asset material.

## Progress tracker

- [x] RE-294 ranking handoff validated.
- [x] Top testable-now metadata sources consumed.
- [x] Evidence counts and dominant blockers extracted.
- [x] Domain selection readiness kept at zero.
- [x] Next blocker-reduction candidate ticket emitted.

## Artifacts

- Extraction CSV: `docs/reverse/generated/re295-metadata-blocker-extraction.csv`
- Summary CSV: `docs/reverse/generated/re295-metadata-blocker-extraction-summary.csv`
- Handoff CSV: `docs/reverse/generated/re295-metadata-blocker-extraction-handoff.csv`
- Markdown: `docs/reverse/functions/re295-metadata-blocker-extraction.md`

## Findings

- Sources extracted: `5`
- Metadata reduction ready rows: `5`
- Domain selection ready rows: `0`
- Raw/asset sources admitted: `0`
- Top source: `story-tracker`

The extraction converts existing metadata blockers into a ranking surface. It does not make any production source or marker patch ready.

## Next objective

- Next ticket: `RE-296`
- Topic: `blocker-reduction-candidate-selection`
- Goal: choose the best metadata-only blocker-reduction candidate and define the next testable narrowing step before any proof-domain selection.

## Readiness

- Metadata work readiness: `ready`
- Code/source readiness: `blocked`
- Selected domain: `none`
- Selected pivot: `none`
- Stop condition: `select a metadata blocker-reduction candidate before reopening any proof domain`

No production source or marker change is authorized by this story.
