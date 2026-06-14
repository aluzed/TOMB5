# Ghidra workflow for TOMB5 PSX NTSC

Status: In progress

This document describes the reproducible Ghidra workflow for the Tomb Raider: Chronicles PSX NTSC executable used by this repo.

## Inputs

Expected repo-root files:

- `TOMB5.BIN` — PlayStation disc image, MODE2/2352.
- `TOMB5.CUE` — cue sheet whose `FILE` entry points to `TOMB5.BIN`.

Expected boot executable:

- Name: `SLUS_013.11`
- MD5: `4ef523e708d7a7d6571f39c6e47784f9`
- Repo reference: `CONTRIBUTING.md`, section `Base Versions (PSX)`.

## One-command workflow

From the repo root:

```bash
python3 scripts/reverse/prepare_ghidra_psx.py
```

The script performs these steps:

1. Converts `TOMB5.BIN/TOMB5.CUE` to a temporary ISO with `bchunk`.
2. Extracts `SYSTEM.CNF` with `7z`.
3. Reads `SYSTEM.CNF` to find the boot executable.
4. Extracts `SLUS_013.11`.
5. Verifies the MD5 against the repo baseline.
6. Parses the PS-X EXE header.
7. Strips the `0x800`-byte PS-X EXE header to create `SLUS_013.11.payload.bin`.
8. Runs Ghidra headless on the raw payload as little-endian MIPS.
9. Writes a log and JSON summary under `build/reverse/generated/`.

## Outputs

Generated files are intentionally placed under `build/reverse/` and should not be committed.

- `build/reverse/disc/tomb5_01.iso`
- `build/reverse/extracted/SYSTEM.CNF`
- `build/reverse/extracted/SLUS_013.11`
- `build/reverse/extracted/SLUS_013.11.payload.bin`
- `build/reverse/generated/prepare_ghidra_psx.log`
- `build/reverse/generated/prepare_ghidra_psx_summary.json`

## Ghidra import details

Ghidra headless does not auto-load the original `PS-X EXE` file here. Direct import fails with `No load spec found`.

Instead, import the stripped payload as raw binary:

```bash
analyzeHeadless build/reverse/ghidra-projects tomb5_psx_ntsc \
  -import build/reverse/extracted/SLUS_013.11.payload.bin \
  -processor MIPS:LE:32:default \
  -cspec default \
  -loader BinaryLoader \
  -loader-baseAddr 0x80010000 \
  -analysisTimeoutPerFile 300 \
  -deleteProject
```

Verified header values for this executable:

- entrypoint: `0x8007663c`
- text base: `0x80010000`
- text size: `606208` bytes (`0x94000`)
- stack: `0x801ffff0`

## Function export and repo mapping

From the repo root:

```bash
python3 scripts/reverse/map_ghidra_to_repo.py
```

For a faster rerun when `build/reverse/generated/prepare_ghidra_psx_summary.json` and the payload already exist:

```bash
python3 scripts/reverse/map_ghidra_to_repo.py --skip-prepare
```

The mapping script runs Ghidra headless with `scripts/reverse/ExportGhidraFunctions.java` as a post-script, exports functions to CSV, parses repo comments such as `//61EE8(<), 625CC(<) (F) (D)`, normalizes final PSX addresses to `0x80xxxxxx`, and maps by exact address.

Primary generated outputs:

- `docs/reverse/generated/ghidra-functions.csv`
- `docs/reverse/generated/repo-functions.csv`
- `docs/reverse/generated/repo-function-map.csv`
- `docs/reverse/generated/mapped-functions.md`
- `docs/reverse/generated/repo-only-functions.md`
- `docs/reverse/generated/unmapped-ghidra-functions.md`
- `docs/reverse/generated/function-map-summary.json`

The same files are also mirrored under `build/reverse/generated/` together with logs.

Current verified summary:

- Ghidra functions: `1440`
- repo functions parsed: `1250`
- mapped functions: `866`
- repo-only functions: `384`
- Ghidra-only functions: `723`

## Keeping the Ghidra project

By default, the script deletes the temporary Ghidra project after analysis to keep the workspace small.

To keep the project for GUI inspection:

```bash
python3 scripts/reverse/prepare_ghidra_psx.py --keep-project
```

Project directory:

`build/reverse/ghidra-projects/tomb5_psx_ntsc.gpr`

## Failure modes

- Missing `bchunk`, `7z`, or `analyzeHeadless`: install the missing tool first.
- Missing `TOMB5.BIN/TOMB5.CUE`: recreate the symlink/cue at repo root.
- MD5 mismatch: stop; the disc image is not the baseline expected by this repo.
- Payload size mismatch: stop; the PS-X EXE header parse or input file is wrong.
