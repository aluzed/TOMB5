# RE-162 — Post-module-game domain reprioritization

Status: Done

## Goal

Select the next reverse-engineering backlog outside the exhausted RE-061 module-game parent domain.

## Scope

- depends on: `RE-161`, `RE-044`
- safety contract: metadata-only generated rows; binary instruction text, proprietary dump records, and raw address literals stay out of versioned outputs

## Progress tracker

- [x] RE-161 module-game exhaustion handoff consumed.
- [x] Closed domains excluded.
- [x] Next-domain shortlist generated.
- [x] Readiness decision recorded.
- [x] Forbidden raw evidence excluded.

## Generated artifacts

- `docs/reverse/generated/re162-post-module-game-domain-reprioritization.csv`
- `docs/reverse/functions/re162-post-module-game-domain-reprioritization.md`

## Findings

- selected next domain: `module-spec_psxpc_n`
- selected pivot: `PrintString`
- excluded closed domains: `audio-effects, collision, module-game`
- all rows remain blocked for source or marker changes until a domain-specific proof-first audit runs

## Selection decision

Recommended next ticket: `RE-163`
Code-change readiness: `documentation-only-selection-gate`
No production source or marker change is authorized by this selection gate.

## Validation

- `python3 -m pytest tests/reverse/test_re162_post_module_game_reprioritization.py -q`
- metadata-only guard over RE-162 outputs

## Next step

RE-163: open a proof-first audit for `module-spec_psxpc_n` / `PrintString`.
