# RE-306 handoff stop-condition readiness gate

## Progress tracker

- [x] RE-305 handoff stop-condition reduction handoff validated.
- [x] RE-305 fingerprint-only evidence schema checked.
- [x] Handoff stop-condition classes gated for proof-domain reopen readiness.
- [x] Proof-domain selection kept blocked pending blocker-reduction source exhaustion audit.

## Gate decision

- Handoff stop-condition classes gated: `5`
- Ready to reopen proof-domain selection: `0`
- Classes needing new evidence/input changes: `5`
- Source patch authorized rows: `0`
- Next metadata source: `blocker-reduction-source-exhaustion-audit`
- Next topic: `blocker-reduction-source-exhaustion-audit`

Handoff stop-condition classes do not reopen proof-domain selection. They consolidate prior stop reasons, but they do not provide new non-raw proof evidence, changed upstream mapping, a selected domain, or source authorization.

## Gate rows

### `proof-blocked-or-no-marker-patch`

- Evidence rows: `27`
- Handoff files: `27`
- Unique stop-condition fingerprints: `27`
- Gate decision: `needs-new-non-raw-proof-evidence`
- Reason: handoff stop conditions still end in proof blockers or no-marker/no-source-patch states
- Ready to reopen domain: `no`
- Source patch authorized: `no`

### `metadata-reduction-before-domain-selection`

- Evidence rows: `12`
- Handoff files: `12`
- Unique stop-condition fingerprints: `12`
- Gate decision: `needs-new-non-raw-proof-evidence`
- Reason: handoff stop conditions request more metadata reduction before domain selection, not a ready domain
- Ready to reopen domain: `no`
- Source patch authorized: `no`

### `generic-handoff-stop-condition`

- Evidence rows: `7`
- Handoff files: `7`
- Unique stop-condition fingerprints: `7`
- Gate decision: `needs-new-non-raw-proof-evidence`
- Reason: generic handoff stop conditions need exhaustion audit rather than domain selection
- Ready to reopen domain: `no`
- Source patch authorized: `no`

### `upstream-input-refresh-or-change-needed`

- Evidence rows: `3`
- Handoff files: `3`
- Unique stop-condition fingerprints: `3`
- Gate decision: `needs-upstream-input-change`
- Reason: upstream inputs or new non-raw evidence must change before any proof domain can reopen
- Ready to reopen domain: `no`
- Source patch authorized: `no`

### `readiness-gate-before-domain-selection`

- Evidence rows: `1`
- Handoff files: `1`
- Unique stop-condition fingerprints: `1`
- Gate decision: `needs-new-non-raw-proof-evidence`
- Reason: readiness gates remain prerequisites and do not themselves authorize source or marker changes
- Ready to reopen domain: `no`
- Source patch authorized: `no`

## Readiness decision

No production source or marker change is authorized by this gate.
The next safe step is to audit exhaustion of the blocker-reduction metadata sources before selecting another proof domain.
