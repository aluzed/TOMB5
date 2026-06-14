#!/usr/bin/env python3
"""Prepare and analyze the TOMB5 PS1 executable with Ghidra headless.

This script is intentionally conservative: it verifies the expected SLUS_013.11
hash before stripping the PS-X EXE header and importing the raw MIPS payload.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import struct
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

EXPECTED_BOOT = "SLUS_013.11"
EXPECTED_MD5 = "4ef523e708d7a7d6571f39c6e47784f9"
PSX_EXE_HEADER_SIZE = 0x800
PSX_RAM_PREFIX = 0x80000000


def run(cmd: list[str], log_file: Path | None = None, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if log_file is not None:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        with log_file.open("a", encoding="utf-8") as f:
            f.write("\n$ " + " ".join(cmd) + "\n")
            f.write(proc.stdout)
    if proc.returncode != 0:
        raise SystemExit(f"Command failed ({proc.returncode}): {' '.join(cmd)}\nSee log: {log_file}")
    return proc


def require_tool(name: str) -> str:
    path = shutil.which(name)
    if not path:
        raise SystemExit(f"Required tool not found in PATH: {name}")
    return path


def md5(path: Path) -> str:
    h = hashlib.md5()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def normalize_psx_addr(value: int) -> int:
    # PS-X EXE headers in this dump store KSEG0 addresses without 0x80000000.
    if value < PSX_RAM_PREFIX:
        return value | PSX_RAM_PREFIX
    return value


def parse_system_cnf(path: Path) -> str:
    text = path.read_text(errors="replace")
    match = re.search(r"BOOT\s*=\s*cdrom:\\([^;\r\n]+);1", text, flags=re.IGNORECASE)
    if not match:
        raise SystemExit(f"Could not find BOOT executable in {path}")
    return match.group(1).replace("\\", "").upper()


def parse_psx_exe_header(path: Path) -> dict[str, int | str]:
    data = path.read_bytes()[:PSX_EXE_HEADER_SIZE]
    if not data.startswith(b"PS-X EXE"):
        raise SystemExit(f"Not a PS-X EXE header: {path}")
    pc_raw = struct.unpack_from("<I", data, 0x10)[0]
    text_base_raw = struct.unpack_from("<I", data, 0x18)[0]
    text_size = struct.unpack_from("<I", data, 0x1C)[0]
    stack_raw = struct.unpack_from("<I", data, 0x30)[0]
    return {
        "pc_raw": f"0x{pc_raw:08x}",
        "entrypoint": f"0x{normalize_psx_addr(pc_raw):08x}",
        "text_base_raw": f"0x{text_base_raw:08x}",
        "text_base": f"0x{normalize_psx_addr(text_base_raw):08x}",
        "text_size": text_size,
        "stack_raw": f"0x{stack_raw:08x}",
        "stack": f"0x{normalize_psx_addr(stack_raw):08x}",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="TOMB5 repo root; default: current directory")
    parser.add_argument("--bin", default="TOMB5.BIN", help="PS1 BIN image relative to repo root")
    parser.add_argument("--cue", default="TOMB5.CUE", help="PS1 CUE image relative to repo root")
    parser.add_argument("--project-name", default="tomb5_psx_ntsc", help="Ghidra project name")
    parser.add_argument("--analysis-timeout", default="300", help="Ghidra analysis timeout per file in seconds")
    parser.add_argument("--keep-project", action="store_true", help="Keep the Ghidra project under build/reverse/ghidra-projects")
    parser.add_argument("--skip-ghidra", action="store_true", help="Prepare files and metadata but do not run analyzeHeadless")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    bin_path = (repo / args.bin).resolve()
    cue_path = (repo / args.cue).resolve()
    out_root = repo / "build" / "reverse"
    disc_dir = out_root / "disc"
    extracted_dir = out_root / "extracted"
    generated_dir = out_root / "generated"
    log_file = generated_dir / "prepare_ghidra_psx.log"
    summary_file = generated_dir / "prepare_ghidra_psx_summary.json"

    for tool in ["bchunk", "7z"]:
        require_tool(tool)
    if not args.skip_ghidra:
        require_tool("analyzeHeadless")

    if not bin_path.exists():
        raise SystemExit(f"Missing BIN image: {bin_path}")
    if not cue_path.exists():
        raise SystemExit(f"Missing CUE image: {cue_path}")

    generated_dir.mkdir(parents=True, exist_ok=True)
    log_file.write_text(f"prepare_ghidra_psx started {datetime.now(timezone.utc).isoformat()}\n", encoding="utf-8")
    disc_dir.mkdir(parents=True, exist_ok=True)
    extracted_dir.mkdir(parents=True, exist_ok=True)

    iso_prefix = disc_dir / "tomb5_"
    iso_path = disc_dir / "tomb5_01.iso"
    if iso_path.exists():
        iso_path.unlink()
    run(["bchunk", str(bin_path), str(cue_path), str(iso_prefix)], log_file=log_file)
    if not iso_path.exists():
        raise SystemExit(f"Expected ISO not created: {iso_path}")

    # Extract SYSTEM.CNF first, then boot executable named by SYSTEM.CNF.
    run(["7z", "x", "-y", f"-o{extracted_dir}", str(iso_path), "SYSTEM.CNF"], log_file=log_file)
    system_cnf = extracted_dir / "SYSTEM.CNF"
    boot_name = parse_system_cnf(system_cnf)
    run(["7z", "x", "-y", f"-o{extracted_dir}", str(iso_path), boot_name], log_file=log_file)
    boot_exe = extracted_dir / boot_name
    if not boot_exe.exists():
        raise SystemExit(f"Boot executable was not extracted: {boot_exe}")

    boot_md5 = md5(boot_exe)
    if boot_name != EXPECTED_BOOT or boot_md5.lower() != EXPECTED_MD5:
        raise SystemExit(
            "Unexpected boot executable. "
            f"got {boot_name} md5={boot_md5}, expected {EXPECTED_BOOT} md5={EXPECTED_MD5}"
        )

    header = parse_psx_exe_header(boot_exe)
    payload = extracted_dir / f"{boot_name}.payload.bin"
    with boot_exe.open("rb") as src, payload.open("wb") as dst:
        src.seek(PSX_EXE_HEADER_SIZE)
        shutil.copyfileobj(src, dst)

    if payload.stat().st_size != int(header["text_size"]):
        raise SystemExit(
            f"Payload size mismatch: got {payload.stat().st_size}, header says {header['text_size']}"
        )

    ghidra_ran = False
    ghidra_project_dir = out_root / "ghidra-projects"
    if not args.skip_ghidra:
        ghidra_project_dir.mkdir(parents=True, exist_ok=True)
        cmd = [
            "analyzeHeadless",
            str(ghidra_project_dir),
            args.project_name,
            "-import", str(payload),
            "-processor", "MIPS:LE:32:default",
            "-cspec", "default",
            "-loader", "BinaryLoader",
            "-loader-baseAddr", str(header["text_base"]),
            "-analysisTimeoutPerFile", str(args.analysis_timeout),
        ]
        if not args.keep_project:
            cmd.append("-deleteProject")
        run(cmd, log_file=log_file)
        ghidra_ran = True

    summary = {
        "repo": str(repo),
        "bin": str(bin_path),
        "cue": str(cue_path),
        "iso": str(iso_path),
        "system_cnf": str(system_cnf),
        "boot_executable": str(boot_exe),
        "boot_name": boot_name,
        "boot_md5": boot_md5,
        "expected_md5": EXPECTED_MD5,
        "payload": str(payload),
        "payload_size": payload.stat().st_size,
        "ghidra_ran": ghidra_ran,
        "ghidra_project_dir": str(ghidra_project_dir),
        "ghidra_project_name": args.project_name,
        **header,
    }
    summary_file.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(json.dumps(summary, indent=2, sort_keys=True))
    print(f"\nLog: {log_file}")
    print(f"Summary: {summary_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
