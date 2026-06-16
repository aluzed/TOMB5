# RE-308 new non-raw proof evidence exploration

## Summary

The RE-307 exhaustion handoff is valid: no blocker-reduction metadata source remains ready, no proof domain is selected, and no source patch is authorized.

No current vector is testable now. The safe continuation requires either a changed upstream mapping export or a newly supplied metadata-only/source-symbolic proof artifact.

## Exploration vectors

- `changed-upstream-mapping`: `needs-new-export`; observed count `0`; next input `changed repo-function-map or function-priority export`.
- `new-user-supplied-proof-artifact`: `missing-input`; observed count `0`; next input `user-provided safe proof artifact or pointer`.
- `safe-source-symbolic-export`: `needs-new-export`; observed count `482`; next input `new structured source-symbolic export with proof linkage`.
- `existing-generated-metadata`: `exhausted-metadata`; observed count `339`; next input `changed generated metadata or newly derived safe evidence`.
- `existing-story-and-markdown-taxonomies`: `exhausted-metadata`; observed count `416`; next input `new taxonomy evidence not already gated blocked`.
- `raw-binary-or-asset-evidence`: `unsafe-raw-only`; observed count `0`; next input `replace with metadata-only or source-symbolic evidence`.

## Readiness decision

No production source or marker change is authorized. Domain selection stays blocked until a new safe input appears.
