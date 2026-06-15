# RE-046 — SoundEffect caller map

Status: Done

## Goal

Advance `audio-effects` / `SoundEffect` through `soundeffect-caller-map` as a metadata-only reverse-engineering step.

## Scope

- depends on: `RE-045`
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

- callers classified: `75`
- selected cluster: `audio-effects-internal`

## Readiness decision

- decision: `caller-clusters-published`
- safe next action: `advance to argument taxonomy`
- code change readiness: `blocked`
- next ticket: `RE-047`

Do not patch production source or add `(F)`, `(D)`, or `(**)` markers from this story alone.

## Validation

- `python3 -m pytest tests/reverse/test_re045_re052_audio_effects_chain.py -q`
- metadata-only guard over RE-045..RE-052 outputs

## Next step

RE-047: advance to argument taxonomy.
