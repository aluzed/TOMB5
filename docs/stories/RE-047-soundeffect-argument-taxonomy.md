# RE-047 — SoundEffect argument taxonomy

Status: Done

## Goal

Advance `audio-effects` / `SoundEffect` through `soundeffect-argument-taxonomy` as a metadata-only reverse-engineering step.

## Scope

- depends on: `RE-046`
- safety contract: `metadata-only; no opcodes; no machine words; no payload coordinates; no branch or call targets; no copied dump records; no raw addresses in generated outputs`

## Progress

- [x] Input artifacts loaded.
- [x] Metadata only artifact published.
- [x] Readiness decision recorded.
- [x] Forbidden raw evidence excluded.

## Generated artifacts

- `docs/reverse/generated/re045-re052-audio-effects-chain.csv`
- `docs/reverse/functions/re045-re052-audio-effects-chain.md`

## Findings

- source callsites classified: `145`
- argument shapes: `16`

## Readiness decision

- decision: `argument-shapes-published`
- safe next action: `advance to comparison gate`
- code change readiness: `blocked`
- next ticket: `RE-048`

Do not patch production source or add `(F)`, `(D)`, or `(**)` markers from this story alone.

## Validation

- `python3 -m pytest tests/reverse/test_re045_re052_audio_effects_chain.py -q`
- metadata-only guard over RE-045..RE-052 outputs

## Next step

RE-048: advance to comparison gate.
