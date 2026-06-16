# RE-293 evidence source inventory

## Progress tracker

- [x] RE-292 blocked handoff validated.
- [x] Safe metadata/source-symbolic evidence sources enumerated.
- [x] Unsafe binary/asset source classes excluded from the inventory.
- [x] Inventory summary and blocked handoff emitted.

## Summary

- Evidence sources inventoried: `15`
- Metadata-only sources: `14`
- Source-symbolic sources: `1`
- Raw/asset sources admitted: `0`
- Candidate evidence gaps: `14`

## Evidence source inventory

### argument-taxonomies

- Type: `generated-csv`
- Pattern: `docs/reverse/generated/*argument*taxonomy*.csv`
- Count: `22`
- Safety: `metadata-only`
- Status: `available`
- Use: symbolic argument and state grouping.
- Gap: needs cross-ticket gap ranking before reuse.

### caller-maps

- Type: `generated-csv`
- Pattern: `docs/reverse/generated/*caller-map*.csv`
- Count: `2`
- Safety: `metadata-only`
- Status: `available`
- Use: legacy caller mapping context.
- Gap: needs normalization with newer callsite maps.

### callsite-maps

- Type: `generated-csv`
- Pattern: `docs/reverse/generated/*callsite*.csv`
- Count: `13`
- Safety: `metadata-only`
- Status: `available`
- Use: source-backed caller/callee context.
- Gap: needs stale-domain coverage comparison.

### comparison-gates

- Type: `generated-csv`
- Pattern: `docs/reverse/generated/*comparison-gate*.csv`
- Count: `2`
- Safety: `metadata-only`
- Status: `available`
- Use: blocked comparison readiness decisions.
- Gap: needs source-gap ranking.

### equivalence-gates

- Type: `generated-csv`
- Pattern: `docs/reverse/generated/*equivalence-gate*.csv`
- Count: `7`
- Safety: `metadata-only`
- Status: `available`
- Use: blocked equivalence readiness decisions.
- Gap: needs proof-evidence gap ranking.

### function-priority

- Type: `generated-csv`
- Pattern: `docs/reverse/generated/function-priority.csv`
- Count: `348`
- Safety: `metadata-only`
- Status: `available`
- Use: closed priority backlog baseline.
- Gap: contains no remaining candidate row.

### generated-markdown

- Type: `generated-md`
- Pattern: `docs/reverse/**/*.md`
- Count: `94`
- Safety: `metadata-only`
- Status: `available`
- Use: human-readable proof summaries and blockers.
- Gap: needs machine-readable gap extraction.

### handoff-csvs

- Type: `generated-csv`
- Pattern: `docs/reverse/generated/*handoff*.csv`
- Count: `38`
- Safety: `metadata-only`
- Status: `available`
- Use: ticket-to-ticket readiness and closure state.
- Gap: needs consolidated next-input ranking.

### proof-audits

- Type: `generated-csv`
- Pattern: `docs/reverse/generated/*proof*.csv`
- Count: `34`
- Safety: `metadata-only`
- Status: `available`
- Use: proof-first domain openings and blockers.
- Gap: needs gap severity ranking.

### repo-function-map

- Type: `generated-csv`
- Pattern: `docs/reverse/generated/repo-function-map.csv`
- Count: `1250`
- Safety: `metadata-only`
- Status: `available`
- Use: authoritative function/domain mapping input.
- Gap: unchanged after RE-291 refresh.

### selection-gates

- Type: `generated-csv`
- Pattern: `docs/reverse/generated/*selection*.csv`
- Count: `15`
- Safety: `metadata-only`
- Status: `available`
- Use: previous domain and cluster selection decisions.
- Gap: needs re-run only after a new input changes.

### source-corpus

- Type: `checked-in-source`
- Pattern: `GAME|SPEC_*|TOOLS source files`
- Count: `482`
- Safety: `source-symbolic`
- Status: `available`
- Use: function names, files, and source-level control context.
- Gap: insufficient alone for binary equivalence readiness.

### source-patch-gates

- Type: `generated-csv`
- Pattern: `docs/reverse/generated/*source-patch-gate*.csv`
- Count: `16`
- Safety: `metadata-only`
- Status: `available`
- Use: source and marker patch denials.
- Gap: needs evidence source ranking before any patch gate can reopen.

### state-contracts

- Type: `generated-csv`
- Pattern: `docs/reverse/generated/*state-contract*.csv`
- Count: `7`
- Safety: `metadata-only`
- Status: `available`
- Use: symbolic state contracts.
- Gap: needs non-raw proof narrowing.

### story-tracker

- Type: `story-md`
- Pattern: `docs/stories/RE-*.md`
- Count: `304`
- Safety: `metadata-only`
- Status: `available`
- Use: progression history and explicit blockers.
- Gap: needs gap extraction into ranked work items.

## Readiness

- Readiness: `blocked`
- Next ticket: `RE-294`
- Next topic: `evidence-source-gap-ranking`
- Selected domain: `none`
- Selected pivot: `none`
- Stop condition: `rank existing safe evidence sources before opening a new proof domain`

No production source or marker change is authorized by this inventory.
