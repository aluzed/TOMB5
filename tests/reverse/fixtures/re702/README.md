# Historical RE-702 inputs

These two RE-701 CSVs are verbatim snapshots from commit
`9dfc43382362eba0539365ba76495e36aa483b38`, under
`docs/reverse/generated/` (66 source files, 353 functions, 354 markers).

RE-702 is a terminal historical gate, not a live source inventory. Its tests
must not consume regenerated working-tree RE-701 exports: the live recursive
scan can also include ignored C files under `build/`.

The identity CSV retains the SHA-256 pinned by the unchanged production gate:
`f0a683d6c4d77f0016e0e25d0bb10f317c8fae2d95e3bf78d13ed475da7cba4f`.
Do not refresh these fixtures from current sources or relax the gate's counts,
fingerprint, blocked readiness, or zero-proof/zero-authorization checks.
Tests copy the snapshots to a temporary repository before mutating them;
artifact-writing tests write only to that temporary repository.
