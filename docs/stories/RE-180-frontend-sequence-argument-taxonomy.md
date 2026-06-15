# RE-180 — frontend-sequence-argument-taxonomy

## Goal
Advance `frontend-sequence` in `module-spec_psxpc_n` using metadata-only proof artifacts.

## Progress tracker
- [x] consumed upstream scope/plan
- [x] emitted deterministic metadata-only artifacts
- [x] kept source and marker changes blocked
- [x] recorded validation path and next dependency

## Generated artifacts
- `docs/reverse/generated/re180-frontend-sequence-argument-taxonomy.csv`
- `docs/reverse/generated/re178-re184-frontend-sequence-epic.csv`
- `docs/reverse/functions/re178-re184-frontend-sequence-epic.md`

## Findings
- FMV playback and cutscene selector families classified
- taxonomy remains source-backed only

## Readiness decision
- status: `completed-documentation-only`
- decision: `blocked-no-source-or-marker-change`
- code change readiness: `blocked`
- next ticket: `RE-181`

## Validation
- `python3 -m pytest tests/reverse/test_re178_re184_frontend_sequence_epic.py -q`
- `python3 -m pytest tests/reverse -q`
- metadata-only guard over generated RE-178..RE-184 artifacts
