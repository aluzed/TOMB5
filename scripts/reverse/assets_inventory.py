#!/usr/bin/env python3
"""Generate lightweight disc/GAMEWAD asset inventories for TOMB5.

This script intentionally writes only text/JSON inventories under docs/reverse/generated.
Large extracted assets stay under build/reverse/re006 and are ignored by git.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import shutil
import struct
import subprocess
from dataclasses import dataclass, asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_WORK = ROOT / "build" / "reverse" / "re006"
DEFAULT_OUT = ROOT / "docs" / "reverse" / "generated"

GAMEWAD_NAMES = [
    "SETUP.MOD",
    "CUTSEQ.JIZ",
    "TITLE.PSX",
    "ANDREA1.PSX",
    "ANDREA2.PSX",
    "ANDREA3.PSX",
    "JOBY2.PSX",
    "JOBY3.PSX",
    "JOBY4.PSX",
    "JOBY5.PSX",
    "ANDY1.PSX",
    "ANDY2.PSX",
    "ANDY3.PSX",
    "RICH1.PSX",
    "RICH2.PSX",
    "RICHCUT2.PSX",
    "RICH3.PSX",
    "RESERVED_17",
    "RESERVED_18",
    "RESERVED_19",
    "RESERVED_20",
    "RESERVED_21",
    "RESERVED_22",
    "RESERVED_23",
    "RESERVED_24",
    "RESERVED_25",
    "RESERVED_26",
    "RESERVED_27",
    "RESERVED_28",
    "RESERVED_29",
    "EXTRAS1.RAW",
    "EXTRAS2.RAW",
    "EXTRAS3.RAW",
    "RESERVED_33",
    "RESERVED_34",
    "RESERVED_35",
    "RESERVED_36",
    "RESERVED_37",
    "RESERVED_38",
    "RESERVED_39",
    "RESERVED_40",
    "TR5LEGAL_EN.RAW",
    "TR4LEGAL_FR.RAW",
    "TR4LEGAL_US.RAW",
    "TR4LEGAL_EN.RAW",
    "TR4LEGAL_EN.RAW",
    "TR5LEGAL_EN.RAW",
    "TR4LEGAL_US.RAW",
    "TR4LEGAL_EN.RAW",
    "TR4LOGO_FR.RAW",
    "TR4LOGO_EN.RAW",
]

LOADING_SCREEN_IMG_SIZE = 512 * 256 * 2
LOADING_CD_IMG_SIZE = 64 * 64 * 2
CD_SECTOR_SIZE = 2048
CODEWAD_PROBE_INDEX = 146
LEVEL_CODEWAD_TRAILER_HACK = 0x691B4
LEVEL_ENTRY_RANGE = range(2, 17)


@dataclass
class DiscFile:
    name: str
    size: int
    date: str
    time: str
    category: str


@dataclass
class GamewadEntry:
    index: int
    name: str
    offset: int
    size: int
    aligned_2048: bool
    category: str
    extracted_path_hint: str
    embedded_codewad_offset: int | None = None
    embedded_codewad_size: int | None = None
    embedded_level_payload_size: int | None = None


def run(cmd: list[str], cwd: Path = ROOT, capture: bool = True) -> str:
    proc = subprocess.run(
        cmd,
        cwd=cwd,
        check=True,
        text=True,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.STDOUT if capture else None,
    )
    return proc.stdout or ""


def ensure_iso(bin_path: Path, cue_path: Path, work: Path) -> Path:
    work.mkdir(parents=True, exist_ok=True)
    iso = work / "tomb501.iso"
    if not iso.exists():
        if not shutil.which("bchunk"):
            raise SystemExit("bchunk is required to convert TOMB5.BIN/TOMB5.CUE to ISO")
        run(["bchunk", str(bin_path), str(cue_path), str(work / "tomb5")])
        generated = work / "tomb501.iso"
        if not generated.exists():
            raise SystemExit("bchunk did not generate tomb501.iso")
    return iso


def parse_7z_listing(text: str) -> list[DiscFile]:
    rows: list[DiscFile] = []
    line_re = re.compile(
        r"^(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2})\s+\.\.\.\.\.\s+(\d+)\s+\d+\s+(.+)$"
    )
    for line in text.splitlines():
        m = line_re.match(line)
        if not m:
            continue
        date, time, size, name = m.groups()
        rows.append(DiscFile(name=name.strip(), size=int(size), date=date, time=time, category=disc_category(name)))
    return rows


def disc_category(name: str) -> str:
    upper = name.upper()
    if upper == "GAMEWAD.OBJ":
        return "gamewad_container"
    if upper == "SLUS_013.11":
        return "boot_executable"
    if upper.endswith(".STR"):
        return "fmv_stream"
    if upper.endswith(".XA"):
        return "xa_audio"
    if upper in {"SYSTEM.CNF", "SCRIPT.DAT", "US.DAT"}:
        return "runtime_metadata"
    return "other"


def gamewad_category(index: int, name: str, size: int) -> str:
    if size == 0:
        return "reserved_empty"
    if index == 0:
        return "setup_module"
    if index == 1:
        return "cutscene_index_or_blob"
    if index in LEVEL_ENTRY_RANGE:
        return "level_entry_with_loading_assets_and_embedded_codewad"
    if 30 <= index <= 32:
        return "extras_storyboard_raw"
    if 41 <= index <= 48:
        return "legal_screen_raw"
    if 49 <= index <= 50:
        return "logo_raw"
    return "unknown_nonempty"


def align_2048(value: int) -> int:
    return (value + CD_SECTOR_SIZE - 1) & ~(CD_SECTOR_SIZE - 1)


def parse_gamewad(gamewad_path: Path) -> list[GamewadEntry]:
    data = gamewad_path.read_bytes()
    entries: list[GamewadEntry] = []
    header = data[: len(GAMEWAD_NAMES) * 8]
    raw = [struct.unpack_from("<ii", header, i * 8) for i in range(len(GAMEWAD_NAMES))]
    setup_size = raw[0][1]
    for i, (offset, size) in enumerate(raw):
        name = GAMEWAD_NAMES[i]
        item = GamewadEntry(
            index=i,
            name=name,
            offset=offset,
            size=size,
            aligned_2048=(offset % CD_SECTOR_SIZE == 0),
            category=gamewad_category(i, name, size),
            extracted_path_hint=f"build/reverse/re006/gamewad/{i:02d}-{name}",
        )
        if i in LEVEL_ENTRY_RANGE and offset > 0 and size > 0:
            pos = offset + LOADING_SCREEN_IMG_SIZE + LOADING_CD_IMG_SIZE + setup_size
            pos = align_2048(pos)
            level_payload_size = size - (pos - offset) - LEVEL_CODEWAD_TRAILER_HACK
            codewad_start = align_2048(pos + max(level_payload_size, 0))
            probe = codewad_start + CODEWAD_PROBE_INDEX * 8
            if 0 <= probe + 8 <= len(data) and offset <= codewad_start < offset + size:
                code_data_offset, code_data_size = struct.unpack_from("<ii", data, probe)
                codewad_size = code_data_offset + code_data_size
                if 0 < codewad_size <= size:
                    item.embedded_codewad_offset = codewad_start
                    item.embedded_codewad_size = codewad_size
            if level_payload_size >= 0:
                item.embedded_level_payload_size = level_payload_size
        entries.append(item)
    return entries


def write_disc_files(path: Path, rows: list[DiscFile]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="\t", lineterminator="\n")
        writer.writerow(["name", "size", "date", "time", "category"])
        for r in rows:
            writer.writerow([r.name, r.size, r.date, r.time, r.category])


def write_gamewad_files(path: Path, rows: list[GamewadEntry]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="\t", lineterminator="\n")
        writer.writerow([
            "index",
            "name",
            "offset",
            "size",
            "aligned_2048",
            "category",
            "embedded_level_payload_size",
            "embedded_codewad_offset",
            "embedded_codewad_size",
        ])
        for r in rows:
            writer.writerow([
                r.index,
                r.name,
                r.offset,
                r.size,
                str(r.aligned_2048).lower(),
                r.category,
                r.embedded_level_payload_size if r.embedded_level_payload_size is not None else "",
                r.embedded_codewad_offset if r.embedded_codewad_offset is not None else "",
                r.embedded_codewad_size if r.embedded_codewad_size is not None else "",
            ])


def extract_gamewad(iso: Path, work: Path) -> Path:
    extract_dir = work / "iso_extract"
    extract_dir.mkdir(parents=True, exist_ok=True)
    gamewad = extract_dir / "GAMEWAD.OBJ"
    if not gamewad.exists():
        if not shutil.which("7z"):
            raise SystemExit("7z is required to extract GAMEWAD.OBJ from ISO")
        run(["7z", "x", "-y", f"-o{extract_dir}", str(iso), "GAMEWAD.OBJ", "SYSTEM.CNF", "SCRIPT.DAT", "US.DAT"])
    return gamewad


def maybe_unpack_gamewad(gamewad: Path, work: Path) -> None:
    # This is a verification side effect only. Do not commit the output.
    output = work / "gamewad"
    if output.exists():
        shutil.rmtree(output)
    run(["python3", str(ROOT / "scripts" / "gamewad.py"), "unpack", str(gamewad), str(output)])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bin", default=str(ROOT / "TOMB5.BIN"))
    parser.add_argument("--cue", default=str(ROOT / "TOMB5.CUE"))
    parser.add_argument("--work", default=str(DEFAULT_WORK))
    parser.add_argument("--out", default=str(DEFAULT_OUT))
    parser.add_argument("--skip-unpack", action="store_true", help="Do not run scripts/gamewad.py verification unpack")
    args = parser.parse_args()

    work = Path(args.work)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    iso = ensure_iso(Path(args.bin), Path(args.cue), work)
    listing = run(["7z", "l", str(iso)])
    disc_rows = parse_7z_listing(listing)
    gamewad = extract_gamewad(iso, work)
    gamewad_rows = parse_gamewad(gamewad)
    if not args.skip_unpack:
        maybe_unpack_gamewad(gamewad, work)

    write_disc_files(out / "disc-files.txt", disc_rows)
    write_gamewad_files(out / "gamewad-files.txt", gamewad_rows)

    summary = {
        "disc": {
            "source_bin": str(Path(args.bin)),
            "source_cue": str(Path(args.cue)),
            "iso": str(iso),
            "file_count": len(disc_rows),
            "total_listed_size": sum(r.size for r in disc_rows),
            "categories": {cat: sum(1 for r in disc_rows if r.category == cat) for cat in sorted({r.category for r in disc_rows})},
        },
        "gamewad": {
            "path": str(gamewad),
            "size": gamewad.stat().st_size,
            "entry_count": len(gamewad_rows),
            "nonempty_entries": sum(1 for r in gamewad_rows if r.size > 0),
            "empty_entries": sum(1 for r in gamewad_rows if r.size == 0),
            "entries_with_embedded_codewad": sum(1 for r in gamewad_rows if r.embedded_codewad_size),
            "categories": {cat: sum(1 for r in gamewad_rows if r.category == cat) for cat in sorted({r.category for r in gamewad_rows})},
        },
        "generated": {
            "disc_files": "docs/reverse/generated/disc-files.txt",
            "gamewad_files": "docs/reverse/generated/gamewad-files.txt",
            "assets_summary": "docs/reverse/generated/assets-summary.json",
        },
        "copyright_safety": "Large extracted assets are under build/reverse/re006 and are not intended for git.",
    }
    (out / "assets-summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
