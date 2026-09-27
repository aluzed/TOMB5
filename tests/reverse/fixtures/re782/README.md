# RE-782 — isolated real-TU bridge contract

The runner compiles the entire selected `GAME/OBJECTS.C` with normal project headers,
Linux g++ i386, PSX_VERSION and PSXPC_TEST, then links normally with unused-section
elimination. It never extracts a function body or permits unresolved symbols.

1260 synthetic cases exercise all six bridge routines by their declared long
signature: five rotations, seven coordinate pairs, two item heights, and queries
below/equal/above each surface. Assertions check output, adjacent canaries, the
complete item buffer and both globals. Ceiling expectations come from the
attributed target execution documented in RE-782; floors are regression controls.

The three ceiling bodies change only on the attributed backend branch. This is
not a native registration test: int/int* object slots are deliberately not used.
It does not certify startup, GetCeiling consumption, gameplay, LP64 or extreme
coordinates producing signed overflow. The optional UBSan mode is similarly
limited to this fixture; it does not resolve the pre-existing GetFloor debt.

Run from the repository with a new output directory:

    python3 tests/reverse/fixtures/re782/run_test.py --root . --source GAME/OBJECTS.C --output /tmp/re782-fresh

Add `--sanitize` for the bounded undefined-behavior sanitizer run.
No protected assets or target instruction dumps are required by this public test.
