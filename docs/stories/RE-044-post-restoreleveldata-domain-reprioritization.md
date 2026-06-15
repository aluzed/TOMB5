# RE-044 — Post-RestoreLevelData domain reprioritization

Status: Done

## Goal

Choose the next reverse-engineering domain after RE-043 closed the RestoreLevelData source reconstruction chain.

## Scope

- depends on: `RE-043`, `RE-004`
- source priority input: `docs/reverse/generated/function-priority.csv`
- safety contract: `metadata-only; no opcodes; no machine words; no payload coordinates; no branch or call targets; no copied dump records; no raw addresses in generated outputs`

## Progress

- [x] Closed RestoreLevelData chain excluded.
- [x] Existing backlog metadata consumed.
- [x] New domain shortlist generated.
- [x] Source patch authorization withheld pending domain-specific proof.

## Generated artifacts

- `docs/reverse/generated/re044-domain-reprioritization.csv`
- `docs/reverse/functions/re044-post-restoreleveldata-reprioritization.md`

## Findings

- RestoreLevelData chain status: `closed-by-RE-043`
- excluded closed-chain candidates: `3`
- top selected domain: `audio-effects`
- top selected function: `SoundEffect` in `GAME/EFFECTS.C`
- code-change readiness: `documentation-only-selection-gate`

## Selection decision

- decision: `start-new-domain-proof-chain`
- selected domain: `audio-effects`
- safe next action: `create RE-045 for audio-effects proof-first audit`
- Recommended next ticket: `RE-045`

Do not patch production source or add `(F)`, `(D)`, or `(**)` markers from RE-044 alone.

## Validation

- `python3 -m pytest tests/reverse/test_re044_post_restoreleveldata_reprioritization.py -q`
- metadata-only guard over RE-044 outputs

## Next step

RE-045: open a proof-first metadata-only audit for `audio-effects` before any source reconstruction or status marker change.
